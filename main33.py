from flask import Flask,render_template,request,flash,redirect,make_response,session,url_for,jsonify,json
from flask_mail import Mail,Message
import pdfkit
import mysql.connector
app=Flask(__name__)
config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'database': 'clinictest'
}
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'stassbooking@gmail.com'
app.config['MAIL_PASSWORD'] = 'dbfpwaqwwjiauout'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)
app.secret_key = 'many random bytes'

'''@app.route('/')
def hi():
    return render_template('hi.html')'''
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/ClinicLogin')
def cLogIn():
    return render_template('page-2.html')

@app.route('/about')
def about():
    return render_template('about2.html')

@app.route('/ClinicRegistration')
def cReg():
    return render_template('page-1.html')

@app.route('/clinicRegistrationProcess',methods=['POST','GET'])
def cRegPro():
    if request.method =='POST':
            signup=request.form
            print(signup)
            emailID=signup['emailID']
            clinicName=signup['clinicName']
            clinicPass=signup['clinicPass']
            mydb=mysql.connector.connect(**config)
            mycursor=mydb.cursor()
            mycursor.execute("select * from clinic")
            testl=mycursor.fetchall()
            t=1
            for i in testl:
                if i[1]==emailID:
                    t=0
                    break
            mydb.commit()
            mycursor.close()
            mydb.close()
            if t==0:
                flash("The emailID is already taken,PLease use a different emailID","warning")
                return redirect('/ClinicRegistration')
            if not len(clinicPass)>=5:
                flash("password must be atleast 5 characters","warning")
                return redirect('/ClinicRegistration')
            else:
                #hashed=bcrypt.hashpw(birthdate.enconde('utf-8'),bcrypt.gensalt())
                #mycursor.execute("insert into dob(name,birthdate,hash) values(%s,%s,%s)",(name,birthdate,hashed))
                mydb=mysql.connector.connect(**config)
                mycursor=mydb.cursor()
                mycursor.execute("insert into clinic(emailID,clinicName,clinicPass) values(%s,%s,%s)",(emailID,clinicName,clinicPass))
                mydb.commit()
                mycursor.close()
                mydb.close()
                mail.send_message('clinicRegistrationProcess',sender='stassbooking@gmail.com',recipients=[emailID],body="Thanks for registering your clinic."+"From now your clinic is a registered clinic in our system."+"With the help of our System you can able to manage the patient booking information"+"We hope that you will like our booking management system"+"\n"+"Regards From"+"\n"+"STASS TEAM"+"\n"+"stassbooking@gmail.com")
                flash("Registered successfully ,Please login to go to dashboard","success")
                return redirect('/ClinicLogin')

@app.route('/resetPassword')
def rPass():
    return render_template('resetPassword.html')

@app.route('/resetPass',methods=['POST','GET'])
def rPass1():
    if request.method =='POST':
            signup=request.form
            print(signup)
            emailID=signup['emailID']
            mydb=mysql.connector.connect(**config)
            mycursor=mydb.cursor()
            mycursor.execute("""select clinicID FROM clinic WHERE emailID LIKE '{}'""".format(emailID))
            val=mycursor.fetchall()
            print(val)
            id1=val[0][0]
            print(id1)
            mydb.commit()
            mycursor.close()
            mydb.close()
            msg = Message('Password Reset',sender='stassbooking@gmail.com',recipients=[emailID])
            msg.body = "testing"
            msg.html = render_template('pass-reset-3.html',id1=id1)
            mail.send(msg)
            #mail.send_message('Password Reset',sender='stassbooking@gmail.com',recipients=[emailID],body="Click on below link to reset your password"+"\n"+"<a href="/setThepass/{{id1}}">Click-Here-To-Reset-Your-Pass</a>"+"\n"+"Regards From"+"\n"+"STASS TEAM"+"\n"+"stassbooking@gmail.com")
            return 'password reset link has been send to email'
 
@app.route('/setThepass/<id1>',methods=['POST','GET'])
def rPass2(id1):
    id1=id1
    if request.method =='POST':
        reset=request.form
        newPassword=reset['newPassword']
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        sql="update clinic set clinicPass=%s where clinicID=%s"
        mycursor.execute(sql,[newPassword,id1])
        mydb.commit()
        mycursor.close()
        mydb.close()
        flash("password updated successfully","success")
        return redirect('/ClinicLogin')
    return render_template('resetPassword1.html',id1=id1)

