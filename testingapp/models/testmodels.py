import datetime
from sqlalchemy_serializer import SerializerMixin
from testingapp import db
from .enums import Grade, NavigationMode, SubmissionMode
from .usermodels import subject_teacher, subject_student


class Subject(db.Model, SerializerMixin):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    points = db.Column(db.Integer)
    teachers = db.relationship("Teacher", secondary=subject_teacher)
    students = db.relationship("Student", secondary=subject_student)
    tests = db.relationship("Test", backref="subject", lazy='dynamic')


class TestResult(db.Model):
    __table__name = 'test_results'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.datetime.now)
    points = db.Column(db.Float, nullable=True)
    grade = db.Column(db.Enum(Grade), default=Grade.F)
    test = db.relationship('Test') # da li ti vraca samo PK od testa?


class Test(db.Model, SerializerMixin):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    time_dependency = db.Column(db.Boolean(), default=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    subject = db.relationship('Subject')
    parts = db.relationship("Part", backref="test", lazy='dynamic')


class Part(db.Model, SerializerMixin):
    __tablename__ = 'parts'

    id = db.Column(db.Integer, primary_key=True)
    navigation_mode = db.Column(db.Enum(NavigationMode), default=NavigationMode.NON_LINEAR)
    submission_mode = db.Column(db.Enum(SubmissionMode), default=SubmissionMode.SIMULTANEOUS)
    time_dependency = db.Column(db.Boolean(), default=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    test = db.relationship('Test')
    sections = db.relationship("Section", backref="part", lazy='dynamic')


class Section(db.Model, SerializerMixin):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    time_dependency = db.Column(db.Boolean(), default=False)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'))
    part = db.relationship('Part')
    items = db.relationship("Item", backref="section", lazy='dynamic')


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    interaction = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': interaction
    }

    id = db.Column(db.Integer, primary_key=True)
    time_dependency = db.Column(db.Boolean(), default=False)
    correct_answer = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text(), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    section = db.relationship('Section')
    max_choices = db.Column(db.Integer, default=1)
    options = db.relationship("Option", backref="item", lazy='dynamic')


class Option(db.Model, SerializerMixin):
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    label = db.Column(db.String(10), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship('Item')
