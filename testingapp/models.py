import datetime
import enum
from testingapp import db, flask_bcrypt, app
import jwt
from sqlalchemy_serializer import SerializerMixin

subject_teacher = db.Table('subject_teacher',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('students.id'))
)
subject_student = db.Table('subject_student',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('students.id'))
)


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-password_hash')
      
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(100))
    role = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'users',
        'polymorphic_on':role
    }


    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.email)

class Admin(User, SerializerMixin):
    __tablename__ = 'admins'

    __mapper_args__ = {
        'polymorphic_identity':'admin'
    }

    serialize_rules = ('-password_hash')
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)


class Student(User, SerializerMixin):
    __tablename__ = 'students'

    __mapper_args__ = {
        'polymorphic_identity':'student'
    }

    serialize_rules = ('-password_hash')
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    card_num = db.Column(db.String(20), nullable=False, unique=True)
    year_of_study = db.Column(db.Integer, nullable=False)
    subjects = db.relationship("Subject", secondary=subject_student)



class Teacher(User, SerializerMixin):
    __tablename__ = 'teachers'

    __mapper_args__ = {
        'polymorphic_identity':'student'
    }

    serialize_rules = ('-password_hash')
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    title = db.Column(db.String(50))
    subjects = db.relationship("Subject", secondary=subject_teacher)

class Subject(db.Model, SerializerMixin):

    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    points = db.Column(db.Integer)
    teachers = db.relationship("Teacher", secondary=subject_teacher)
    students = db.relationship("Student", secondary=subject_student)
    tests = db.relationship("Test", backref="subject", lazy='dynamic')


class Test(db.Model, SerializerMixin):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    time_dependancy = db.Column(db.Boolean(), default=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    subject = db.relationship('Subject')
    parts = db.relationship("Part", backref="test", lazy='dynamic')


class Navigation_Mode(enum.Enum):
    LINEAR = 1
    NON_LINEAR = 2

class Submission_Mode(enum.Enum):
    INDIVIDUAL = 1
    SIMULTANEOUS = 2


class Part(db.Model, SerializerMixin):
    __tablename__ = 'parts'

    id = db.Column(db.Integer, primary_key=True)
    navigation_mode = db.Column(db.Enum(Navigation_Mode), default=Navigation_Mode.NON_LINEAR)
    submission_mode = db.Column(db.Enum(Submission_Mode), default=Submission_Mode.SIMULTANEOUS)
    time_dependancy = db.Column(db.Boolean(), default=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    test = db.relationship('Test')
    sections = db.relationship("Section", backref="part", lazy='dynamic')



class Section(db.Model, SerializerMixin):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    time_dependancy = db.Column(db.Boolean(), default=False)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'))
    part = db.relationship('Part')
    items = db.relationship("Item", backref="section", lazy='dynamic')


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    time_dependancy = db.Column(db.Boolean(), default=False)
    correct_answer = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text(), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    section = db.relationship('Section')