@app.route('/dashboard$',methods=['POST','GET'])
def dashboard():
        if request.method=='POST':
          session['emailID']=request.form['emailID']
          #session['clinicName']=request.form['clinicName']
          #username=request.form['Username']
          session['clinicPass']=request.form['clinicPass']
          #passw=request.form['Password']
          #print(session['username'])
          mydb=mysql.connector.connect(**config)
          mycursor=mydb.cursor()
          sql="SELECT * FROM clinic WHERE emailID= %s AND clinicPass= %s"
          #params=(username,passw)
          params=(session['emailID'],session['clinicPass'])
          mycursor.execute(sql,params)
          val=mycursor.fetchall()
         
          idVal=0
          mycursor.close()
          mydb.close()
          if(len(val)!=0):
            #msg=session['clinicName']
            idVal=val[0][0]
            msg=val[0][2]
            return render_template('dashboard.html',name=msg,val=idVal)
          else:
            flash("Wrong password","danger")
            return redirect('/ClinicLogin')

@app.route('/dashboard/<id>')
def dashboard1(id):
    if 'emailID' in session:
        #msg=session['clinicName']
        emailID=session['emailID']
        clinicPass=session['clinicPass']
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        sql="SELECT * FROM clinic WHERE emailID= %s AND clinicPass= %s"
        #params=(username,passw)
        params=(emailID,clinicPass)
        mycursor.execute(sql,params)
        val=mycursor.fetchall()
        print(val)
        idVal=val[0][0]
        msg=val[0][2]
        print(idVal)
        mycursor.close()
        mydb.close()
        return render_template('dashboard.html',name=msg,val=idVal)
    else:
        flash("Please Login To Access Dashboard","warning")
        return redirect('/ClinicLogin')
    return render_template('dashboard.html')
@app.route('/logout')
def logout():
    session.pop('emailID', None)
    flash("Logged out successfully","success")
    return redirect('/ClinicLogin')

#### For Patient check  ####

@app.route('/pcheck/<id>')
def pcheck(id):
    if 'emailID' in session:
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        mycursor.execute("""select * FROM patient WHERE clinicID LIKE '{}'""".format(id))
        data1=mycursor.fetchall()
        id1=id
        print(data1)
        if(len(data1)==0):
          flash("No entries yet","no-entries-pa")
          return render_template('pcheck1.html',val=id1)
        if(len(data1)!=0):
          return render_template('pcheck1.html',data1=data1,val=id1)
        mycursor.close()
        mydb.close()
    else:
        flash("Please Login To Access Dashboard","warning")
        return redirect('/ClinicLogin')

@app.route('/pnewEntry/<id1>', methods=['POST','GET'])
def pnewEntry(id1):
  if(request.method =='POST'):
    data=request.form
    clinicID=id1
    patientName=data['patientName']
    patientMobile=data['patientMobile']
    doctorName=data['doctorName']
    specialization=data['specialization']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    mycursor.execute("insert into patient(clinicID,patientName,patientMobile,doctorName,specialization) values(%s,%s,%s,%s,%s)",(clinicID,patientName,patientMobile,doctorName,specialization))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return redirect(url_for('pcheck',id=clinicID))

@app.route("/pupdate/<id>/<rid>",methods=['GET','POST'])
def pupdate(id,rid):
  mydb=mysql.connector.connect(**config)
  id1=id
  rid1=rid
  if(request.method =='POST'):
    data=request.form
    patientName=data['patientName']
    patientMobile=data['patientMobile']
    doctorName=data['doctorName']
    specialization=data['specialization']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    sql="update patient set doctorName=%s,specialization=%s,patientName=%s,patientMobile=%s where clinicID=%s and patientID=%s"
    mycursor.execute(sql,[doctorName,specialization,patientName,patientMobile,id1,rid1])
    mydb.commit()
    mycursor.close()
    mydb.close()
    flash("entries updated","entries-mssg")
    return redirect(url_for('pcheck',id=id1))
  #mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  #mycursor.execute("""SELECT * Doctor WHERE id LIKE '{}'""".format(id))
  sql="select * from patient where clinicID=%s and patientID=%s"
  mycursor.execute(sql,[id1,rid1])
  datas=mycursor.fetchall()
  #print(datas)
  mycursor.close()
  mydb.close()
  return render_template('pupdate.html',datas=datas)

