from flask import Flask, render_template, request,send_file,send_from_directory,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
import os
from werkzeug import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:taru9668@localhost/studentPortal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  
UPLOAD_FOLDER = './uploads'
app.secret_key = 'njsdnjsd'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
class Student(db.Model):
    name = db.Column(db.String(50),primary_key = True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))

class Reference(db.Model):
    email = db.Column(db.String(50),primary_key = True)

class uploaded(db.Model):
    name = db.Column(db.String(50),primary_key=True)



@app.route('/upload')
def upload():
   return send_from_directory('uploads',"3musketeer.jpg",as_attachment=True)

@app.route('/logout')
def logout():
   session.pop('email',None)
   return redirect(url_for('login'))


@app.route('/display<filename>')
def display(filename):
   return send_from_directory('uploads',filename)

@app.route('/personal_details')
def personal_details():
    if 'email' in session:
        name = session['email']
        return render_template('personal_detail.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/parental_details')
def parental_details():
    if 'email' in session:
        name = session['email']
        return render_template('parent_detail.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/contact')
def contact():
    if 'email' in session:
        name = session['email']
        return render_template('contact.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/communication')
def communication():
    if 'email' in session:
        name = session['email']
        return render_template('communication.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/qualified')
def qualified():
    if 'email' in session:
        name = session['email']
        return render_template('qualify.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/academic_classX')
def academic_classX():
    if 'email' in session:
        name = session['email']
        return render_template('classX.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/academic_classXII')
def academic_classXII():
    if 'email' in session:
        name = session['email']
        return render_template('classXII.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        name = session['email']
        return render_template('dashboard.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/dikhade')
def dikhade():
   return render_template('display.html',filename="3musketeer.jpg")

@app.route('/akshat')
def akshat():
   return render_template('dashboard_test.html')


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
    return render_template("register.html",name="")
    
@app.route('/login',methods=['GET','POST'])

def login():
    if request.method == 'POST':
        name  = request.form['Email']
        password = request.form['Password']
        if name is "":
            return redirect(url_for('login'))
        person = Student.query.all()
        if request.form.get('teacher'):
            return render_template('dashboard_test.html')
        for i in person:
            if i.email == name and i.password==password:
                session['email']=name
                return redirect(url_for('dashboard'))
        return render_template('main.html',name = "Yor are not a registered user!")
    return render_template('main.html',name="")

if __name__ == "__main__":
    app.run(debug=True)