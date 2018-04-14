from flask import Flask, render_template, request,send_file,send_from_directory,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
import os
from werkzeug import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ptw161@akj011@localhost/StudentPortal'
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

class Courses(db.Model):
    cid = db.Column(db.String(30),primary_key=True)
    cname = db.Column(db.String(30))
    ccredits = db.Column(db.Integer())
    semester = db.Column(db.Integer())
    teacherid = db.Column(db.String(30))

class Teachers(db.Model):
    name = db.Column(db.String(30))
    email = db.Column(db.String(30),primary_key=True)
    password = db.Column(db.String(30))

class Admin(db.Model):
    email = db.Column(db.String(30),primary_key=True)
    password = db.Column(db.String(30))

class Marks(db.Model):
    sno=db.Column(db.Integer(),primary_key=True)
    cid=db.Column(db.String(30))
    sid=db.Column(db.Integer())
    marks=db.Column(db.Integer())

# create table student(name char(30), email char(30) unique,  password  char(30),  image_url char(100),  contact_no char(12), father_name char(30),  mother_name char(30), guardian_name char(30), guardian_contact_no char(30), guardian_email_id char(30),date_of_birth char(8),gender char(10), admission_category char(10), physically_challenged char(10),  nationality char(30), marital_status char(30), address char(200), city char(30), state char(30), zip char(30), country char(30), name_of_exam char(30), exam_marks char(30), exam_rank char(30), semester int, branch char(30), roll_no INT PRIMARY KEY AUTO_INCREMENT,  x_passing_year char(30), x_school_name char(30), x_board_name char(30), x_grade char(30), xii_passing_year char(30), xii_school_name char(30), xii_board_name char(30), xii_grade char(30));

# create table courses(cid char(30) primary key, cname char(30), ccredits int, semester int, teacherid char(30));
#insert into courses values('SMAT130C', 'Maths', 3, 1, 'ABAB');
#insert into courses values('IITP132C', 'Introduction to programming' , 5, 1, 'VKC');
#insert into courses values('SPAS230C', 'Probability and Statistics', 3, 2, 'ABAB');
#insert into courses values('IDST232C', 'Data Structures and ALgorithms', 5, 2, 'BSS');
#insert into courses values('SMAT332C', 'Maths 2', 3, 3, 'ABAB');
#insert into courses values('IOOM332C', 'Object Orientation and Methodology', 5, 3, 'RK');
#insert into courses values('SMAT430C', 'Maths 3', 3, 4, 'Mary Samuel');
#insert into courses values('IDBM432C', 'Database Management Systems', 5, 4, 'Shikha Gautam');

#create table teachers(name char(30), email char(30) primary key, password char(30));

#create table admin(email char(30) primary key, password char(30));
#insert into admin values('admin@iiitl.ac.in','admin@iiitl');

#create table marks(sno int primary key auto_increment,cid char(30),sid int,marks int not null);

@app.route('/logout')
def logout():
   session.pop('email',None)
   session.pop('temail',None)
   session.pop('name',None)
   session.pop('tname',None)
   session.pop('roll_no',None)
   session.pop('gender',None)
   session.pop('dob',None)
   session.pop('contact',None)
   session.pop('category',None)
   session.pop('acategory',None)
   session.pop('semester',None)
   session.pop('aemail',None)
   return redirect('/')


@app.route('/display<filename>')
def display(filename):
   return send_from_directory('uploads',filename)