@app.route("/pdelete/<id>/<rid>",methods=['GET','POST'])
def pdelete(id,rid):
  #data=request.form
  #ID=data['ID']
  #print(data)
  id1=id
  rid1=rid
  mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  mycursor.execute("""DELETE FROM patient WHERE clinicID LIKE '{}' AND patientID LIKE '{}'""".format(id1,rid1))
  mydb.commit()
  mycursor.close()
  mydb.close()
  return redirect(url_for('pcheck',id=id1))

##for doctor database#########

@app.route('/dcheck/<id>')
def dcheck(id):
    #mycursor.execute("SELECT * FROM doctor")
    #data=mycursor.fetchall()
    #mycursor.execute("SELECT * FROM patient")
    #data1=mycursor.fetchall()
    #return render_template('check.html',data=data,data1=data1)
    if 'emailID' in session:
        #msg=session['username']
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        mycursor.execute("""select clinicID,doctorID,doctorName,specialization,DOB,phoneNo,emailID,time,day FROM doctor WHERE clinicID LIKE '{}'""".format(id))
        data=mycursor.fetchall()
        id1=id
        print(data)
        #mycursor.execute("SELECT * FROM patient")
        #data1=mycursor.fetchall()
        print(id1)
        if(len(data)==0):
          flash("No entries yet","no-entries")
          return render_template('dcheck1.html',val=id1)
        '''if(len(data1)==0):
          flash("No entries yet","no-entries-pa")
          return render_template('dcheck.html')'''
        if(len(data)!=0):
          return render_template('dcheck1.html',data=data,val=id1)
        '''if(len(data1)!=0):
          return render_template('check.html',data1=data1)'''
        mycursor.close()
        mydb.close()
    else:
        flash("Please Login To Access Dashboard","warning")
        return redirect('/ClinicLogin')

@app.route('/newEntry/<id1>', methods=['POST','GET'])
def newEntry(id1):
  if(request.method =='POST'):
    data=request.form
    clinicID=id1
    print(clinicID)
    #doctorID=data['doctorID']
    doctorName=data['doctorName']
    specialization=data['specialization']
    DOB=data['DOB']
    phoneNo=data['phoneNo']
    emailID=data['emailID']
    time=data['time']
    day=data['day']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    mycursor.execute("insert into doctor(clinicID,doctorName,specialization,DOB,phoneNo,emailID,time,day) values(%s,%s,%s,%s,%s,%s,%s,%s)",(clinicID,doctorName,specialization,DOB,phoneNo,emailID,time,day))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return redirect(url_for('dcheck',id=id1))

@app.route("/dupdate/<id>/<rid>",methods=['GET','POST'])
def dupdate(id,rid):
  mydb=mysql.connector.connect(**config)
  id1=id
  rid1=rid
  role=0
  if(request.method =='POST'):
    data=request.form
    doctorName=data['doctorName']
    specialization=data['specialization']
    DOB=data['DOB']
    phoneNo=data['phoneNo']
    emailID=data['emailID']
    time=data['time']
    day=data['day']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    sql="update doctor set doctorName=%s,specialization=%s,DOB=%s,phoneNo=%s,emailID=%s,time=%s,day=%s where clinicID=%s and doctorID=%s"
    mycursor.execute(sql,[doctorName,specialization,DOB,phoneNo,emailID,time,day,id1,rid1])
    mydb.commit()
    mycursor.close()
    mydb.close()
    flash("entries updated","entries-mssg")
    return redirect(url_for('dcheck',id=id1))
  #mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  #mycursor.execute("""SELECT * Doctor WHERE id LIKE '{}'""".format(id))
  sql="select * from doctor where clinicID=%s and doctorID=%s"
  mycursor.execute(sql,[id1,rid1])
  datas=mycursor.fetchall()
  print(datas)
  mycursor.close()
  mydb.close()
  return render_template('dupdate.html',datas=datas,role=role,id1=id1)

