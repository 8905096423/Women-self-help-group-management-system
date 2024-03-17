import json 
from urllib.parse import urlparse
from flask import Flask,render_template,request,session,redirect, url_for, flash
import mysql.connector 
import pandas as pd
import numpy as np 
import secrets 

app=Flask(__name__)
app.secret_key = 'RNSIT#123hpooja'
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="RNSIT#123h",
    database="women1",
)
global mycursor
mycursor=mydb.cursor()


@app.route('/')
def index():
    return render_template("index.html")




@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/group.html')
def group():
    return render_template("group.html")
    

@app.route('/manageGroup.html')
def mg():
    return render_template("manageGroup.html")


@app.route('/grp_info.html')
def Grp_info():
    return render_template("grp_info.html")



@app.route('/Grp_signin', methods=['POST'])
def grp_signin():
        username = request.form['In_username']
        password = request.form['In_password']
        groupname = request.form['In_groupname']
        query = "SELECT * FROM ORG WHERE Username = %s AND Pass_word = %s AND Group_Name = %s "
        mycursor.execute(query, (username, password,groupname))
        user = mycursor.fetchone()
        
        if user:
            return redirect('/grp_info.html') 
        else:
            flash('Invalid username or password or Group name. Please sign up first.', 'error')
            return redirect('/manageGroup.html') 
        
        cursor.close()
        conn.close()



@app.route('/Grp_signup', methods=['POST'])
def grp_signup():
    global gr_signup 
    gr_signup=[]
    user_name = request.form.get("username")
    email_Add = request.form.get("emailAdd")
    pass_word = request.form.get("password")
    confirm_pass=request.form.get("confirmPass")
    print(confirm_pass)
    username_exists = check_username_exists(user_name)
    password_exists=check_password_exists(pass_word)
    mail_exists=check_mail_exists(email_Add)

    if username_exists:
        flash('Username already exists. Please choose a different username.', 'error')
        return redirect('/group.html')
    elif password_exists:
        flash('Please choose any other password.', 'error')
        return redirect('/group.html')
    elif mail_exists:
        flash('Already account exists with this mail , please choose other mail to continue.', 'error')
        return redirect('/group.html')
    elif pass_word!=confirm_pass:
        flash('Password and Confirm Password do not match. Please make sure both passwords are identical.', 'error')
        return redirect('/group.html')

    else:
        gr_signup.append(user_name)
        gr_signup.append(email_Add)
        gr_signup.append(pass_word)

    signup_form = True
    return render_template('group.html', signup_confirm=signup_form,username_exists=False)




@app.route('/Grp_info', methods=['POST'])
def grp_info():
    
    # Get data from the second form
    group_Name = request.form.get("groupName")
    stDate = request.form.get("st_date")
    Intrest = request.form.get("interest")
    Tot_no_memb = request.form.get("TotNo_memb")
    group_location = request.form.get("Group_loc")
    meeting_ptn = request.form.get("meetingPtn")

    gr_signup.append(group_Name)
    gr_signup.append(stDate)
    gr_signup.append(Intrest)
    gr_signup.append(Tot_no_memb)
    gr_signup.append(group_location)
    gr_signup.append(meeting_ptn)

    values=(gr_signup[0],gr_signup[1],gr_signup[2],gr_signup[3],gr_signup[4],gr_signup[5],gr_signup[6],gr_signup[7],gr_signup[8])

    query = "INSERT INTO ORG(Username, Mail_adress, Pass_word, Group_Name, Start_Date, intrest_perc, No_members, Grp_Location, Meet_ptn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(query, values)
    mydb.commit()

    return render_template("group.html")






def check_username_exists(username):
    query1="SELECT * FROM ORG WHERE Username =%s"
    mycursor.execute(query1,(username,))
    result=mycursor.fetchone()
    if not result:
        return False 
    else:
        return True
    
def check_password_exists(password):
    query2="SELECT * FROM ORG WHERE Pass_word=%s"
    mycursor.execute(query2,(password,))
    result=mycursor.fetchone()
    if not result:
        return False
    else:
        return True 
    
def check_mail_exists(mail_id):
    query3="SELECT * FROM ORG WHERE Mail_adress=%s"
    mycursor.execute(query3,(mail_id,))
    result=mycursor.fetchone()
    if not result:
        return False
    else:
        return True



if __name__ == '__main__':
    app.run(debug=True)