@app.route('/personal_details',methods=['GET','POST'])
def personal_details():
    if 'tname' in session or 'aemail' in session:
        return redirect(url_for('logout'))
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
    if 'tname' in session or 'aemail' in session:
        return redirect(url_for('logout'))
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
    if 'tname' in session or 'aemail' in session:
        return redirect(url_for('logout'))
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
    if 'tname' in session or 'aemail' in session:
        return redirect(url_for('logout'))
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
    if 'tname' in session or 'aemail' in session:
        return redirect(url_for('logout'))
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
    if 'tname' in session or 'aemail' in session:
        return redirect(url_for('logout'))
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
    if 'tname' in session or 'aemail' in session:
        return redirect(url_for('logout'))
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
    if 'tname' in session or 'aemail' in session:
        return redirect(url_for('logout'))
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
                session['semester']=i.semester
                if i.image_url != None :
                    filename = i.image_url
                break
        course = Courses.query.all()
        course1='No courses to Show'
        course2=''
        for i in course:
            if i.semester is not None:
                if i.semester == session['semester']:
                    if course1 == 'No courses to Show':
                        course1 = "1. "+i.cid+" "+i.cname
                        continue
                    course2 = "2. "+i.cid+" "+i.cname
        name = session['name']
        return render_template('dashboard.html',name=name,filename=filename,course1=course1,course2=course2)
    return redirect(url_for('logout'))

@app.route('/update_students',methods=['GET','POST'])
def update_students():
    if 'name' in session or 'tname' in session or 'aemail' not in session :
        return redirect(url_for('logout'))
    sid=0
    try:
        sid=int(request.args.get('sid'))
    except ValueError:
        return redirect(url_for('admin_students'))
    message='No such Unique ID found'
    if sid !='' and sid != None and request.method == 'POST' :
        students=Student.query.all()
        for i in students:
            if i.roll_no == sid:
                message = 'Student Details Updated Successfully'
                temp=request.form['name']
                if temp != '':
                    i.name=temp
                temp=request.form['email']
                if temp != '':
                    i.email=temp
                temp=request.form['password']
                if temp != '':
                    i.password=temp
                temp=request.form['contact']
                if temp != '':
                    i.contact_no=temp
                temp=request.form['fname']
                if temp != '':
                    i.father_name=temp
                temp=request.form['mname']
                if temp != '':
                    i.mother_name=temp
                temp=request.form['gname']
                if temp != '':
                    i.guardian_name=temp
                temp=request.form['gcontact']
                if temp != '':
                    i.guardian_contact_no=temp
                temp=request.form['gemail']
                if temp != '':
                    i.guardian_email_id=temp
                temp=request.form['dob']
                if temp != '':
                    i.date_of_birth=temp
                temp=request.form['gender']
                if temp != '':
                    i.gender=temp
                temp=request.form['acat']
                if temp != '':
                    i.admission_category=temp
                temp=request.form['physical']
                if temp != '':
                    i.physically_challenged=temp
                temp=request.form['nationality']
                if temp != '':
                    i.nationality=temp
                temp=request.form['mstatus']
                if temp != '':
                    i.marital_status=temp
                temp=request.form['address']
                if temp != '':
                    i.address=temp
                temp=request.form['city']
                if temp != '':
                    i.city=temp
                temp=request.form['state']
                if temp != '':
                    i.state=temp
                temp=request.form['zip']
                if temp != '':
                    i.zip=temp
                temp=request.form['country']
                if temp != '':
                    i.country=temp
                temp=request.form['examname']
                if temp != '':
                    i.name_of_exam=temp
                temp=request.form['exammarks']
                if temp != '':
                    i.exam_marks=temp
                temp=request.form['examrank']
                if temp != '':
                    i.exam_rank=temp
                temp=request.form['semester']
                try:   
                    if temp != '':
                        i.semester=temp
                except ValueError:
                    message='invalid semester'
                    break
                temp=request.form['branch']
                if temp != '':
                    i.branch=temp
                temp=request.form['xyear']
                if temp != '':
                    i.x_passing_year=temp
                temp=request.form['xschool']
                if temp != '':
                    i.x_school_name=temp
                temp=request.form['xboard']
                if temp != '':
                    i.x_board_name=temp
                temp=request.form['xgrade']
                if temp != '':
                    i.x_grade=temp
                temp=request.form['xiiyear']
                if temp != '':
                    i.xii_passing_year=temp
                temp=request.form['xiischool']
                if temp != '':
                    i.xii_school_name=temp
                temp=request.form['xiiboard']
                if temp != '':
                    i.xii_board_name=temp
                temp=request.form['xiigrade']
                if temp != '':
                    i.xii_grade=temp
                db.session.commit()
    if sid !='' and sid != None and request.method == 'GET' :
        students=Student.query.all()
        for i in students :
            if i.roll_no == sid :
                name=i.name
                email=i.email
                contact=i.contact_no
                fname=i.father_name
                mname=i.mother_name
                gname=i.guardian_name
                gcontact=i.guardian_contact_no
                gemail=i.guardian_email_id
                dob=i.date_of_birth
                gender=i.gender
                acat=i.admission_category
                physical=i.physically_challenged
                nationality=i.nationality
                mstatus=i.marital_status
                address=i.address
                city=i.city
                state=i.state
                zip=i.zip
                country=i.country
                examname=i.name_of_exam
                exammarks=i.exam_marks
                examrank=i.exam_rank
                semester=i.semester
                branch=i.branch
                xyear=i.x_passing_year
                xschool=i.x_school_name
                xboard=i.x_board_name
                xgrade=i.x_grade
                xiiyear=i.xii_passing_year
                xiischool=i.xii_school_name
                xiiboard=i.xii_board_name
                xiigrade=i.xii_grade
                return render_template('update_students.html',name=name,email=email,contact=contact,fname=fname,mname=mname,gname=gname,gcontact=gcontact,gemail=gemail,dob=dob,gender=gender,acat=acat,physical=physical,nationality=nationality,mstatus=mstatus,address=address,city=city,state=state,zip=zip,country=country,examname=examname,exammarks=exammarks,examrank=examrank,semester=semester,branch=branch,xyear=xyear,xschool=xschool,xboard=xboard,xgrade=xgrade,xiischool=xiischool,xiiboard=xiiboard,xiigrade=xiigrade,xiiyear=xiiyear,sid=str(sid))
    return redirect(url_for('admin_students',message=message))


