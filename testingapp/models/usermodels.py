from testingapp import db, flask_bcrypt
from sqlalchemy_serializer import SerializerMixin

subject_teacher = db.Table('subject_teacher',
                           db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
                           db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'))
                           )
subject_student = db.Table('subject_student',
                           db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                           db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'))
                           )


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-password_hash', '-password')

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(100))
    role = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': role
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
        'polymorphic_identity': 'admin'
    }

    serialize_rules = ('-password_hash')
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)


class Student(User, SerializerMixin):
    __tablename__ = 'students'

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    serialize_rules = ('-password_hash')
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    card_num = db.Column(db.String(20), nullable=False, unique=True)
    year_of_study = db.Column(db.Integer, nullable=False)
    subjects = db.relationship("Subject", secondary=subject_student)


class Teacher(User, SerializerMixin):
    __tablename__ = 'teachers'

    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }

    serialize_rules = ('-password_hash')
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    title = db.Column(db.String(50))
    subjects = db.relationship("Subject", secondary=subject_teacher)
