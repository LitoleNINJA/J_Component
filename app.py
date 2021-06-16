from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cms2.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class CMS(db.Model) :
    sno = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100), nullable=False)
    l_name = db.Column(db.String(100))
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f"{self.username} - {self.f_name}"

class Student(db.Model) :
    reg_no = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer)
    batch = db.Column(db.String(50), nullable=False)
    grad_year = db.Column(db.Integer)


class Faculty(db.Model) :
    reg_no = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer)
    email = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.String(50), nullable=False)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up', methods=['POST'])
def sign_up():
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    login = CMS(f_name=f_name, l_name=l_name, email=email, username=username, password=password)
    db.session.add(login)
    db.session.commit()
    return render_template('index.html', f_name=f_name, l_name=l_name)

@app.route('/student')
def student():
    allcms = CMS.query.all()
    return render_template('student.html', allcms=allcms)




# FACULTY
@app.route('/faculty')
def faculty():
    return render_template('faculty.html')

@app.route('/faculty_view')
def facultyview():
    allFaculty = Faculty.query.all()
    return render_template('faculty_view.html', allFaculty=allFaculty)

@app.route('/faculty_view', methods=['POST'])
def faculty_view():
    reg_no = request.form['reg_no']
    faculty = Faculty.query.filter_by(reg_no=reg_no)
    return render_template('faculty_view.html', faculty=faculty)

@app.route('/faculty_add')
def facultyadd():
    return render_template('faculty_add.html')

@app.route('/faculty_add', methods=['POST'])
def faculty_add():
    reg_no = request.form['reg_no']
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    rank = request.form['rank']
    print(reg_no, name)
    fac = Faculty(reg_no=reg_no, name=name, phone=phone, email=email, rank=rank)
    db.session.add(fac)
    db.session.commit()
    return render_template('faculty_add.html', name=name)

@app.route('/faculty_edit')
def facultyedit():
    allFaculty = Faculty.query.all()
    return render_template('faculty_del.html', allFaculty=allFaculty)

@app.route('/faculty_edit', methods=['POST'])
def faculty_edit():
    reg_no = request.form['reg_no']
    faculty = Faculty.query.filter_by(reg_no=reg_no).first()
    db.session.delete(faculty)
    db.session.commit()
    return render_template('faculty_del.html', faculty=faculty)



@app.route('/courses')
def courses():
    return render_template('courses.html')

if __name__ == '__main__':
    app.run(debug=True)