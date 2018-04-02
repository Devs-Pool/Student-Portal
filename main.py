from flask import Flask, render_template, request,send_file,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
import os
from werkzeug import secure_filename
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:taru9668@localhost/studentPortal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

class Student(db.Model):
    name = db.Column(db.String(50),primary_key = True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))

class uploaded(db.Model):
    name = db.Column(db.String(50),primary_key=True)

@app.route('/upload')
def upload():
   return send_from_directory('uploads',"3musketeer.jpg",as_attachment=True)

@app.route('/dashboard')
def dashboard():
   return render_template('dashboard.html')

@app.route('/display<filename>')
def display(filename):
   return send_from_directory('uploads',filename)

@app.route('/dikhade')
def dikhade():
   return render_template('display.html',filename="3musketeer.jpg")


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = (secure_filename(f.filename))
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      signature = uploaded(name=filename)
      db.session.add(signature)
      db.session.commit()
      return 'file uploaded successfully'


@app.route('/register',methods=['GET','POST'])

def register():
    if request.method == 'POST':
        name = request.form['Name']
        email  = request.form['Email']
        password = request.form['Password']
        signature = Student(name=name,email=email,password=password)
        db.session.add(signature)
        db.session.commit()
        return render_template("thanks.html")
    return render_template("register.html",name="nothing")
    
@app.route('/login',methods=['GET','POST'])

def login():
    if request.method == 'POST':
        name  = request.form['Email']
        password = request.form['Password']
        person = Student.query.all()
        for i in person:
            if i.email == name and i.password==password:
                return render_template('dashboard.html',name = name)
        return render_template('main.html',name = name)
    return render_template('main.html',name="noting")

if __name__ == "__main__":
    app.run(debug=True)