@app.route("/ddelete/<id>/<rid>",methods=['GET','POST'])
def ddelete(id,rid):
  #data=request.form
  #ID=data['ID']
  #print(data)
  id1=id
  rid1=rid
  mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  mycursor.execute("""DELETE FROM doctor WHERE clinicID LIKE '{}' AND doctorID LIKE '{}'""".format(id1,rid1))
  mydb.commit()
  mycursor.close()
  mydb.close()
  return redirect(url_for('dcheck',id=id1))

@app.route('/newE/<id1>')
def neE(id1):
    c=id1
    return c

@app.route('/booking')
def booki():
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    mycursor.execute("SELECT * FROM clinic ORDER BY clinicID")
    clinical = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    #print(clinical)
    return render_template('book.html', clinical=clinical)
@app.route("/clinic",methods=["POST","GET"])
def clinic():  
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    if request.method == 'POST':
        clinic_id = request.form['clinic_id']
        #print(clinic_id)
        mycursor.execute("SELECT DISTINCT doctorName,specialization from doctor where clinicID=(SELECT clinicID from clinic WHERE clinicName = %s)", [clinic_id])
        special = mycursor.fetchall()
        #print(special)
        OutputArray = []
        for row in special:
            outputObj = {
                'id': row[0],
                'name': row[1]}
            OutputArray.append(outputObj)
        #print(OutputArray)
    return jsonify(OutputArray)

'''c=1
s2=""
for i in str:
    if(i=='('):
        s1=str[c:-1]
        break
    s2=s2+i
    c=c+1
print(s1)
print(s2)'''

@app.route("/bookingProcessing" ,methods=["POST","GET"])
def bookingP():
        if request.method =='POST':
            book=request.form
            clinicname=book['clinicname']
            #sp=book['clinic_id']
            speciality=book['speciality']
            #print(clinicname)
            print(book)
            #speciality='dfg(eye)'
            patientN=book['patientN']
            patientM=book['patientM']
            if len(clinicname)== 0:
                flash("Please select a clinic from the drop down","warning")
                return redirect('/booking')
            if len(speciality)== 0:
                flash("Please select a doctor with specialization from the drop down","warning")
                return redirect('/booking')
            if len(patientN)== 0:
                flash("please enter the name","warning")
                return redirect('/booking')
            if len(patientM)!= 10:
                flash("please enter a valid phone number","warning")
                return redirect('/booking')
            c=1
            #print("ok")
            doctor=""
            for ind in speciality:
                if(ind=='('):
                    specialization=speciality[c:-1]
                    break
                doctor=doctor+ind
                c=c+1
            #doctor=doctor.split()
            #specialization=specialization.split()
            print(doctor)
            print(specialization)
            mydb=mysql.connector.connect(**config)
            mycursor=mydb.cursor()
            mycursor.execute("""SELECT clinicID from clinic where clinicName LIKE '{}'""".format(clinicname))
            clinic_id=mycursor.fetchall()
            clinic_id=clinic_id[0][0]
            print(clinic_id)
            mycursor.execute("insert into patient(clinicID,patientName,patientMobile,doctorName,specialization) values(%s,%s,%s,%s,%s)",(clinic_id,patientN,patientM,doctor,specialization))
            mydb.commit()
            #flash("booking Confirmed","success")
            #mycursor.execute("SELECT id,Doname,specialization,patientN,patientM FROM WHERE patientN = %s and patientM = %s",)
            mycursor.execute("""SELECT max(patientID) from patient WHERE patientName LIKE '{}' AND patientMobile LIKE '{}'""".format(patientN,patientM))
            pid=mycursor.fetchall()
            pid=pid[0][0]
            #mycursor.execute("""SELECT clinicID,patientID,patientName,patientMobile,doctorName,specialization FROM patient WHERE clinicID LIKE '{}' AND patientName LIKE '{}' AND patientMobile LIKE '{}'""".format(clinic_id,patientN,patientM))
            mycursor.execute("""SELECT clinicID,patientID,patientName,patientMobile,doctorName,specialization FROM patient WHERE patientID LIKE '{}'""".format(pid))

            patient=mycursor.fetchall()
            
            #print(patient)
            clinicID=patient[0][0]
            Id=patient[0][1]
            #print(Id)
            Doname=patient[0][4]
            #print(Doname)
            specialization=patient[0][5]
            #print(specialization)
            patientN=patient[0][2]
            #print(patientN)
            patientM=patient[0][3]
            mycursor.execute("""SELECT clinicName FROM clinic WHERE clinicID LIKE '{}'""".format(clinicID))
            clinicName=mycursor.fetchall();
            clinicName=clinicName[0][0]
            mycursor.close()
            mydb.close()
            #print(patientM)
            html=render_template('pdfGenerate2.html',clinicID=clinicID,Id=Id,Doname=Doname,specialization=specialization,patientN=patientN,patientM=patientM,clinicName=clinicName)
            pdf=pdfkit.from_string(html, False)
            response=make_response(pdf)
            response.headers["Content-Type"]="application/pdf"
            response.headers["Content-Disposition"]="inline; filename=output.pdf"
            return response