@app.route('/admin_students',methods=['GET','POST'])
def admin_students():
    if 'name' in session or 'tname' in session or 'aemail' not in session :
        return redirect(url_for('logout'))
    message=request.args.get('message')
    if message == None:
        message=''
    if request.method == 'POST' :
        sid=0
        try:
            sid = int(request.form['sid'])
        except ValueError:
            message='Invalid Unique ID'
            return render_template('admin_students.html',name=message)
        students = Student.query.all()
        message='Invalid Unique ID'
        for i in students :
            if i.roll_no == sid :
                return redirect(url_for('update_students',sid=str(sid)))
    return render_template('admin_students.html',name=message)

@app.route('/add_course',methods=['GET','POST'])
def add_course():
    if 'name' in session or 'tname' in session or 'aemail' not in session :
        return redirect(url_for('logout'))
    message = ''
    if request.method == 'POST' :
        cid=request.form['cid']
        cname=request.form['cname']
        ccredits=request.form['ccredits']
        try :
            semester=int(request.form['semester'])
        except ValueError:
            message = 'Semester must be an integer'
            return redirect(url_for('admin_courses',cid=message))
        courses = Courses.query.all()
        for i in courses:
            if cid == i.cid :
                message='Course id already exists'
        if message != 'Course id already exists' :
            tid=request.form['tid']
            new_course = Courses(cid=cid,cname=cname,ccredits=ccredits,semester=semester,teacherid=tid)
            db.session.add(new_course)
            db.session.commit()
            message = 'Course added successfully'
    return redirect(url_for('admin_courses',cid=message))

@app.route('/remove_course',methods=['GET','POST'])
def remove_course():
    if 'name' in session or 'tname' in session or 'aemail' not in session :
        return redirect(url_for('logout'))
    cid=request.form['cid']
    if 'cid' is not None or 'cid' != '' :
        course = Courses.query.filter_by(cid=cid).first()
        message='No such course exist'
        if course is not None :
            db.session.delete(course)
            db.session.commit()
            message='Course removed successfully'
    return redirect(url_for('.admin_courses',cid=message))

