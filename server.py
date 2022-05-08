import os
import base64 
import io  
import PIL
from PIL import Image
from MySQLdb import connections
from django.shortcuts import render
from flask import Flask,send_file, render_template,send_file,url_for,redirect,flash, request, redirect,session
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_login import login_required
from flask_login import LoginManager
from flask_login import *
from datetime import *

app=Flask(__name__,template_folder='template')
app.secret_key="key"
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="servetoexcel"
mysql=MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)

		
@app.route('/')
def index():
  return render_template('patients/index.html')

@app.route('/userlogin',methods=['POST','GET'])
def userlogin():
    message="Please fill the login "
    if request.method=='POST':
        useremail=request.form['u_email']
        userpassword=request.form['u_psw']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE usermail = %s AND userpass = %s', (useremail, userpassword))
        user=cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['u_psw'] = user['userpass']
            session['u_email'] = user['usermail']
            session['u_name'] = user['username']
            return redirect(url_for('main'))
        else:
            # Account doesnt exist or username/password incorrect
             message = 'Incorrect username/password!'
    return render_template('/patients/login.html', message='')
   
    
@app.route('/userregistration',methods=['POST','GET'])
def userregistration():
    msg = ''
    if request.method == 'POST':
        username = request.form['u_name']
        usermail = request.form['u_email']
        userpassword = request.form['u_psw']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE usermail = %s', (usermail,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', usermail):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not userpassword or not usermail:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (%s, %s, %s)', (username, usermail, userpassword))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            #after successfully inserted redirect to loginpage
            return render_template('/patients/login.html') 
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('/patients/signup.htm', msg=msg)


@app.route('/main',methods=['POST','GET'])
@login_manager.user_loader

def main(): 
    if 'loggedin' in session:
        email=session['u_email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Select * from docprofile')
        hospdata=cursor.fetchall()
        return render_template('/patients/main.html',hospdata=hospdata)
     
    
    return render_template('/patients/login.html')


# @app.route('/profile/<id>',methods=['POST','GET'])
# def DocProfile(id):
#     email=session['u_email']
#     cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('Select * from docprofile where docemail=%s',(id,))
#     profiledata=cursor.fetchall()
#     return render_template('/patients/docmoreinfo.html',profiledata=profiledata)

@app.route('/bookings',methods=['POST','GET'])
def bookings():
    if request.method=='POST':
       
        name=request.form['name']
        email=request.form['email']
        demail=request.form['demail']
        issues=request.form['issues']
        days=request.form['cdays']
        dates=request.form['cdates']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO bookings VALUES (%s, %s, %s,%s,%s,%s)', ( name,email,demail,issues,days,dates))
        mysql.connection.commit()
        return render_template("/patients/bookednotify.html")
    return render_template('/patients/Bookings.html')



@app.route('/userlogout')
def userlogout():
   session.pop('u_email')
   return redirect(url_for('index'))


@app.route('/sent') 
def sent():
    return render_template('/patients/notification.html')

@app.route('/browseengine')
def browseengine():
    return render_template("/patients/Browse.html")


@app.route('/media',methods=['POST','GET'])
def media():
    if request.method=='POST':
        email=session['u_email']
        content=request.form['content']
        postdate=date.today() #request.form['date']
        posttime=datetime.now() #request.form['time']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("Insert into dataset values(%s,%s,%s,%s)",(email,content,postdate,posttime,))
        mysql.connection.commit()
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("Select * from dataset")
       
    posts=cursor.fetchall()
    return render_template('/patients/Media.html',posts=posts)












@app.route('/doctorlogin',methods=['POST','GET'])
def doctorlogin():
    if request.method=='POST':
        message=  "Please fill the login "
        adminname=request.form['admin_email']
        adminpassword=request.form['admin_psw']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctors WHERE docemail = %s AND docpass = %s', (adminname, adminpassword))
        admin=cursor.fetchone()

        if admin:
            session['loggedin'] = True
            session['admin_psw'] = admin['docpass']
            session['admin_email'] = admin['docemail']
            session['admin_name'] = admin['docname']
            return redirect(url_for('docmain'))
        else:
            # Account doesnt exist or username/password incorrect
            message = 'Incorrect username/password!'
    return render_template('/doctors/doclogin.html', message='')
     
@app.route('/doctorregistration',methods=['POST','GET'])
def doctorregistration():
    if request.method=='POST':
        msg=""
        adminname=request.form['admin_name']
        adminemail=request.form['admin_email']
        adminpassword=request.form['admin_psw']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        account=cursor.execute('SELECT * FROM doctors WHERE docemail=%s',(adminemail,))
        if account :
             msg="Account already exists in this email Id"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',adminemail):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', adminname):
            msg = 'Username must contain only characters and numbers!'
        elif not adminname or not adminpassword or not adminemail:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO doctors VALUES (%s, %s, %s)', ( adminname, adminemail,adminpassword))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            #after successfully inserted redirect to loginpage
            return render_template('/doctors/doclogin.html')
    elif request.method == 'POST':
     
        msg = 'Please fill out the form!'
        return render_template('doctors/docsignup.html', msg=msg)
    return render_template('doctors/docsignup.html')

@app.route('/docmain',methods=['GET','POST'])
def docmain():
    if 'loggedin' in session:
        demail=session['admin_email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM bookings WHERE demail=%s',(demail,))
        bookingList=cursor.fetchall()
        cursor.execute('select docmeet from docprofile where docemail=%s',(demail,))
        docmeeting=cursor.fetchall()
        

       
        return render_template('/doctors/docmain.html',bookingList=bookingList,docmeeting=docmeeting)
    else:
        return render_template('/doctors/docmain.html')

@app.route('/docsent')
def docsent():
    return render_template('/doctors/docsent.html')

@app.route('/doclogout')
def doclogout():
   session.pop('admin_email')
   return redirect(url_for('index'))

@app.route('/doctorinfo')
def doctorinfo():
    return render_template('/doctors/result.html')

@app.route('/detailinfo/<id>')
def detailinfo(id):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('Select * from docinfo where email=%s',(id,)) 
    docdata=cursor.fetchall()

    return render_template('/doctors/information.html',docdata=docdata)


@app.route("/profileupdate",methods=['POST','GET'])
def profileupdate():
    if request.method=='POST':
            dname=request.form['d_name']
            dage=request.form['d_age']
            demail=request.form['d_email']
            dphno=request.form['d_phno']
            dphno2=request.form['d_phno2']
            ddegree=request.form['d_degree']
            dspeci=request.form['d_speci']
            dclg=request.form['d_clg']
            drank=request.form['d_rank']
            dexp=request.form['d_exp']
            dhosp=request.form['d_hosp']
            dtreat=request.form['d_treat']
            dfees=request.form['d_fees']
            dmeet=request.form['d_meet']
            ddays=request.form['d_days']
            dtiming=request.form['d_time']
            dstatus=request.form['d_status']
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO docprofile VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(dname,dage,demail,dphno,dphno2,ddegree,dspeci,dclg,drank,dexp,dhosp,dtreat,dfees,dmeet,ddays,dtiming,dstatus))
            mysql.connection.commit()
            return redirect(url_for('docsent'))
    return render_template('/doctors/docprofileupdate.html')






@app.route('/contact',methods=['POST','GET'])
def contact():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        subject=request.form['subject']
        message=request.form['message']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO contact VALUES(%s,%s,%s,%s)',(name,email,subject,message,))
        mysql.connection.commit()
    return render_template('/patients/index.html') 
 
if __name__=='__main__':
    app.debug=True
    app.run()

