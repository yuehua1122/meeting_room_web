# connect_database.py
import pymysql

# 資料庫參數設定
connection_params = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "kevinbear60404",
    "db": "meeting room",
    "charset": "utf8",
    "cursorclass": pymysql.cursors.DictCursor
}

def check(data):
    try:
        c_id = data["c_id"]
        r_start = data["r_start"]
        r_end = data["r_end"]
        room = data["room"]
        successful_message = ' '

        # 建立資料庫連接
        with pymysql.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                # 檢查 c_id 是否存在
                check_id_sql = "SELECT c_id FROM customer WHERE c_id = %s"
                cursor.execute(check_id_sql, (c_id,))
                if cursor.rowcount == 0:
                    return "預約失敗，ID不存在!"
                
            
                # 檢查特定的會議室在特定時間是否已被預定
                check_time_and_room_sql = """ 
                SELECT * FROM reserve 
                WHERE room_no = %s AND (
                    (r_start <= %s AND r_end >= %s) OR  
                    (r_start >= %s AND r_start <= %s) OR 
                    (r_end >= %s AND r_end <= %s)         
                )AND r_del = FALSE
                """
                cursor.execute(check_time_and_room_sql, (room, r_start, r_start, r_end, r_end, r_start, r_end,))
                if cursor.rowcount > 0:
                    return "預約失敗，會議室已被預定!"
                                
                # 插入預約
                insert_sql = "INSERT INTO reserve (r_start, r_end, c_id, room_no) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_sql, (r_start, r_end, c_id, room,))    
                successful_message = "預約成功!&" + "預約ID : " + c_id + "&會議室 : " + room + "&從 " + r_start + " 到 " + r_end 
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
                view_time_query = "SELECT * FROM reserve WHERE (DATE(r_start) <= %s AND DATE(r_end) >= %s)AND r_del ORDER BY r_no ASC"
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
                c_id_query = "SELECT r_no, r_start, r_end, room_no, c_id FROM reserve WHERE c_id = %s AND r_del = FALSE ORDER BY r_no ASC"
                cursor.execute(c_id_query, (m_id,))
                results = cursor.fetchall()
                return results
    except pymysql.MySQLError as e:
        return "資料庫連接錯誤，無法查詢預約資料"
    
def delete(data):
    r_no = data["r_no"]
    with pymysql.connect(**connection_params) as connection:
        with connection.cursor() as cursor: 
            update = "UPDATE reserve SET r_del = TRUE WHERE r_no = %s"
            cursor.execute(update, (r_no,))
            connection.commit()
    try:            
        c_id = data["c_id"]
        # 建立資料庫連接
        with pymysql.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                c_id_query = "SELECT r_no, r_start, r_end, room_no FROM reserve WHERE c_id = %s AND r_del = FALSE ORDER BY r_no ASC"
                cursor.execute(c_id_query, (c_id,))
                results = cursor.fetchall()
                return results
    except pymysql.MySQLError as e:
        return "資料庫連接錯誤，無法查詢預約資料"
    
def now(data):
    try:  
        room = data["room"]
        with pymysql.connect(**connection_params) as connection:
            with connection.cursor() as cursor: 
                # 檢查是否為有效預約
                query = """
                SELECT 
                    CASE 
                        WHEN COUNT(*) > 0 THEN '使用中'
                        ELSE '空室'
                    END AS room_status
                FROM reserve 
                WHERE 
                    room_no = %s AND 
                    r_del = 0 AND 
                    r_start <= NOW() AND 
                    r_end >= NOW()
                """
                cursor.execute(query, (room,))
                result = cursor.fetchone()

                # 如果預約有效，再檢查預約紀錄
                if result and result['room_status'] == '使用中':
                    sign_query = """
                    SELECT * FROM sign 
                    WHERE 
                        room_no = %s AND 
                        s_in <= DATE_ADD(r_start, INTERVAL 5 MINUTE)
                    """
                    cursor.execute(sign_query, (room,))
                    sign_result = cursor.fetchone()

                    # 如果沒有在5分鐘內簽到，則轉為空室
                    if not sign_result:
                        return '空室'

                return result['room_status'] if result else '查無資料'
                
    except pymysql.MySQLError as e:
        return "資料庫連接錯誤，無法查詢預約資料"
            
            
    
    
    
 

 


    




   