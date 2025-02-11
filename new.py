from flask import Flask,render_template,request,url_for,session,redirect,flash
from flask_mysqldb import MySQL
app=Flask(__name__,template_folder='template')

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="register"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


@app.route("/",methods=["GET","POST"])   #HOME PAGE
def index():
    if 'alogin' in request.form:
        if request.method == 'POST':
            aname=request.form["aname"]
            apass=request.form["apass"]
            try:
                cur=mysql.connection.cursor()
                cur.execute("select * from admin where aname=%s and apass=%s",[aname,apass])
                res=cur.fetchone()
                if res:
                    session["aname"]=res["aname"]
                    session["aid"]=res["aid"]
                    return redirect(url_for('admin_home'))
                else:
                    return render_template("open.html")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template('open.html')
@app.route("/alog",methods=["POST","GET"])   # hod login ku iruku
def alog():
    if 'alogin' in request.form:
        if request.method == 'POST':
            aname=request.form["aname"]
            apass=request.form["apass"]
            try:
                cur=mysql.connection.cursor()
                cur.execute("select * from admin where aname=%s and apass=%s",[aname,apass])
                res=cur.fetchone()
                if res:
                    session["aname"]=res["aname"]
                    session["aid"]=res["aid"]
                    return redirect(url_for('admin_home'))
                else:
                    return render_template("adlogin.html")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close() 
    return render_template('adlogin.html')

@app.route("/plog",methods=["POST","GET"])       #princi oda login page ana ulla pogala login matu katudhu
def plog():
    if 'plogin' in request.form:
        if request.method == 'POST':
            pname=request.form["pname"]
            ppass=request.form["ppass"]
            try:
                cur=mysql.connection.cursor()
                cur.execute("select * from principal where pname=%s and ppass=%s",[pname,ppass])
                res=cur.fetchone()
                if res:
                    session["pname"]=res["pname"]
                    session["pid"]=res["pid"]
                    return redirect(url_for('princi_home'))
                else:
                    return render_template("princilogin.html")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template('princilogin.html')


@app.route("/admin_home",methods=["POST","GET"])
def admin_home():
    return render_template('adminhome.html')

@app.route("/princi_home",methods=["POST","GET"])    #principal oda home page pa, idula user details and leave requests pakalam
def princi_home():
    return render_template('principalhome.html')

@app.route("/contact",methods=["POST","GET"])       #contact details open aguthu pa
def contact():
    return render_template('contact.html')

@app.route("/signup",methods=["POST","GET"])       #open aguthu staff signup , database la data store aguthu
def signup():
    if 'register' in request.form:
        if request.method == 'POST':
          uname=request.form['uname']
          password=request.form['password']
          dept=request.form['dept']
          address=request.form['address']
          contact=request.form['contact']
          mail=request.form['mail']
          cur=mysql.connection.cursor()
          cur.execute('insert into users(name,password,dept,address,contact,mail) values (%s,%s,%s,%s,%s,%s)',[uname,password,dept,address,contact,mail])
          mysql.connection.commit()
          return render_template('signup.html')
    return render_template('signup.html')
   
@app.route("/about")                   # clg ku about vision mission la 
def about():
    return render_template('about.html')

''' @app.route("/Register",methods=["POST","GET"])
def Register():
    if request.method=="POST":
        userName=request.form.get('userName')
        name=request.form.get('name')
        mail=request.form.get('eMail')
        pword=request.form.get('passWord')
        rpword=request.form.get('rePassWord')
        return render_template("profile.html",userName=userName,name=name,mail=mail,pword=pword,rpword=rpword)'''
@app.route("/login",methods=["POST","GET"])        #staff login same as princi login. open aguthu ana ulla pola ,ulla ponu na logout code irukanum
def login():
    if 'ulogin' in request.form:
        if request.method == 'POST':
            name=request.form["uname"]
            password=request.form["password"]
            try:
                cur=mysql.connection.cursor()
                cur.execute("select * from users where name=%s and password=%s",[name,password])
                res=cur.fetchone()
                if res:
                    session["name"]=res["name"]
                    session["pid"]=res["pid"]
                    return redirect(url_for('user_home'))
                else:
                    return render_template('login.html')
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template('login.html')

@app.route("/profile",methods=["POST","GET"])
def profile():
    return render_template('profile.html')
