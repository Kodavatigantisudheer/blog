from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',password='system',database='sudheer')
with mysql.connector.connect(host='localhost',user='root',password='system',database='sudheer'):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists register(username varchar(40) primary key,mobile varchar(20) unique,email varchar(50) unique,password varchar(20))")
    cursor.execute("create table if not exists login(username varchar(40) primary key,password varchar(20) unique)")
app=Flask(__name__)
app.secret_key="my secretkey is too secret"
@app.route("/")
def home():
    return render_template('homepage.html')
@app.route("/reg",methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        mobile=request.form['mobile']
        email=request.form['email']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute("insert into register(username,mobile,email,password) values(%s,%s,%s,%s)",[username,mobile,email,password])
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        mydb.commit()
        cursor.execute("select count(*) from register where username=%s && password=%s",[username,password])
        data=cursor.fetchone()[0]
        print(data)
        cursor.close()
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('home'))
        else:
            return "invalid username and password"

    return render_template('login.html')
@app.route("/logout")
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/addposts',methods=['GET','POST'])
def addposts():
    if request.method=="POST":
        title=request.form['title']
        content=request.form['content']
        slug=request.form['slug']
        # print(title)
        # print(content)
        # print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute("insert into posts(title,content,slug) values(%s,%s,%s)",[title,content,slug])
        mydb.commit()
        cursor.close()
    return render_template('add_post.html')
@app.route('/viewpost')
def viewpost():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts')
    posts=cursor.fetchall()
    cursor.close()
    return render_template('viewpost.html',posts=posts)
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.execute('delete from posts where id=%s',(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('viewpost'))
@app.route('/update_post/<int:id>',methods=['GET','POST'])
def update_post(id):
    if request.method=="POST":
        title=request.form['title']
        content=request.form['content']
        slug=request.form['slug']
        # print(title)
        # print(content)
        # print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('update posts set title=%s,content=%s,slug=%s where id=%s',(title,content,slug,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('viewpost'))
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from posts where id=%s',(id,))
        post=cursor.fetchone()
        cursor.close()
        return render_template('update.html',post=post)
        

app.run()