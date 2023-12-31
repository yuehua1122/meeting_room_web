from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect,generate_csrf
from datetime import datetime
from markupsafe import escape
import re,os

#先設好Flask
#static_folder設置告訴Flask在哪裡查找靜態資源文件。
#static_url_path設置預設路徑
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)
app.config['SECRET_KEY'] = os.urandom(24) # 替換成一個強隨機值
csrf = CSRFProtect(app)

# 主頁
@app.route("/")
def reserve():
    return render_template("reserve.html")

# 查看預約
@app.route("/view")
def view():
    return render_template("view.html")

# 變更預約
@app.route("/modify")
def modify():
    return render_template("modify.html")

# 即時狀況
@app.route("/now")
def now():
    from connect_database import now
    message5 = now()
    table = "<table border='1'>"
    table += "<tr><th>會議室</th><th>即時狀況</th></tr>"
    for item in message5:
        table += f"<tr><td>{item['room_no']}</td><td>{item['room_status']}</td></tr>"
    table += "</table>"
    return render_template('now.html', table=table)

# 處理預約資料
@app.route("/rdata", methods=["POST"])
def rdata():
    def is_valid_c_id(c_id):
        return re.match(r'^B\d{7}$', c_id) is not None

    def is_valid_room(room):
        return re.match(r'^A\d{3}$', room) is not None

    def is_valid_date(year, month, day):
        try:
            datetime(int(year), int(month), int(day))
            return True
        except ValueError:
            return False

    def is_valid_time(hour, minute):
        return 0 <= int(hour) <= 23 and 0 <= int(minute) <= 59
    
    c_id = request.form.get("c_id")
    room = request.form.get("meetroom")
    topic = request.form.get("topic")
    start_year = request.form.get("start_year")
    start_month = request.form.get("start_month")
    start_date = request.form.get("start_date")
    start_hour = request.form.get("start_hour")
    start_minute = request.form.get("start_minute")
    end_year = request.form.get("end_year")
    end_month = request.form.get("end_month")
    end_date = request.form.get("end_date")
    end_hour = request.form.get("end_hour")
    end_minute = request.form.get("end_minute")

    if (is_valid_c_id(c_id) and
        is_valid_room(room) and
        is_valid_date(start_year, start_month, start_date) and
        is_valid_time(start_hour, start_minute) and
        is_valid_date(end_year, end_month, end_date) and
        is_valid_time(end_hour, end_minute)):
        #所有驗證通過
        
        # 建立回應資料
        response_data = {
            "c_id": c_id,
            "room": room,
            "topic": topic,
            "r_start": start_year + "-" + start_month + "-" + start_date + " " + start_hour + ":" + start_minute,
            "r_end": end_year + "-" + end_month + "-" + end_date + " " + end_hour + ":" + end_minute
        }
    
        #將資料傳送到連接資料庫的文件
        from connect_database import check
        message1 = check(response_data)
        escaped_message = escape(message1)
        return jsonify(escaped_message)
    else:
        #驗證失敗，返回錯誤
        return jsonify({"error": "Invalid input"}), 400 

@app.route("/vdata", methods=["POST"])
def vdata():
    def is_valid_date(year, month, day):
        try:
            datetime(int(year), int(month), int(day))
            return True
        except ValueError:
            return False    
    
    viewYear = request.form.get("viewYear")
    viewMonth = request.form.get("viewMonth")
    viewDate = request.form.get("viewDate")
    
    if (is_valid_date(viewYear, viewMonth, viewDate)):
        
        response_data = {
            "viewTime": viewYear + "-" + viewMonth + "-" + viewDate
        }
        from connect_database import view
        message2 = view(response_data)

        if not message2:
            return jsonify("當日無預約資料")  # 如果沒有資料，返回相應的消息
        else:
            table = "<table border='1'>"
            table += "<tr><th>預約開始時間</th><th>預約結束時間</th><th>用戶名</th><th>員工號碼</th><th>會議室</th></tr>"

            for index, item in enumerate(message2):
                row_class = "even" if index % 2 == 0 else "odd"
                table += f"<tr class='{row_class}'>"
                table += f"<td>{item['r_start']}</td><td>{item['r_end']}</td><td>{item['c_name']}</td><td>{item['c_id']}</td><td>{item['room_no']}</td>"
                table += "</tr>"

            table += "</table>"
            return jsonify(table)
    else:
        #驗證失敗，返回錯誤
        return jsonify({"error": "Invalid input"}), 400 
    

@app.route("/mdata", methods=["POST"])
def mdata():
    csrf_token = generate_csrf()
    def is_valid_m_id(m_id):
        return re.match(r'^B\d{7}$', m_id) is not None
    
    m_id = request.form.get("m_id")
    if (is_valid_m_id(m_id)):
    
        response_data = {"m_id": m_id}
        from connect_database import modify
        message3 = modify(response_data)
                
        if not message3:
            return jsonify("查無該ID的預約資料")  # 如果沒有資料，返回相應的消息
        
        table = "<table border='1'>"
        table += "<tr><th>預約開始時間</th><th>預約結束時間</th><th>會議室</th><th>操作</th></tr>"

        for item in message3:   
            table += f"<tr><td>{item['r_start']}</td><td>{item['r_end']}</td><td>{item['room_no']}</td>"
            table += f"<td><form id = 'dform' method='POST' action='/delete'>"
            table += f"<input type='hidden' name='csrf_token' value='{csrf_token}'/>"
            table += f"<input type='hidden' name='r_no' value='{item['r_no']}'>"
            table += f"<input type='hidden' name='c_id' value='{item['c_id']}'>"
            table += f"<button type='submit'>刪除</button></form></td></tr>"
                
        table += "</table>"
        return jsonify(table)
    else:
        #驗證失敗，返回錯誤
        return jsonify({"error": "Invalid input"}), 400 

@app.route('/delete', methods=['POST'])
def delete():
    def is_valid_c_id(c_id):
        return re.match(r'^B\d{7}$', c_id) is not None
    
    c_id = request.form.get("c_id")
    r_no = request.form.get("r_no")
    
    if (is_valid_c_id(c_id)): 
        
        response_data = {"r_no": r_no,"c_id": c_id}
        from connect_database import delete
        message4 = delete(response_data)
        if not message4:
            return render_template("nodata.html")  # 如果沒有資料，返回相應的消息
        
        table = "<table border='1'>"
        table += "<tr><th>預約開始時間</th><th>預約結束時間</th><th>會議室</th><th>操作</th></tr>"

        for item in message4:   
            table += f"<tr><td>{item['r_start']}</td><td>{item['r_end']}</td><td>{item['room_no']}</td>"
            table += f"<td><button type='submit'>刪除</button></td></tr>"
                
        return render_template("sucessdelete.html")
    else:
        #驗證失敗，返回錯誤
        return jsonify({"error": "Invalid input"}), 400     

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
    
    
