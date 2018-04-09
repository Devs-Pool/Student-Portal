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
    date_of_birth=db.Column(db.String(30))
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


@app.route('/logout')
def logout():
   session.pop('email',None)
   return redirect(url_for('login'))


@app.route('/display<filename>')
def display(filename):
   return send_from_directory('uploads',filename)

@app.route('/personal_details',methods=['GET','POST'])
def personal_details():
    if 'name' not in session:
        return redirect(url_for('login'))
    name = session['name']
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('personal_details'))
        f = request.files['file']
        filename = (secure_filename(f.filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gender = "female"
        if request.form.get('male'):
            gender = "male"
        marry = "unmarried"
        dob = request.form['date']
        if request.form.get('marry'):
            marry = "married"
        handicapped = "yes"
        if request.form.get('n'):
            handicapped = "no"
        national = "indian"
        if request.form.get('other'):
            national = request.form['getcountry']
        category = "General"
        if request.form.get('sc'):
            category = "SC"
        if request.form.get('st'):
            category = "ST"
        if request.form.get('obc'):
            category = "OBC"
        if category == "" or national == "" or dob == "" or gender == "" or handicapped == "" or marry == "" :
            return redirect(url_for('personal_details'))
        student = Student.query.all()
        for i in student:
            if i.roll_no == session['roll_no']:
                i.nationality = national
                i.date_of_birth = dob
                i.gender = gender
                i.admission_category = category
                i.physically_challenged = handicapped
                i.marital_status = marry
                i.image_url = filename
                db.session.commit()
                break
        return redirect(url_for('parental_details'))
    student = Student.query.all()
    filename = "user.png"
    for i in student:
        if i.roll_no == session['roll_no']:
            if i.gender != None:
                return redirect(url_for('parental_details'))
            if i.image_url != None:
                filename = i.image_url
            break
    return render_template('personal_detail.html',name=name,filename=filename)
    

@app.route('/parental_details',methods=['GET','POST'])

def parental_details():
    if 'name' not in session:
        return redirect(url_for('login'))
    name = session['name']
    if request.method == 'POST':
        fname=request.form['fname']
        mname=request.form['mname']
        gname=request.form['gname']
        gemail=request.form['gemail']
        gmobile=request.form['gmobile']
        if gemail == "" or fname == "" or mname == "" or gname == "" or gmobile == "":
            return redirect(url_for('parental_details'))
        student = Student.query.all()
        for i in student:
            if i.roll_no == session['roll_no']:
                i.father_name = fname
                i.mother_name = mname
                i.guardian_name = gname
                i.guardian_contact_no = gmobile
                i.guardian_email_id = gemail
                db.session.commit()
                break
        return redirect(url_for('contact'))
    student = Student.query.all()
    filename = "user.png"
    for i in student:
        if i.roll_no == session['roll_no']:
            if i.father_name != None:
                return redirect(url_for('contact'))
            if i.image_url != None:
                filename = i.image_url
            break
    return render_template('parent_detail.html',name=name,filename=filename)

@app.route('/contact',methods=['GET','POST'])
def contact():
    if 'name' not in session:
        return redirect(url_for('login'))
    name = session['name']
    if request.method == 'POST':
        contact = request.form['contact_no']
        if contact == "" :
            return redirect(url_for('parental_details'))
        student = Student.query.all()
        for i in student:
            if i.roll_no == session['roll_no']:
                i.contact_no = contact
                db.session.commit()
                break
        return redirect(url_for('communication'))
    student = Student.query.all()
    filename = "user.png"
    for i in student:
        if i.roll_no == session['roll_no']:
            if i.contact_no != None:
                return redirect(url_for('communication'))
            if i.image_url !=None:
                filename = i.image_url
            break
    return render_template('contact.html',name=name,filename=filename)

@app.route('/communication',methods=['GET','POST'])

def communication():
    if 'name' not in session:
        return redirect(url_for('login'))
    name = session['name']
    if request.method == 'POST' :
        address=request.form['address']
        address=address+request.form['line2']
        address=address+request.form['line3']
        city=request.form['city']
        state=request.form['state']
        zip=request.form['zip']
        country=request.form['country']
        if address == "" or city == "" or state == "" or zip == "" or country == "" :
            return redirect(url_for('communication'))
        student = Student.query.all()
        for i in student:
            if i.roll_no == session['roll_no']:
                i.address = address
                i.city = city
                i.state = state
                i.zip = zip
                i.country = country
                db.session.commit()
                break
        return redirect(url_for('qualified'))
    student = Student.query.all()
    filename = "user.png"
    for i in student:
        if i.roll_no == session['roll_no']:
            if i.zip != None:
                return redirect(url_for('qualified'))
            if i.image_url != None:
                filename = i.image_url
            break
    return render_template('communication.html',name=name,filename=filename)


@app.route('/qualified',methods=['GET','POST'])
def qualified():
    if 'name' not in session:
        return redirect(url_for('login'))
    name = session['name']
    if request.method == 'POST' :
        exam=request.form['exam']
        marks=request.form['marks']
        rank=request.form['rank']
        branch=request.form['branch']
        if exam == "" or marks == "" or rank == "" or branch == "" :
            return redirect(url_for('qualified'))
        student = Student.query.all()
        for i in student:
            if i.roll_no == session['roll_no']:
                i.name_of_exam = exam
                i.exam_marks = marks
                i.exam_rank = rank
                i.branch = branch
                db.session.commit()
                break
        return redirect(url_for('academic_classX'))
    student = Student.query.all()
    filename = "user.png"
    for i in student:
        if i.roll_no == session['roll_no']:
            if i.name_of_exam != None:
                return redirect(url_for('academic_classX'))
            if i.image_url != None:
                filename = i.image_url
            break
    return render_template('qualify.html',name=name,filename=filename)


@app.route('/academic_classX',methods=['GET','POST'])
def academic_classX():
    if 'name' not in session:
        return redirect(url_for('login'))
    name = session['name']
    if request.method == 'POST' :
        year=request.form['year']
        school=request.form['school']
        board=request.form['board']
        percent=request.form['percent']
        if year == "" or school == "" or board == "" or percent == "" :
            return redirect(url_for('academic_classX'))
        student = Student.query.all()
        for i in student:
            if i.roll_no == session['roll_no']:
                i.x_passing_year = year
                i.x_school_name = school
                i.x_board_name = board
                i.x_grade = percent
                db.session.commit()
                break
        return redirect(url_for('academic_classXII'))
    student = Student.query.all()
    filename = "user.png"
    for i in student:
        if i.roll_no == session['roll_no']:
            if i.x_board_name != None:
                return redirect(url_for('academic_classXII'))
            if i.image_url != None:
                filename = i.image_url
            break
    return render_template('classX.html',name=name,filename=filename)


@app.route('/academic_classXII',methods=['GET','POST'])
def academic_classXII():
    if 'name' not in session:
        return redirect(url_for('login'))
    name = session['name']
    if request.method =='POST' :
        year=request.form['year']
        school=request.form['school']
        board=request.form['board']
        percent=request.form['percent']
        if year == "" or school == "" or board == "" or percent == "" :
            return redirect(url_for('academic_classXII'))
        student = Student.query.all()
        for i in student:
            if i.roll_no == session['roll_no']:
                i.xii_passing_year = year
                i.xii_school_name = school
                i.xii_board_name = board
                i.xii_grade = percent
                db.session.commit()
                break
        return redirect(url_for('dashboard'))
    student = Student.query.all()
    filename = "user.png"
    for i in student:
        if i.roll_no == session['roll_no']:
            if i.xii_board_name != None:
                return redirect(url_for('dashboard'))
            if i.image_url != None :
                filename = i.image_url
            break
    return render_template('classXII.html',name=name,filename=filename)

@app.route('/dashboard')
def dashboard():
    if 'name' in session:
        person = Student.query.all()
        filename="user.png"
        for i in person:
            if i.roll_no == session['roll_no']:
                session['gender']=i.gender
                session['dob']=i.date_of_birth
                session['contact']=i.contact_no
                session['category']= i.admission_category
                session['acategory']=i.admission_category
                if i.image_url != None :
                    filename = i.image_url
                break
        name = session['name']
        return render_template('dashboard.html',name=name,filename=filename)
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])

def register():
    if request.method == 'POST':
        name = request.form['Name']
        email  = request.form['Email']
        password = request.form['Password']
        signature = Student(name=name,email=email,password=password,semester="1")
        db.session.add(signature)
        db.session.commit()
        return redirect(url_for('login'))
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
                session['roll_no']=i.roll_no
                return redirect(url_for('dashboard'))
        return render_template('main.html',name = "Yor are not a registered user!")
    return render_template('main.html',name="")

if __name__ == "__main__":
    app.run(debug=True)