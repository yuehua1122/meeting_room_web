# connect_database.py
import pymysql
from mysql.connector.constants import ClientFlag
# 資料庫參數設定

#connection_params = {
#    "host='kuramysql.mysql.database.azure.com',
#    "port="3306",
#    user="kura",
#    password="Kevinbear60404",
#    db="kruadb",
#    ssl={"ca","C:/Users/user/Desktop/專題/沙崙資安競賽/meeting room web/web/DigiCertGlobalRootCA.crt.pem"},
#    ={'ca': '/path/to/ca-file'})
#    "charset": "utf8mb4",
#    "cursorclass": pymysql.cursors.DictCursor
#}


connection_params = {
    'user': 'kura',
    'password': 'Kevinbear60404',
    'host': 'kuramysql.mysql.database.azure.com',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'C:/Users/user/Desktop/DigiCertGlobalRootCA.crt.pem',
}


import pymysql

def check(data):
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
                    (r_start <= %s AND r_end >= %s) OR 
                    (r_start >= %s AND r_end <= %s)
                )
                """
                cursor.execute(check_time_and_room_sql, (room, r_start, r_start, r_end, r_end, r_start, r_end))
                if cursor.rowcount > 0:
                    return "預約失敗，會議室已被預定!"

                # 插入預約
                insert_sql = "INSERT INTO reserve (`r_start`, `r_end`, `c_id`,`room_no`) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_sql, (r_start, r_end, c_id, room))
                successful_message = "預約成功!&" + "預約ID : " + c_id + "&會議室 : " + room + "&從 " + r_start + " 到 " + r_end 
            connection.commit()
        return successful_message
    

def view(data):
        viewTime = data["viewTime"]            

        # 建立資料庫連接
        with pymysql.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                view_time_query = "SELECT * FROM reserve WHERE (DATE(r_start) <= %s AND DATE(r_end) >= %s) ORDER BY r_no ASC"
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
    



   