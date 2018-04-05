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
    name = db.Column(db.String(50))
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    image_url = db.Column(db.String(100))
    contact_no = db.Column(db.String(12))
    father_name =db.Column(db.String(30))
    mother_name = db.Column(db.String(30))
    guardian_name= db.Column(db.String(30))
    guardian_contact_no= db.Column(db.String(12))
    guardian_email_id=db.Column(db.String(30))
    date_of_birth=db.Column(db.String(8))
    gender=db.Column(db.String(10))
    admission_category=db.Column(db.String(10))
    physically_challenged=db.Column(db.String(10))
    nationality=db.Column(db.String(30))
    marital_status=db.Column(db.String(30))
    address=db.Column(db.String(200))
    city=db.Column(db.String(30))
    state=db.Column(db.String(30))
    zip=db.Column(db.String(30))
    country=db.Column(db.String(30))
    name_of_exam=db.Column(db.String(30))
    exam_marks=db.Column(db.String(30))
    exam_rank=db.Column(db.String(30))
    semester=db.Column(db.Integer())
    branch=db.Column(db.String(30))
    roll_no=db.Column(db.Integer(),primary_key=True)
    x_passing_year=db.Column(db.String(30))
    x_school_name=db.Column(db.String(30))
    x_board_name=db.Column(db.String(30))
    x_grade=db.Column(db.String(30))
    xii_passing_year=db.Column(db.String(30))
    xii_school_name=db.Column(db.String(30))
    xii_board_name=db.Column(db.String(30))
    xii_grade=db.Column(db.String(30))

    #  create table student(name char(30), email char(30) unique,  password  char(30),  image_url char(100),  contact_no char(12), father_name char(30),  mother_name char(30), guardian_name char(30), guardian_contact_no char(30), guardian_email_id char(30),date_of_birth char(8),gender char(10), admission_category char(10), physically_challenged char(10),  nationality char(30), marital_status char(30), address char(200), city char(30), state char(30), zip char(30), country char(30), name_of_exam char(30), exam_marks char(30), exam_rank char(30), semester int, branch char(30), roll_no INT PRIMARY KEY AUTO_INCREMENT,  x_passing_year char(30), x_school_name char(30), x_board_name char(30), x_grade char(30), xii_passing_year char(30), xii_school_name char(30), xii_board_name char(30), xii_grade char(30));
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
    if 'name' in session:
        name = session['name']
        return render_template('personal_detail.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/parental_details')
def parental_details():
    if 'name' in session:
        name = session['name']
        return render_template('parent_detail.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/contact')
def contact():
    if 'name' in session:
        name = session['name']
        return render_template('contact.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/communication')
def communication():
    if 'name' in session:
        name = session['name']
        return render_template('communication.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/qualified')
def qualified():
    if 'name' in session:
        name = session['name']
        return render_template('qualify.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/academic_classX')
def academic_classX():
    if 'name' in session:
        name = session['name']
        return render_template('classX.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/academic_classXII')
def academic_classXII():
    if 'name' in session:
        name = session['name']
        return render_template('classXII.html',name=name,filename="3musketeer.jpg")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'name' in session:
        name = session['name']
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
        email  = request.form['Email']
        password = request.form['Password']
        if email is "":
            return redirect(url_for('login'))
        person = Student.query.all()
        if request.form.get('teacher'):
            return render_template('dashboard_test.html')
        for i in person:
            if i.email == email and i.password==password:
                session['email']=email
                session['name']=i.name
                return redirect(url_for('dashboard'))
        return render_template('main.html',name = "Yor are not a registered user!")
    return render_template('main.html',name="")

if __name__ == "__main__":
    app.run(debug=True)