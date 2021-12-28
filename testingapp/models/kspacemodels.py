import datetime
from sqlalchemy_serializer import SerializerMixin
from testingapp import db
from .testmodels import Section

ProblemRelationship = db.Table(
    'problems_related',
    db.Column('source', db.Integer, db.ForeignKey('kspaces.id')),
    db.Column('target', db.Integer, db.ForeignKey('kspaces.id'))
    )

#Many to many relationship between section and kspace model
section_kspace = db.Table('section_kspace',
                           db.Column('section_id', db.Integer, db.ForeignKey('sections.id')),
                           db.Column('kspace_id', db.Integer, db.ForeignKey('kspaces.id'))
                           )

class KnowledgeSpace(db.Model, SerializerMixin):
    __tablename__ = 'kspaces'

    serialize_rules = ('-source_problems',)


    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('parts.id'))
    problem = db.relationship("Section", secondary=section_kspace)
    probability = db.Column(db.Float, nullable=True)
    iita_generated = db.Column(db.Boolean, default=False)

    #this node is pointing to target_problems
    #source_problems are pointing to this node
    target_problems = db.relation(
                    'KnowledgeSpace',secondary=ProblemRelationship,
                    primaryjoin=ProblemRelationship.c.source==id,
                    secondaryjoin=ProblemRelationship.c.target==id,
                    backref="source_problems",
                    cascade="all, delete")