####----Admin Section-----

@app.route("/adminlogin$2345cool")
def adminLogin():
        return render_template('AlogIn.html')   

@app.route("/dashboard%$2_Admin" ,methods=["POST","GET"])
def adminLoginvalidation():
        if request.method=='POST':
          session['adName']=request.form['adName']
          session['adPass']=request.form['adPass']
          mydb=mysql.connector.connect(**config)
          mycursor=mydb.cursor()
          sql="SELECT * FROM admin WHERE adName= %s AND adPass= %s"
          params=(session['adName'],session['adPass'])
          mycursor.execute(sql,params)
          val=mycursor.fetchall()
         
          idVal=0
          mycursor.close()
          mydb.close()
          if(len(val)!=0):
            #msg=session['clinicName']
            idVal=val[0][0]
            msg=val[0][1]
            return render_template('dashboardAdmin.html',name=msg,val=idVal)
          else:
            flash("Wrong password","danger")
            return redirect('/adminlogin$2345cool')

@app.route('/dashboard%$1_Admin')
def adminLoginvalidation1():
    if 'adName' in session:
          adName=session['adName']
          adPass=session['adPass']
          mydb=mysql.connector.connect(**config)
          mycursor=mydb.cursor()
          sql="SELECT * FROM admin WHERE adName= %s AND adPass= %s"
          params=(adName,adPass)
          mycursor.execute(sql,params)
          val=mycursor.fetchall()
         
          idVal=0
          mycursor.close()
          mydb.close()
          if(len(val)!=0):
            #msg=session['clinicName']
            idVal=val[0][0]
            msg=val[0][1]
            return render_template('dashboardAdmin.html',name=msg,val=idVal)
          else:
            flash("Wrong password","danger")
            return redirect('/adminlogin$2345cool')
    else:
        flash("Please Login To Access Dashboard","warning")
        return redirect('/adminlogin$2345cool')

@app.route('/logoutAdmin')
def logoutAdmin():
    session.pop('adName', None)
    flash("Logged out successfully","success")
    return redirect('/adminlogin$2345cool')

@app.route('/adclinic')
def adClinic():
    #mycursor.execute("SELECT * FROM doctor")
    #data=mycursor.fetchall()
    #mycursor.execute("SELECT * FROM patient")
    #data1=mycursor.fetchall()
    #return render_template('check.html',data=data,data1=data1)
    if 'adName' in session:
        #msg=session['username']
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        mycursor.execute("""select * FROM clinic""")
        data=mycursor.fetchall()
        print(data)
        #mycursor.execute("SELECT * FROM patient")
        #data1=mycursor.fetchall()
        if(len(data)==0):
          flash("No entries yet","no-entries")
          return render_template('adClinic.html')
        '''if(len(data1)==0):
          flash("No entries yet","no-entries-pa")
          return render_template('dcheck.html')'''
        if(len(data)!=0):
          return render_template('adClinic.html',data=data)
        '''if(len(data1)!=0):
          return render_template('check.html',data1=data1)'''
        mycursor.close()
        mydb.close()
    else:
        flash("Please Login To Access Dashboard","warning")
        return redirect('/adminlogin$2345cool')

@app.route('/newEntryadminclinic', methods=['POST','GET'])
def newEntryAdClinic():
  if(request.method =='POST'):
    data=request.form
    #clinicID=data['clinicID']
    emailID=data['emailID']
    clinicName=data['clinicName']
    clinicPass=data['clinicPass']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    mycursor.execute("insert into clinic(emailID,clinicName,clinicPass) values(%s,%s,%s)",(emailID,clinicName,clinicPass))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return redirect(url_for('adClinic'))

