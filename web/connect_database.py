# connect_database.py
import pymysql,os

# 資料庫參數設定
connection_params = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT")),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "db": os.environ.get("DB_NAME"),
    "charset": "utf8",
    "cursorclass": pymysql.cursors.DictCursor
}

def check(data):
    try:
        c_id = data["c_id"]
        r_start = data["r_start"]
        r_end = data["r_end"]
        room = data["room"]
        topic = data["topic"]
        successful_message = ' '

        # 建立資料庫連接
        with pymysql.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                # 檢查 c_id 是否存在
                check_id_sql = "SELECT c_id,c_name FROM customer WHERE c_id = %s"
                cursor.execute(check_id_sql, (c_id,))
                result = cursor.fetchone()
                if cursor.rowcount == 0:
                    return "預約失敗，ID不存在!"
                
                # 取得顧客名字
                c_name = result["c_name"]  
                
                # 檢查 room 是否存在
                check_room_sql = "SELECT room_no FROM room WHERE room_no = %s"
                cursor.execute(check_room_sql, (room,))
                if cursor.rowcount == 0:
                    return "無此會議室，請重新預約!"
                # 檢查特定的會議室在特定時間是否已被預定
                check_time_and_room_sql = """ 
                SELECT * FROM reserve 
                WHERE room_no = %s AND (
                    (r_start <= %s AND r_end >= %s) OR  
                    (r_start >= %s AND r_start <= %s) OR 
                    (r_end >= %s AND r_end <= %s)         
                )AND r_del = 0

                """
                cursor.execute(check_time_and_room_sql, (room, r_start, r_start, r_end, r_end, r_start, r_end,))
                if cursor.rowcount > 0:
                    return "預約失敗，會議室已被預定!"
                                    
                # 插入預約
                insert_sql = "INSERT INTO reserve (r_start, r_end, c_id, room_no, topic) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_sql, (r_start, r_end, c_id, room, topic))    
                successful_message = successful_message = (
                    "預約成功!&" +
                    "預約ID : " + c_id + "&" +
                    "用戶名字 : " + c_name + "&" +
                    "會議室 : " + room + "&" +
                    "會議主題 : " + topic + "&" +
                    "從 " + r_start + " 到 " + r_end
                )
                # 取得自動生成的 r_no
                r_no = cursor.lastrowid
                insert_sign_sql = "INSERT INTO sign (s_no, room_no, c_id) VALUES (%s, %s, %s)"
                cursor.execute(insert_sign_sql,(r_no, room, c_id))
            connection.commit()
        return successful_message
    except pymysql.MySQLError as e:
        return "尚未連接資料庫,無法處理您的預約訊息"  # 或者返回其他適當的錯誤消息

def view(data):
    try:
        viewTime = data["viewTime"]            

        # 建立資料庫連接
        with pymysql.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                view_time_query = """
                SELECT r.*, c.c_name
                FROM reserve r
                LEFT JOIN sign s ON r.r_no = s.s_no
                LEFT JOIN customer c ON r.c_id = c.c_id
                WHERE (DATE(r_start) <= %s AND DATE(r_end) >= %s) AND r.r_no = s.s_no
                ORDER BY r.r_no ASC
                """
                cursor.execute(view_time_query, (viewTime, viewTime,))
                results = cursor.fetchall()
            # 重新編號 r_no
            new_results = []
            new_r_no = 1
            for result in results:
                result["r_no"] = new_r_no
                new_results.append(result)
                new_r_no += 1
            return new_results
    except pymysql.MySQLError as e:
        return "尚未連接資料庫"  # 或者返回其他適當的錯誤訊息
def modify(data):
    try:
        m_id = data["m_id"]
        # 建立資料庫連接
        with pymysql.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                c_id_query = "SELECT r_no, r_start, r_end, room_no, c_id FROM reserve WHERE c_id = %s AND r_del = 0 ORDER BY r_no ASC"
                cursor.execute(c_id_query, (m_id,))
                results = cursor.fetchall()
                return results
    except pymysql.MySQLError as e:
        return "資料庫連接錯誤，無法查詢預約資料"
def delete(data):
    r_no = data["r_no"]
    with pymysql.connect(**connection_params) as connection:
        with connection.cursor() as cursor:
            #更新reserve資料表的r_del變為1 
            update = "UPDATE reserve SET r_del = 1 WHERE r_no = %s"
            cursor.execute(update, (r_no,))
            #刪除sign資料表的簽到記錄
            delete = "DELETE FROM sign WHERE s_no = %s"
            cursor.execute(delete, (r_no,))
            connection.commit()
    try:            
        c_id = data["c_id"]
        # 建立資料庫連接
        with pymysql.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                c_id_query = "SELECT r_no, r_start, r_end, room_no FROM reserve WHERE c_id = %s AND r_del = 0 ORDER BY r_no ASC"
                cursor.execute(c_id_query, (c_id,))
                results = cursor.fetchall()
                return results
    except pymysql.MySQLError as e:
        return "資料庫連接錯誤，無法查詢預約資料"


def now():
    try:  
        with pymysql.connect(**connection_params) as connection:
            with connection.cursor() as cursor: 
                # 首先檢查是否有有效的預約
                query = """
                WITH RankedSign AS (
                    SELECT
                        s_no,
                        s_in,
                        room_no,
                        ROW_NUMBER() OVER (PARTITION BY room_no ORDER BY s_in DESC) AS rn
                    FROM
                        sign
                )
                SELECT 
                    room.room_no,
                    CASE 
                        WHEN latest_reserve.r_start <= NOW() 
                            AND latest_reserve.r_end >= NOW() 
                            AND latest_reserve.r_del = 0 
                            AND sign.s_in IS NOT NULL  -- 確保有簽入時間
                            AND sign.s_in BETWEEN latest_reserve.r_start AND latest_reserve.r_end  -- 簽入時間在預約時段內
                        THEN '使用中'
                        WHEN latest_reserve.r_start <= NOW() 
                            AND latest_reserve.r_end >= NOW() 
                            AND latest_reserve.r_del = 0 
                            AND sign.s_in IS NULL  -- 無簽入時間
                        THEN '已經在預約時間內，但尚未有人簽入'
                        ELSE '空室'
                    END AS room_status
                FROM 
                    room
                LEFT JOIN (
                    SELECT 
                        room_no,
                        MAX(r_start) AS r_start,
                        MAX(r_end) AS r_end,
                        MAX(r_del) AS r_del
                    FROM 
                        reserve
                    WHERE 
                        NOW() BETWEEN r_start AND r_end
                        AND r_del = 0
                    GROUP BY 
                        room_no
                ) AS latest_reserve ON room.room_no = latest_reserve.room_no
                LEFT JOIN RankedSign sign ON room.room_no = sign.room_no AND sign.rn = 1;
                """
                cursor.execute(query)  # 執行 SQL 查詢
                results = cursor.fetchall()
                print (results)
                return results
                
    except pymysql.MySQLError as e:
        return f"資料庫連接錯誤，無法查詢預約資料: {e}"