from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class PCTasks(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(600),nullable=True)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"{self.task} - {self.desc}"


 

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
      pctask=request.form['task']
      pcdesc=request.form['desc']
      pictask = PCTasks(task=pctask,desc=pcdesc)
      db.session.add(pictask)
      db.session.commit()
    allTasks = PCTasks.query.all()
    return render_template("index.html", allTasks=allTasks)

    # return render_template("index.html")
    
@app.route('/update/<int:id>')
def update(id):
    print(id)
    udTask = PCTasks.query.filter_by(id=id).first()
    db.session.delete(udTask)
    db.session.commit()

    # ptask=request.form['task']
    # pdesc=request.form['desc']
    # pictask = PCTasks(task=ptask,desc=pdesc)
    # db.session.add(pictask)
    # db.session.commit()

    # print(allTasks)
    # allTasks = PCTasks.query.all()
    return render_template("update.html")

@app.route('/delete/<int:id>')
def delete(id):
    delTasks = PCTasks.query.filter_by(id=id).first()
    db.session.delete(delTasks)
    db.session.commit()
    # print(allTasks)
    # allTasks = PCTasks.query.all()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
