from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Subject

subject_bp = Blueprint('subject', __name__)


@subject_bp.route('/subject', methods=['POST'])
def create_subject():
    try:
        data = request.json
        name = data.get('name', 'NO NAME')
        description = data.get('description', '')
        points = data['points']
        teachers = data.get('teachers', [])
        students = data.get('students', [])

        new_subject = Subject(name=name, description=description, points=points)
        db.session.add(new_subject)
        db.session.commit()
        return jsonify(new_subject.to_dict())
    except Exception as error:
        print(error)
        return Response(status=400)

@subject_bp.route('/subject', methods=['GET'])
def get_all():
    return jsonify([sub.to_dict() for sub in Subject.query.all()])
