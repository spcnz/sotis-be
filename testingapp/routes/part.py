from flask import Blueprint, request, jsonify
from testingapp import db
from testingapp.models.testmodels import Test, Subject, Part

part_bp = Blueprint('part', __name__)


@part_bp.route('/test/<test_id>/part', methods=['POST'])
def create_part(test_id):
    data = request.json

    navigation_mode = ''
    submission_mode = ''
    time_dependency = data.get('time_dependency', False)
    test_id = data.get('test_id')

    new_part = Part(navigation_mode=navigation_mode, submission_mode=submission_mode,
                    time_dependency=time_dependency, test_id=test_id)
    db.session.add(new_part)
    db.session.commit()
    return jsonify(new_part)