@app.route('/update_course',methods=['GET','POST'])
def update_course():
    if 'name' in session or 'tname' in session or 'aemail' not in session :
        return redirect(url_for('logout'))
    cid = request.args.get('cid')
    teacher = request.form['tid']
    if request.method == 'POST' :
        course = Courses.query.all()
        teachers=Teachers.query.all()
        found=False
        for i in teachers :
            if i.email == teacher:
                found=True
                break
        for i in course :
            if not found:
                cid='Teacher not found'
                break
            if i.cid == cid :
                i.teacherid = teacher
                db.session.commit()
    return redirect(url_for('.admin_courses',cid=cid))

@app.route('/promote', methods=['GET','POST'])
def promote():
    if 'name' in session or 'tname' in session or 'aemail' not in session :
        return redirect(url_for('logout'))
    message=''
    if request.method == 'POST':
        students=Student.query.all()
        for i in students:
            if i.semester == None:
                i.semester = 0
            i.semester=i.semester+1
        db.session.commit()
        message='Promoted Successfully'
    return redirect(url_for('admin_courses',cid=message))

@app.route('/demote', methods=['GET','POST'])
def demote():
    if 'name' in session or 'tname' in session or 'aemail' not in session :
        return redirect(url_for('logout'))
    message=''
    if request.method == 'POST':
        students=Student.query.all()
        for i in students:
            if i.semester == None:
                i.semester = 0
            i.semester=i.semester-1
        db.session.commit()
        message='Demoted Successfully'
    return redirect(url_for('admin_courses',cid=message))

@app.route('/admin_courses', methods=['GET','POST'])
def admin_courses():
    if 'name' in session or 'tname' in session:
        return redirect(url_for('logout'))
    cid = request.args.get('cid')
    if request.method == 'GET' :
        if 'aemail' in session:
            if cid == 'course' or cid == '' or cid == None :
                cid = ''
            if cid == '' or cid == 'Course removed successfully' or cid == 'No such course exist' or cid == 'Course added successfully' or cid == 'Course id already exists' or cid == 'Semester must be an integer' or cid == 'Teacher not found' or cid == 'Promoted Successfully' or cid == 'Demoted Successfully' :
                return render_template('admin_courses.html',name=cid)
            course = Courses.query.all()
            for i in course :
                if i.cid == cid :
                    return render_template('update_course.html',cid=cid,cname=i.cname,ccredits=i.ccredits,semester=i.semester,tid=i.teacherid)
            return render_template('admin_courses.html',name='No course found with course id '+ cid )
    if request.method == 'POST' :
        if 'aemail' in session:
            cid=request.form['cid']
            if cid != '' or cid == None :
                return redirect(url_for('.admin_courses',cid=cid))
            return redirect(url_for('.admin_courses',cid='course'))
    return redirect(url_for('logout'))

@app.route('/teacher_marks', methods=['GET','POST'])
def teacher_marks():
    if 'name' in session or 'aemail' in session or 'temail' not in session:
        return redirect(url_for('logout'))
    message=''
    if request.method=='POST' :
        cid=request.form['cid']
        email=request.form['roll']
        marks=0
        try:
            marks=int(request.form['marks'])
        except ValueError:
            return render_template('teacher_marks.html',message='Invalid Marks')
        course=Courses.query.filter_by(cid=cid).first()
        if course==None:
            return render_template('teacher_marks.html',message='Invalid Course')
        if course.teacherid!=session['temail']:
            return render_template('teacher_marks.html',message='You are not assigned to the requested course')
        student=Student.query.filter_by(email=email).first()
        if student==None:
            return render_template('teacher_marks.html',message='Invalid Student')
        if student.semester < course.semester:
            return render_template('teacher_marks.html',message='Student is not eligible to take the given course')
        mrow=Marks.query.filter_by(cid=cid,sid=student.roll_no).first()
        if mrow==None:
            mrow=Marks(cid=cid,sid=student.roll_no,marks=marks)
            db.session.add(mrow)
            db.session.commit()
        else:
            mrow.marks=marks
            db.session.commit()
            message='Marks updated successfully'
    return render_template('teacher_marks.html',message=message)

