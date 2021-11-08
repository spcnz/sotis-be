from faker import Faker
from testingapp import db
from testingapp.models.usermodels import *
from testingapp.models.testmodels import *
from testingapp.models.enums import *
import random

fake = Faker()
emails = [fake.unique.email() for i in range(50)]
teachers = []
students = []
subjects = []

def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print ('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


clear_data(db.session)

def add_admin():
    admin = Admin(email=emails[0], first_name=fake.first_name(), last_name=fake.last_name(),password="123456")
    db.session.add(admin)
    db.session.commit()

def add_teachers():
    for i in range(1, 10):
        teacher = Teacher(
            email=emails[i], 
            first_name=fake.first_name(), 
            last_name=fake.last_name(),
            password="123456", 
            title=fake.prefix()
            )
        db.session.add(teacher)
        db.session.commit()
        teachers.append(teacher)

def add_students():
    for i in range(11, 20):
        student = Student(
            email=emails[i], 
            first_name=fake.first_name(), 
            last_name=fake.last_name(),
            password="123456", 
            year_of_study=random.choice([1, 2, 3, 4]), 
            card_num=fake.swift(length=8) + "/" + fake.year()
            )
        db.session.add(student)
        db.session.commit()
        students.append(student)

def add_subjects():
    for i in range(10):
        subject = Subject(
            name=fake.text(max_nb_chars=10), 
            description=fake.paragraph(),
            points=random.choice(range(2,10)) 
            )
        teacher_index = random.choice(range(0, len(teachers)))
        subject.teachers.append(teachers[teacher_index])
        for stud in students:
            subject.students.append(stud)
        db.session.add(subject)
        db.session.commit()
        subjects.append(subject)


def add_tests():
    parts = db.relationship("Part", backref="test", lazy='dynamic')

    for i in range(3):
        time_dependency = fake.boolean(chance_of_getting_true=50)
        test = Test(
            title=fake.text(max_nb_chars=10), 
            time_dependency=time_dependency,
            time_limit_seconds=(random.choice([900, 1800, 2700]) if time_dependency else 0),
            )
        subject_index = random.choice(range(0, len(subjects)))
        test.subject = subjects[subject_index]
        test.subject_id = subjects[subject_index].id
        db.session.add(test)
        db.session.commit()

        add_parts(test.id)

def add_parts(test_id):
    for i in range(3):
        part = Part(
            title=fake.text(max_nb_chars=10), 
            navigation_mode=random.choice([e.name for e in NavigationMode]),
            submission_mode=random.choice([e.name for e in SubmissionMode]),
            test_id=test_id
            )
        db.session.add(part)
        db.session.commit()

        add_sections(part.id)

def add_sections(part_id):
    for i in range(3):
        section = Section(
            title=fake.text(max_nb_chars=10), 
            part_id=part_id
            )
        db.session.add(section)
        db.session.commit()

        add_items(section.id)

def add_items(section_id):
    for i in range(3):
        max_choices=random.choice([1, 1, 3])
        item = Item(
            score=random.choice(range(2,5)), 
            question=fake.text(max_nb_chars=20) + " ?",
            max_choices=max_choices,
            section_id=section_id
            )
        db.session.add(item)
        db.session.commit()

        add_options(item.id, max_choices)


def add_options(item_id, max_choices):
    option_names = ['A', 'B', 'C', 'D', 'E']
    for i in range(5):
        option = Option(
            name=option_names[i], 
            label=fake.text(max_nb_chars=10),
            correct_answer=(max_choices > 0),
            item_id=item_id,
            )
        db.session.add(option)
        db.session.commit()
        max_choices = max_choices - 1

def add_test_result():
    pass

if __name__ == '__main__':
    add_admin()
    print("\nADDED ADMIN....\n")
    add_teachers()
    print("\nADDED TEACHERS....\n")
    add_students()
    print("\nADDED STUDENTS....\n")
    add_subjects()
    print("\nADDED SUBJECTS....")
    add_tests()
    print("\nADDED TESTS....\n")
    # add_test_result()
    # print("\nADDED TEST RESULTS....\n")