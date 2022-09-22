import mysql.connector
import webview

mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database = "Hospital")  
mycursor = mydb.cursor()

# DOCTOR TABLE:
# mycursor.execute("CREATE TABLE Doctor(Doc_ID int(4) primary key , Name varchar(100) not null , Department varchar(50) not null)") 

# APPOINTMENT TABLE:
# mycursor.execute("CREATE TABLE Appointments(App_ID int(4) primary key, Department varchar(30), Doctor varchar(100), Patient_Name varchar(100), Mobile_No int, Date date, Time varchar(10),Patient_Mail varchar(50))");

# USERINFO TABLE:
# mycursor.execute("CREATE TABLE UserInfo(Patient_Mail varchar(50) primary key, Password varchar(50))")

class api:  

    res_id = 0
    # LOGIN MENU:
    # PATIENT LOGIN:
    def user_menu(self,usermail,userpass):
        try:
            mycursor.execute("SELECT Password FROM UserInfo WHERE Patient_Mail = '{}'".format(usermail))
            result = mycursor.fetchall()
            if result[0][0] == userpass:
                return True
            else:
                return False
        except:
            return False
    # PATIENT REGISTER:
    def patient_register(self,patient_mail,patient_pass):
        try:
            mycursor.execute("SELECT Patient_Mail FROM UserInfo WHERE Patient_Mail = '{}'".format(patient_mail))
            result = mycursor.fetchall()
            if "@" in str(patient_mail) and ".com" in str(patient_mail):
                if len(result) == 0:
                    mycursor.execute("INSERT INTO UserInfo(Patient_Mail, Password) VALUES ('{}','{}')".format(patient_mail,patient_pass))
                    mydb.commit()
                    l = ["2"]
                    return l
                else:
                    l = ['0',"Email already exists"]
                    return l
            else:
                l = ['1',"Invalid Email"]
                return l
        except:
            return False
    # ADMIN LOGIN:
    def admin_menu(self,password):
        if password == "admin123": 
            return True
        else:
            return False


    # ADMIN MENU FUNCTIONS
    # NEW DOCTOR
    def add_doctor(self,doc_name,doc_department):
        mycursor.execute("SELECT Doc_ID FROM Doctor")
        result = mycursor.fetchall()
        if len(result) == 0:
            doc_id = 1
        else:
            doc_id = result[-1][0]+1
        mycursor.execute("INSERT INTO Doctor(Doc_ID, Name, Department) VALUES ({},'{}','{}')".format(doc_id, doc_name, doc_department))
        mydb.commit()
        return True
    # VIEW DOCTORS IN A DEPARTMENT
    def view_doctors(self,department):
        mycursor.execute("SELECT Name FROM Doctor where Department = '{}'".format(department))
        result = mycursor.fetchall()
        return list(result)
    # VIEW APPOINTMENTS OF A DOCTOR
    def view_appointments_doctor(self,doctor_name):
        html=""
        try:
            mycursor.execute("SELECT * FROM Appointments WHERE Doctor = '{}'".format(doctor_name))
            result = mycursor.fetchall()
            for i in result:
                html = html + '''<li>
                <div class = "Doctor_Column_Header">
                <div class = "Table_Column" style="flex-basis: 2%;">
                    <h3>{}</h3>
                </div>
                <div class = "Table_Column" style="flex-basis: 15%;">
                    <h3>{}</h3>
                </div>
                <div class = "Table_Column" style="flex-basis: 25%;">
                    <h3>{}</h3>
                </div>
                <div class = "Table_Column" style="flex-basis: 25%;">
                    <h3>{}</h3>
                </div>
                <div class = "Table_Column" style="flex-basis: 25%;">
                    <h3>{}</h3>
                </div>
                <div class = "Table_Column" style="flex-basis: 25%;">
                    <h3>{}</h3>
                </div>
                <div class = "Table_Column" style="flex-basis: 25%;">
                    <h3>{}</h3>
                </div>
                </div>
                </li>'''.format(i[0],i[1],i[2],i[3],i[4],i[5],i[6])
            return html
        except Exception as e:
            print(e)
    # VIEW ALL DOCTORS
    def view_all_doctors(self):
        html = ""
        mycursor.execute("SELECT * FROM Doctor")
        result = mycursor.fetchall()
        for i in result:
            html = html + '''<li>
              <div class = "Doctor_Column_Header">
                <div class = "Table_Column" style="flex-basis: 2%;">
                    <h1>{}</h1>
                </div>
                <div class = "Table_Column" style="flex-basis: 50%;">
                    <h1>{}</h1>
                </div>
                <div class = "Table_Column" style="flex-basis: 50%;">
                    <h1>{}</h1>
                </div>
                <div class = "Table_Column" style="flex-basis: 25%;">
                    <i class="fi-rr-trash" id = "{}" onclick = "remove_doc_confirm(this.id)"></i>
                </div>
            </div>
            </li>'''.format(i[0],i[1],i[2],i[0])
        return html
    # DELETE DOCTOR
    def delete_doctor(self,doc_id):
        mycursor.execute("DELETE FROM Doctor WHERE Doc_ID = {}".format(doc_id))
        mydb.commit()
        return True
    
    
    # PATIENT MENU FUNCTIONS:
    # BOOK APPOINTMENT
    def book_appointment(self,department,doctor_name,patient_name,mob_no,date,time,patient_mail):
        mycursor.execute("SELECT App_ID FROM Appointments")
        result = mycursor.fetchall()
        if len(result) == 0:
            app_id = 1
        else:
            app_id = result[-1][0]+1
        mycursor.execute("SELECT * FROM Appointments WHERE Patient_Mail = '{}'".format(patient_mail))
        result = mycursor.fetchall()
        if len(result) == 0:
            mycursor.execute("INSERT INTO Appointments(App_ID, Department, Doctor, Patient_Name, Mobile_No, Date, Time, Patient_Mail) VALUES({},'{}','{}','{}','{}','{}','{}','{}')".format(app_id,department,doctor_name,patient_name,mob_no,date,time,patient_mail))
            mydb.commit()
            return True
        else:
            l = ["1","You already have a pending appointment"]
            return l
    # VIEW DEPARTMENTS
    def view_departments(self):
        mycursor.execute("SELECT DISTINCT Department FROM Doctor")
        result = mycursor.fetchall()
        return list(result)
    # VIEW APPOINTMENTS
    def view_appointments(self,patient_mail):
        html = ""
        mycursor.execute("SELECT * FROM Appointments WHERE Patient_Mail = '{}'".format(patient_mail))
        result = mycursor.fetchall()
        if len(result) != 0:
            for i in result:
                dte = str(i[5])
                dte = dte.split("-")
                dte = str(dte[2]+"-"+dte[1]+"-"+dte[0])
                html = html + '''<div class="card">
                    <div class="card-top">{}</div>
                    <div class="card-bottom">
                    <br><br>
                    <h3>Appointment ID: {}</h3>
                    <br><br>
                    <h3>Department: {}</h3>
                    <br><br>
                    <h3>Doctor: {}</h3>
                    <br><br>
                    <h3>Date: {}</h3>
                    <br><br>
                    <h3>Time: {}</h3>
                    <br><br>
                    
                    <button class="card-btn" onclick="res_app();">RESCHEDULE APPOINTMENT</button>
                    <button class="card-btn" onclick="cancel_app();">CANCEL APPOINTMENT</button>
                    </div>
                
                </div>
                '''.format(i[3],i[0],i[1],i[2],dte,i[6])
                global res_id
                res_id = i[0]
            return html
        else:
            l = ["1","You have no appointments"]
            return l
    # RESCHEDULE APPOINTMENT
    def reschedule_appointment(self,date,time):
        global res_id
        mycursor.execute("UPDATE Appointments SET Date = '{}', Time = '{}' WHERE App_ID = {}".format(date,time,res_id))
        mydb.commit()
    # CANCEL APPOINTMENT
    def cancel_appointment(self):
        global res_id
        mycursor.execute("DELETE FROM Appointments WHERE App_ID = {}".format(res_id))
        mydb.commit()

api = api()
with open("Hospital.html", "r") as f:
    try:
        r = f.read()
        webview.create_window(title='Medlife Healthcare', html=r, js_api=api)
        webview.start(debug=True)
    except Exception as E:
        print(E)
