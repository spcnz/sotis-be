from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Test, Subject

test_bp = Blueprint('test', __name__)

@test_bp.route('/test', methods=['GET'])
def get():
    #s = request.json()
    #print(s)
    s = Subject()
    test = Test(title="Test test hehe", time_dependency=True, subject_id=1)
    db.session.add(test)
    db.session.commit()
    new_test2 = Test.query.filter(Test.title=="Test test hehe").first()

    print(test.to_dict())  # mijenja mu indeks automatski objektu
    print(new_test2.to_dict())
    return "HVALA"


@test_bp.route('/test', methods=['POST'])
def create_test():
    try:
        data = request.json
        title = data.get('title', 'NO TITLE')
        time_dependency = bool(data.get('time_dependency', False))
        subject_id = data.get('subject_id')
        new_test = Test(title=title, time_dependency=time_dependency, subject_id=subject_id)
        db.session.add(new_test)
        db.session.commit()

        return jsonify(new_test.to_dict())
    except Exception as error:
        print(error)
        return Response(status=400)
