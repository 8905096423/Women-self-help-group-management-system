import json 
from urllib.parse import urlparse
from flask import Flask,render_template,request,session,redirect, url_for, flash,jsonify
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
global i


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/member_info.html')
def memb():
    sql = "SELECT Member_id, M_Name, Age, Adress, ph_no FROM GRPP WHERE gp_Username = %s"
    mycursor.execute(sql, (inn_username,))
    members = mycursor.fetchall()
    num_members = len(members)
    memb_id_value=inn_username+'_'+str(1)
    # Pass group information and member data to the template
    group_name = "Women's Self-Help Group"
    group_description = "Welcome to our women's self-help group. We empower each other through mutual support and collaboration."
    return render_template('member_info.html', group_name=group_name, group_description=group_description, members=members,memb_length=num_members,memb_value=memb_id_value)





@app.route('/delete-member/<member_id>', methods=['POST'])
def delete_member(member_id):
    # Fetch member details from GRPP table
    query = "SELECT * FROM GRPP WHERE Member_id = %s"
    mycursor.execute(query, (member_id,))
    member_details = mycursor.fetchone()
    if member_details:
        # Insert member details into PAST_MEMB table
        insert_query = "INSERT INTO PAST_MEMB VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.execute(insert_query, member_details)
        # Delete member record from GRPP table
        delete_query = "DELETE FROM GRPP WHERE Member_id = %s"
        mycursor.execute(delete_query, (member_id,))
        # Commit changes
        mydb.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 404





@app.route('/get_data')
def get_data():
   
    query1 ="SELECT MAX(CAST(SUBSTRING(Member_id, LOCATE('_', Member_id) + 1) AS UNSIGNED)) AS max_member_id FROM GRPP WHERE gp_Username = %s" 
    mycursor.execute(query1, (inn_username,))
    members = mycursor.fetchall()
    max_id =int(members[0][0]) + 1
    new_memb_id=inn_username+'_'+str(max_id)
    
    data = {'message':new_memb_id }
    return jsonify(data)


@app.route('/save-member/<member_id>/<name>/<age>/<address>/<ph_no>', methods=['POST'])
def save_member(member_id,name,age,address,ph_no):
    
    # Check if member ID exists in GRPP table
    query = "SELECT * FROM GRPP WHERE Member_id = %s"
    mycursor.execute(query, (member_id,))
    existing_member = mycursor.fetchone()



    if existing_member:
        # Member ID exists, update the member details
        update_query = "UPDATE GRPP SET M_Name = %s, Age = %s, Adress = %s, ph_no = %s WHERE Member_id = %s"
        mycursor.execute(update_query, (name, age, address, ph_no, member_id))
    else:
        # Member ID does not exist, insert a new member
        
        insert_query = "INSERT INTO GRPP (gp_Username ,Member_id, M_Name, Age, Adress, ph_no) VALUES (%s,%s, %s, %s, %s, %s)"
        mycursor.execute(insert_query, (inn_username,member_id, name, age, address, ph_no))
        
    # Commit changes to the database
    mydb.commit()

    return jsonify({'success': True}), 200









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
        global inn_username
        inn_username = request.form['In_username']
        password = request.form['In_password']
        groupname = request.form['In_groupname']
        query = "SELECT * FROM ORG WHERE Username = %s AND Pass_word = %s AND Group_Name = %s "
        mycursor.execute(query, (inn_username, password,groupname))
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