@app.route("/adclinicupdate/<id>",methods=['GET','POST'])
def adclinicupdate(id):
  mydb=mysql.connector.connect(**config)
  id1=id
  if(request.method =='POST'):
    data=request.form
    emailID=data['emailID']
    clinicName=data['clinicName']
    clinicPass=data['clinicPass']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    sql="update clinic set clinicName=%s,emailID=%s,clinicPass=%s where clinicID=%s"
    mycursor.execute(sql,[clinicName,emailID,clinicPass,id1])
    mydb.commit()
    mycursor.close()
    mydb.close()
    flash("entries updated","entries-mssg")
    return redirect(url_for('adClinic'))
  #mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  #mycursor.execute("""SELECT * Doctor WHERE id LIKE '{}'""".format(id))
  sql="select * from clinic where clinicID=%s"
  mycursor.execute(sql,[id1])
  datas=mycursor.fetchall()
  print(datas)
  mycursor.close()
  mydb.close()
  return render_template('adClinicupdate.html',datas=datas)

@app.route("/adclinicdelete/<id>",methods=['GET','POST'])
def adclinicdelete(id):
  #data=request.form
  #ID=data['ID']
  #print(data)
  id1=id
  mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  mycursor.execute("""DELETE FROM clinic WHERE clinicID LIKE '{}'""".format(id1))
  mydb.commit()
  mycursor.close()
  mydb.close()
  return redirect(url_for('adClinic'))

#-----Admin Doctor side---
'''@app.route('/addoctor')
def adDoctor():
    #mycursor.execute("SELECT * FROM doctor")
    #data=mycursor.fetchall()
    #mycursor.execute("SELECT * FROM patient")
    #data1=mycursor.fetchall()
    #return render_template('check.html',data=data,data1=data1)
    if 'adName' in session:
        #msg=session['username']
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        mycursor.execute("""select clinicID,doctorID,doctorName,specialization,DOB,phoneNo,emailID,time,day FROM doctor""")
        data=mycursor.fetchall()
        print(data)
        #mycursor.execute("SELECT * FROM patient")
        #data1=mycursor.fetchall()
        if(len(data)==0):
          flash("No entries yet","no-entries")
          return render_template('adDoctor1.html')
        if(len(data)!=0):
          return render_template('adDoctor1.html',data=data)
        mycursor.close()
        mydb.close()
    else:
        flash("Please Login To Access Dashboard","warning")
        return redirect('/adminlogin$2345cool')'''

@app.route('/addoctor',methods=['GET','POST'])
def adDoctor():
    #mycursor.execute("SELECT * FROM doctor")
    #data=mycursor.fetchall()
    #mycursor.execute("SELECT * FROM patient")
    #data1=mycursor.fetchall()
    #return render_template('check.html',data=data,data1=data1)
    if request.method=='POST':
        data=request.form
        clinicID=data['clinicID']
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        mycursor.execute("""select clinicID,doctorID,doctorName,specialization,DOB,phoneNo,emailID,time,day FROM doctor WHERE clinicID LIKE '{}'""".format(clinicID))
        data=mycursor.fetchall()
        if(len(data)==0):
          flash("No entries yet","no-entries")
          return render_template('adDoctor1.html')
        if(len(data)!=0):
          return render_template('adDoctor1.html',data=data)
        mycursor.close()
        mydb.close()
    else:
        if 'adName' in session:
            #msg=session['username']
            mydb=mysql.connector.connect(**config)
            mycursor=mydb.cursor()
            mycursor.execute("""select clinicID,doctorID,doctorName,specialization,DOB,phoneNo,emailID,time,day FROM doctor""")
            data=mycursor.fetchall()
            print(data)
            #mycursor.execute("SELECT * FROM patient")
            #data1=mycursor.fetchall()
            if(len(data)==0):
                flash("No entries yet","no-entries")
                return render_template('adDoctor1.html')
            if(len(data)!=0):
                return render_template('adDoctor1.html',data=data)
            mycursor.close()
            mydb.close()
        else:
            flash("Please Login To Access Dashboard","warning")
            return redirect('/adminlogin$2345cool')