@app.route("/staffleave",methods=["POST","GET"])
def staffleave():

    if 'application' in request.form:
        if request.method == 'POST':
          aname=request.form['aname']
          adept=request.form['adept']
          adesignation=request.form['adesignation']
          adoc=request.form['adoc']
          afdate=request.form['afdate']
          atdate=request.form['atdate']
          areason=request.form['areason']
          aaddress=request.form['aaddress']
          acontact=request.form['acontact']
          cur=mysql.connection.cursor()
          cur.execute('insert into application(name,department,designation,document,fromdate,todate,reason,address,contact) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',[aname,adept,adesignation,adoc,afdate,atdate,areason,aaddress,acontact])
          mysql.connection.commit()
          return render_template('staff leave.html')
    return render_template('staff leave.html')

    return render_template('staff leave.html')
@app.route("/open",methods=["POST","GET"])
def open():
    return render_template('open.html')
@app.route("/user_home",methods=["POST","GET"])
def user_home():
    return render_template('profile.html')

@app.route("/user_profile")
def user_profile():
    cur = mysql.connection.cursor()
    id=session["pid"]
    qry="select * from users where pid=%s"
    cur.execute(qry,[id])
    data=cur.fetchone()
    cur.close()
    count=cur.rowcount
    if count==0:
        flash("Users Not Found ...!!!!","danger")
    else:
        return render_template("user_profile.html",res=data)
    

@app.route("/update_user", methods=['GET','POST'])
def update_user():
    if request.method == 'POST':
        name = request.form['name']
        password=request.form['password']
        dept=request.form['dept']
        address=request.form['address']
        contact=request.form['contact']
        mail=request.form['mail']
        pid=session["pid"]
        cur=mysql.connection.cursor()
        cur.execute("update users set name=%s,password=%s,dept=%s,address=%s,contact=%s,mail=%s where pid=%s",[name,password,dept,address,contact,mail,pid])
        mysql.connection.commit()
        flash('User Updated Successfully','success')
        return redirect(url_for('user_profile'))
    return render_template("user_profile.html")

'''@app.route("/requests", methods=['GET','POST'])
def requests():
  if request.method == 'POST':
          aname=request.form['aname']
          adept=request.form['adept']
          adesignation=request.form['adesignation']
          adoc=request.form['adoc']
          afdate=request.form['afdate']
          atdate=request.form['atdate']
          areason=request.form['areason']
          aaddress=request.form['aaddress']
          acontact=request.form['acontact']'''
@app.route("/requests", methods=['GET','POST'])
def requests():
          cur=mysql.connection.cursor()
          cur.execute("select * from application")
          data=cur.fetchall()
          cur.close()
          count=cur.rowcount
          if count==0:
                    flash("Requests Not Found ...!!!!","danger")
          else:
                    return render_template("request.html",res=data)
  
                
        


@app.route("/logout")        #ellarum logout agaraku iruku, idu illama login panna mudiyathu, avanga home kulla poga idu irukanum
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/view_users")
def view_users():
    cur = mysql.connection.cursor()
    qry = "select * from users"
    cur.execute(qry)
    data=cur.fetchall()
    cur.close()
    count = cur.rowcount
    if count == 0:
        flash("Users not Found...!!!!","danger")
    return render_template("users.html",res=data)

@app.route("/pview_users")
def pview_users():
    if "approved" in request.form:
        if request.method == 'POST':
          uname=request.form['name']
          dept=request.form['dept']
          address=request.form['address']
          contact=request.form['contact']
          mail=request.form['mail']
          cur=mysql.connection.cursor()
          cur.execute('insert into principalusers(name,password,dept,address,contact,mail) values (%s,%s,%s,%s,%s,%s)',[uname,dept,address,contact,mail])
          mysql.connection.commit()
          return render_template('request.html')
    return render_template("request.html")

@app.route("/qview_users")          #principal oda page la users oda details katraku iruku
def qview_users():
    cur = mysql.connection.cursor()
    qry = "select * from users"   # i have  changed the "principalusers" to "users" !! on 1.2.2025 
    cur.execute(qry)
    data=cur.fetchall()
    cur.close()
    count = cur.rowcount
    if count == 0:
        flash("Users not Found...!!!!","danger")
    return render_template("principalusers.html",res=data)



@app.route("/delete_users/<string:id>",methods=['GET','POST'])   #idu use panni princi users ah delete panalam
def delete_users(id):
    cur=mysql.connection.cursor()
    cur.execute("delete from users where pid=%s",[id])
    mysql.connection.commit()
    flash("Users Delete Successfully","danger")
    return redirect(url_for("view_users"))   

if __name__=="__main__":
    app.secret_key='123'
    app.run(debug=True)