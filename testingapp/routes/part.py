from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Test, Subject, Part, OptionResult
from testingapp.utils.authutils import get_user_if_logged_in
from testingapp.models.enums import NavigationMode, SubmissionMode
from flask_jwt_extended import jwt_required


part_bp = Blueprint('part', __name__)


@part_bp.route('/test/<test_id>/part', methods=['POST'])
def create_part(test_id):
    data = request.json
    title = data.get("title")
    navigation_values = set(item.value for item in NavigationMode)
    submission_values = set(item.value for item in SubmissionMode) 
    navigation_mode = NavigationMode[data.get("navigation_mode")] if data.get("navigation_mode") in navigation_values else NavigationMode.LINEAR
    submission_mode = SubmissionMode[data.get("submission_mode")] if data.get("submission_mode") in submission_values else SubmissionMode.SIMULTANEOUS

    new_part = Part(navigation_mode=navigation_mode, submission_mode=submission_mode,test_id=test_id, title=title)
    db.session.add(new_part)
    db.session.commit()
    return jsonify(new_part.to_dict())


@part_bp.route('/part', methods=['GET'])
def get_test_parts():
    data = request.json
    test_id = request.args.get('test_id')
    parts = Part.query.filter_by(test_id = test_id).all()

    return jsonify([part.to_dict() for part in parts])

@part_bp.route('/part/submit', methods=['POST'])
@jwt_required
def submit_responses():
    try:
        data = request.json
        responses = data.get('responses')
        user = get_user_if_logged_in()
        for response in responses:
            checked = response.get('checked')
            test_id = response.get('test_id')
            option_id = response.get('option_id')
            result = OptionResult(checked=checked, test_id=test_id, option_id=option_id, student_id=user.id)
            db.session.merge(result)

        
        db.session.commit()
        return Response(status=200)
    except Exception as error:
        print(error)
        return Response(status=400)
