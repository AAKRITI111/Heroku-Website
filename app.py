from flask import Flask, render_template, url_for, request, redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PCTasks(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(200),nullable=False)
    userlogged = db.Column(db.String(200),nullable=False)
    assigned = db.Column(db.String(600),nullable=True)
    desc = db.Column(db.String(600),nullable=True)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"{self.task} - {self.desc}"

@app.route('/login',methods=['POST','GET'])
def login():
  if request.method == 'POST':
   username = request.form['username']
   password = request.form['password']
   if username in ['Picy','Pica'] and password == "iamsorry":
    session["user"]=username
    return redirect(url_for("home"))
   else:
    return render_template("login.html")
  else:
    return render_template("login.html")



@app.route('/home',methods=['GET'])
def home():
  if "user" in session :
    allTasks = PCTasks.query.all()
    return render_template("index.html", allTasks=allTasks)
  else:
    return render_template("login.html")

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method=='POST':
      pctask=request.form['task']
      pcdesc=request.form['desc']
      pcassign=request.form['assigned']
      pcuserlogged=session['user']
      print("asby",pcuserlogged)
      pictask = PCTasks(task=pctask,desc=pcdesc,assigned=pcassign,userlogged=pcuserlogged)
      db.session.add(pictask)
      db.session.commit()
    allTasks = PCTasks.query.all()
    return render_template("index.html", allTasks=allTasks)
    
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
  if "user" in session:
   if request.method == 'POST' :
    ptask=request.form['task']
    pdesc=request.form['desc']
    passign=request.form['assign']
    # pictask = PCTasks(task=ptask,desc=pdesc)
    pcTask = PCTasks.query.filter_by(id=id).first()
    pcTask.task=ptask
    pcTask.desc=pdesc
    pcTask.assign=passign
    pcTask.userlogged=session['user']
    db.session.add(pcTask)
    db.session.commit()
    return redirect("/")

    # print(allTasks)
    # allTasks = PCTasks.query.all()
   pcTask = PCTasks.query.filter_by(id=id).first()
   return render_template("index.html", pcTask=pcTask)
  else:
    return render_template("login.html")

@app.route('/delete/<int:id>')
def delete(id):
  if "user" in session :
    delTasks = PCTasks.query.filter_by(id=id).first()
    db.session.delete(delTasks)
    db.session.commit()
    # print(allTasks)
    # allTasks = PCTasks.query.all()
    return redirect(url_for("home"))
  else:
    return render_template("login.html")

@app.route('/about')
def about():
  if "user" in session :
    return render_template('about.html')
  else:
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

