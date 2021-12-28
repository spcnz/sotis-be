import datetime
from sqlalchemy_serializer import SerializerMixin
from testingapp import db
from .enums import NavigationMode, SubmissionMode
from .usermodels import subject_teacher, subject_student

SectionRelationship = db.Table(
    'sections_related',
    db.Column('section_from', db.Integer, db.ForeignKey('sections.id')),
    db.Column('section_to', db.Integer, db.ForeignKey('sections.id'))
    )
test_part = db.Table('test_part',
                           db.Column('test_id', db.Integer, db.ForeignKey('tests.id')),
                           db.Column('part_id', db.Integer, db.ForeignKey('parts.id'))
                           )

class Subject(db.Model, SerializerMixin):
    __tablename__ = 'subjects'
    serialize_rules = ('-tests', '-students')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    points = db.Column(db.Integer)
    teachers = db.relationship("Teacher", secondary=subject_teacher)
    students = db.relationship("Student", secondary=subject_student)
    tests = db.relationship('Test', back_populates='subject')


class ItemResult(db.Model, SerializerMixin):
    __table__name = "item_result"
    id = db.Column(db.Integer, primary_key=True)
    serialize_rules = ()

    student = db.relationship('Student', backref='item_result')
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    item = db.relationship('Item', backref='item_result')
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    is_correct = db.Column(db.Boolean(), default=False)

class Test(db.Model, SerializerMixin):
    __tablename__ = 'tests'

    serialize_rules = ('-subject', '-item_result')
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    time_dependency = db.Column(db.Boolean(), default=False)
    time_limit_seconds = db.Column(db.Integer, default=600)

    subject = db.relationship("Subject", back_populates="tests")
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    parts = db.relationship("Part", secondary=test_part)



class Part(db.Model, SerializerMixin):
    __tablename__ = 'parts'
    serialize_rules = ('-sections.part', '-test')

    def submission(self):
        return self.submission_mode.name

    def navigation(self):
        return self.navigation_mode.name

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    navigation_mode = db.Column(db.Enum(NavigationMode), default=NavigationMode.NON_LINEAR)
    submission_mode = db.Column(db.Enum(SubmissionMode), default=SubmissionMode.SIMULTANEOUS)

    sections = db.relationship("Section", backref="part", lazy='dynamic')



class Section(db.Model, SerializerMixin):
    __tablename__ = 'sections'
    serialize_rules = ('-sections_to', '-part', '-sections_from')


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'))
    items = db.relationship("Item", backref="section", lazy='dynamic')
    sections_to = db.relation(
                    'Section',secondary=SectionRelationship,
                    primaryjoin=SectionRelationship.c.section_from==id,
                    secondaryjoin=SectionRelationship.c.section_to==id,
                    backref="sections_from")


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    serialize_rules = ('-section', '-options.item', '-item_result')

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text(), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    max_choices = db.Column(db.Integer, default=1)
    options = db.relationship("Option", backref="item", lazy='dynamic')


class Option(db.Model, SerializerMixin):
    __tablename__ = 'options'

    serialize_rules = ('-item', '-option_result', '-correct_answer')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    label = db.Column(db.String(30), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    is_correct = db.Column(db.Boolean, default=False)
