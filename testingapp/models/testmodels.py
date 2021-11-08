import datetime
from sqlalchemy_serializer import SerializerMixin
from testingapp import db
from .enums import Grade, NavigationMode, SubmissionMode
from .usermodels import subject_teacher, subject_student


class Subject(db.Model, SerializerMixin):
    __tablename__ = 'subjects'
    serialize_rules = ('-tests.subject_id', '-tests.subject')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    points = db.Column(db.Integer)
    teachers = db.relationship("Teacher", secondary=subject_teacher)
    students = db.relationship("Student", secondary=subject_student)
    tests = db.relationship('Test', back_populates='subject')


class TestResult(db.Model):
    __table__name = 'test_results'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.datetime.now)
    points = db.Column(db.Float, nullable=True)
    grade = db.Column(db.Enum(Grade), default=Grade.F)

    student = db.relationship('Student', backref='test_results')
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    test = db.relationship('Test', backref='test_results')
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))


class Test(db.Model, SerializerMixin):
    __tablename__ = 'tests'
    serialize_rules = ('-parts.test', '-subject.tests')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    time_dependency = db.Column(db.Boolean(), default=False)
    time_limit_seconds = db.Column(db.Integer, default=600)

    subject = db.relationship("Subject", back_populates="tests")
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    parts = db.relationship("Part", backref="test", lazy='dynamic')


class Part(db.Model, SerializerMixin):
    __tablename__ = 'parts'
    serialize_rules = ('-sections', '-test')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    navigation_mode = db.Column(db.Enum(NavigationMode), default=NavigationMode.NON_LINEAR)
    submission_mode = db.Column(db.Enum(SubmissionMode), default=SubmissionMode.SIMULTANEOUS)

    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    sections = db.relationship("Section", backref="part", lazy='dynamic')


class Section(db.Model, SerializerMixin):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'))
    items = db.relationship("Item", backref="section", lazy='dynamic')


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    serialize_rules = ('-options', '-section')

    interaction = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': interaction
    }

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text(), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    max_choices = db.Column(db.Integer, default=1)
    options = db.relationship("Option", backref="item", lazy='dynamic')


class Option(db.Model, SerializerMixin):
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    label = db.Column(db.String(10), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    correct_answer = db.Column(db.Boolean, default=False)
    checked = db.Column(db.Boolean, default=False)
