from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:taru9668@localhost/studentPortal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)    

class Comment(db.Model):
    name = db.Column(db.String(50),primary_key = True)
    password = db.Column(db.String(40))
    def __init__(self,name,password):
        self.name = name
        self.password = password


@app.route('/profile')

def profile():
    return render_template("choose.html",name="Tarun")


@app.route('/form',methods=['GET','POST'])

def form():
    return render_template('register.html',name="noting")

    
@app.route('/login',methods=['GET','POST'])

def login():
    if request.method == 'POST':
        name  = request.form['username']
        password = request.form['pass']
        person = Comment.query.all()
        for i in person:
            if i.name == name and i.password == password:
                return render_template('form.html',name = name)
        signature = Comment(name=name,password=password)
        db.session.add(signature)
        db.session.commit()
        return render_template('register.html',name = name)
    return render_template('hello.html',name="noting")

if __name__ == "__main__":
    app.run(debug=True)