@app.route("/adddelete/<id>",methods=['GET','POST'])
def adddelete(id):
  #data=request.form
  #ID=data['ID']
  #print(data)
  id1=id
  mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  mycursor.execute("""DELETE FROM doctor WHERE doctorID LIKE '{}'""".format(id1))
  mydb.commit()
  mycursor.close()
  mydb.close()
  return redirect(url_for('adDoctor'))

@app.route("/addupdate/<id>",methods=['GET','POST'])
def addupdate(id):
  mydb=mysql.connector.connect(**config)
  id1=id
  role=1
  if(request.method =='POST'):
    data=request.form
    doctorName=data['doctorName']
    specialization=data['specialization']
    DOB=data['DOB']
    phoneNo=data['phoneNo']
    emailID=data['emailID']
    time=data['time']
    day=data['day']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    sql="update doctor set doctorName=%s,specialization=%s,DOB=%s,phoneNo=%s,emailID=%s,time=%s,day=%s where doctorID=%s"
    mycursor.execute(sql,[doctorName,specialization,DOB,phoneNo,emailID,time,day,id1])
    mydb.commit()
    mycursor.close()
    mydb.close()
    flash("entries updated","entries-mssg")
    return redirect(url_for('adDoctor'))
  #mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  #mycursor.execute("""SELECT * Doctor WHERE id LIKE '{}'""".format(id))
  #sql="select doctorID,doctorName,specialization,DOB,phoneNo,emailID,time,day from doctor where doctorID=%s"
  sql="select * from doctor where doctorID=%s"
  mycursor.execute(sql,[id1])
  datas=mycursor.fetchall()
  print(datas)
  mycursor.close()
  mydb.close()
  return render_template('dupdate.html',datas=datas,role=role)

@app.route('/newEntryadmindoctor', methods=['POST','GET'])
def newEntryAdDoctor():
  if(request.method =='POST'):
    data=request.form
    #clinicID=data['clinicID']
    doctorName=data['doctorName']
    specialization=data['specialization']
    DOB=data['DOB']
    phoneNo=data['phoneNo']
    emailID=data['emailID']
    time=data['time']
    day=data['day']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    mycursor.execute("insert into doctor(doctorName,specialization,DOB,phoneNo,emailID,time,day) values(%s,%s,%s,%s,%s,%s,%s)",(doctorName,specialization,DOB,phoneNo,emailID,time,day))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return redirect(url_for('adDoctor'))

#-------Admin Patient-------

@app.route('/adpatient',methods=['GET','POST'])
def adPatient():
    if request.method=='POST':
        data=request.form
        clinicID=data['clinicID']
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        mycursor.execute("""select * FROM patient WHERE clinicID LIKE '{}'""".format(clinicID))
        data1=mycursor.fetchall()
        if(len(data)==0):
          flash("No entries yet","no-entries")
          return render_template('adPatient.html')
        if(len(data)!=0):
          return render_template('adPatient.html',data1=data1)
        mycursor.close()
        mydb.close()
    else:
        if 'adName' in session:
            mydb=mysql.connector.connect(**config)
            mycursor=mydb.cursor()
            mycursor.execute("""select * FROM patient""")
            data1=mycursor.fetchall()
            if(len(data1)==0):
                flash("No entries yet","no-entries-pa")
                return render_template('adPatient.html')
            if(len(data1)!=0):
                return render_template('adPatient.html',data1=data1)
            mycursor.close()
            mydb.close()
        else:
            flash("Please Login To Access Dashboard","warning")
            return redirect('/adminlogin$2345cool')

@app.route("/adpdelete/<id>",methods=['GET','POST'])
def adpdelete(id):
  #data=request.form
  #ID=data['ID']
  #print(data)
  id1=id
  mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  mycursor.execute("""DELETE FROM patient WHERE patientID LIKE '{}'""".format(id1))
  mydb.commit()
  mycursor.close()
  mydb.close()
  return redirect(url_for('adPatient'))

