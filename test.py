from flask import Flask,render_template,request,url_for,session,redirect,flash
from flask_mysqldb import MySQL
app=Flask(__name__,template_folder='template')

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="register"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


@app.route("/",methods=["GET","POST"])
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





@app.route("/login",methods=["POST","GET"])
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

@app.route("/plog",methods=["POST","GET"])
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


@app.route("/princi_home",methods=["POST","GET"])
def princi_home():
    return render_template('principalhome.html')


@app.route("/contact",methods=["POST","GET"])
def contact():
    return render_template('contact.html')

@app.route("/signup",methods=["POST","GET"])
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


@app.route("/open",methods=["POST","GET"])
def open():
    return render_template('open.html')






@app.route("/profile",methods=["POST","GET"])
def profile():
    return render_template('profile.html')
    

@app.route("/alog",methods=["POST","GET"])   #eduku ne therila ana iruku
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
    

@app.route("/user_home",methods=["POST","GET"])
def user_home():
    return render_template('profile.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__=="__main__":
    app.secret_key='123'
    app.run(debug=True)