@app.route('/teacher_dashboard', methods=['GET','POST'])
def teacher_dashboard():
    if 'name' in session or 'aemail' in session:
        return redirect(url_for('logout'))
    if request.method == 'GET':
        count=0
        c1=''
        c2=''
        c3=''
        c4=''
        if 'temail' in session:
            courses=Courses.query.all()
            for i in courses:
                if i.teacherid==session['temail']:
                    count=count+1
                    if count==1:
                        c1=str(count)+". "+i.cid+" "+i.cname
                    if count==2:
                        c2=str(count)+". "+i.cid+" "+i.cname
                    if count==3:
                        c3=str(count)+". "+i.cid+" "+i.cname
                    if count==4:
                        c4=str(count)+". "+i.cid+" "+i.cname
            return render_template('teacher_course.html',course1=c1,course2=c2,course3=c3,course4=c4)
    return redirect(url_for('logout'))

@app.route('/marks/<filename>')
def marks(filename):
    filen="user.png"
    person = Student.query.all()
    for i in person:
        if i.roll_no == session['roll_no']:
            if i.image_url != None :
                filen = i.image_url
            break
    return render_template('marks.html',filename=filen,semister=filename)

@app.route('/register',methods=['GET','POST'])
def register():
    if 'tname' in session or 'name' in session or 'aemail' in session:
        return redirect(url_for('logout'))
    if request.method == 'POST':
        name = request.form['Name']
        email  = request.form['Email']
        password = request.form['Password']
        if name == "" or email == "" or password == "" :
            return redirect(url_for('register'))
        person = Student.query.all()
        for i in person:
            if i.email == email:
                return render_template('register.html',name='Email already registered')
        teachers = Teachers.query.all()
        for i in teachers:
            if i.email == email:
                return render_template('register.html',name='Email already registered')
        if request.form.get('teacher'):
            signature = Teachers(name=name,email=email,password=password)
            db.session.add(signature)
            db.session.commit()
            return redirect(url_for('login'))
        signature = Student(name=name,email=email,password=password,semester=1)
        db.session.add(signature)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html",name="")
    
@app.route('/login',methods=['GET','POST'])

def login():
    if 'tname' in session or 'name' in session or 'aemail' in session:
        return redirect(url_for('logout'))
    if request.method == 'POST':
        email  = request.form['Email']
        password = request.form['Password']
        if email is "":
            return redirect(url_for('login'))
        if request.form.get('teacher'):
            teacher = Teachers.query.all()
            for i in teacher: 
                if i.email == email and i.password == password:
                    session['temail'] = email
                    session['tname'] = i.name
                    return redirect(url_for('teacher_dashboard'))
            return render_template('main.html',name="You are not registered teacher")
        if request.form.get('admin'):
            admin = Admin.query.all()
            for i in admin: 
                if i.email == email and i.password == password:
                    session['aemail'] = email
                    return redirect(url_for('.admin_courses',cid='course'))
            return render_template('main.html',name="You are not registered admin")
        person = Student.query.all()
        for i in person:
            if i.email == email and i.password==password:
                session['email']=email
                session['name']=i.name
                session['roll_no']=i.roll_no
                return redirect(url_for('dashboard'))
        return render_template('main.html',name = "Yor are not a registered user!")
    return render_template('main.html',name="")

@app.route('/',methods=['GET','POST'])
def main():
    if 'tname' in session or 'name' in session or 'aemail' in session:
        return redirect(url_for('logout'))
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)