@app.route("/adpupdate/<id>",methods=['GET','POST'])
def adpupdate(id):
  mydb=mysql.connector.connect(**config)
  id1=id
  role=1
  if(request.method =='POST'):
    data=request.form
    patientName=data['patientName']
    patientMobile=data['patientMobile']
    doctorName=data['doctorName']
    specialization=data['specialization']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    sql="update patient set doctorName=%s,specialization=%s,patientName=%s,patientMobile=%s where patientID=%s"
    mycursor.execute(sql,[doctorName,specialization,patientName,patientMobile,id1])
    mydb.commit()
    mycursor.close()
    mydb.close()
    flash("entries updated","entries-mssg")
    return redirect(url_for('adPatient'))
  #mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  #mycursor.execute("""SELECT * Doctor WHERE id LIKE '{}'""".format(id))
  sql="select * from patient where patientID=%s"
  mycursor.execute(sql,[id1])
  datas=mycursor.fetchall()
  #print(datas)
  mycursor.close()
  mydb.close()
  return render_template('pupdate.html',datas=datas,role=role)

@app.route('/newEntryadminpatient', methods=['POST','GET'])
def newEntryAdPatient():
  if(request.method =='POST'):
    data=request.form
    #clinicID=data['clinicID']
    patientName=data['patientName']
    patientMobile=data['patientMobile']
    doctorName=data['doctorName']
    specialization=data['specialization']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    mycursor.execute("insert into patient(patientName,patientMobile,doctorName,specialization) values(%s,%s,%s,%s)",(patientName,patientMobile,doctorName,specialization))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return redirect(url_for('adPatient'))

#----contact Us----
@app.route('/contacts')
def contacts():
  return render_template('contacts2.html')
@app.route("/inform", methods=['POST', 'GET'])
def inform():
    if request.method == "POST":
        name = request.form["name"]
        email =request.form["email"] 
        number=request.form["number"]
        message = request.form["message"]
        print(name)
    #msg = Message(sub, sender='stassbooking@gmail.com', recipients=['sayantan.bose286@gmail.com'])
    #msg.body = maill
    mail.send_message('Notification From Client',sender='stassbooking@gmail.com',recipients=['stassbooking@gmail.com'],body=message+"\n" + name+ "\n" + "Email : "+ email +"\n" + "Phone No.:"+ number)
    mail.send_message('Notification',sender='stassbooking@gmail.com',recipients=[email],body="We will contact you soon!"+"\n"+"Regards From"+"\n"+"STASS TEAM")
    #return "<h1>Thanks For Contacting Us!<h1><h2>We will Communicate You Soon<h2>"
    return render_template('thanks32.html')

@app.route("/checkDetails")
def checkDetailsP():
   mydb=mysql.connector.connect(**config)
   mycursor=mydb.cursor()
   mycursor.execute("""select clinicID,clinicName FROM clinic""")
   data=mycursor.fetchall()
   mydb.commit()
   mycursor.close()
   mydb.close()
   return render_template('checkdetails.html',data=data)

@app.route("/checkDetails",methods=['POST','GET'])
def checkDetails():
   '''mydb=mysql.connector.connect(**config)
   mycursor=mydb.cursor()
   mycursor.execute("""select clinicID,clinicName FROM clinic""")
   data=mycursor.fetchall()
   mydb.commit()
   mycursor.close()
   mydb.close()
   return render_template('checkdetails.html',data=data)'''
   if request.method=='POST':
        print('hi')
        data12=request.form
        clinicID=data12['clinicID']
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        mycursor.execute("""select clinicID,doctorName,specialization,time,day FROM doctor WHERE clinicID LIKE '{}'""".format(clinicID))
        data1=mycursor.fetchall()
        mycursor.execute("""select clinicID,clinicName FROM clinic""")
        data=mycursor.fetchall()
        print(data1)
        if(len(data1)==0):
          flash("No entries yet","entries-mssg")
          return render_template('checkdetails.html',data=data)
        if(len(data1)!=0):
          return render_template('checkdetails.html',data1=data1,data=data)
        '''if(len(data)==0):
          flash("No entries yet","no-entries")
          return render_template('checkdetails.html')
        if(len(data)!=0):
          return render_template('checkdetails.html',data=data)'''
        mycursor.close()
        mydb.close()
        


@app.errorhandler(404)
def page_not_f(e):
        return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server(e):
        return render_template('500.html'), 500

if __name__ == '__main__':
   app.run(debug=True,host='127.0.0.1',port='8081')
