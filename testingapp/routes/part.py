from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Test, Subject, Part
from testingapp.utils.authutils import get_user_if_logged_in
from testingapp.models.enums import NavigationMode, SubmissionMode
from flask_jwt_extended import jwt_required


part_bp = Blueprint('part', __name__)


@part_bp.route('/test/part', methods=['POST'])
def create_part():
    data = request.json
    title = data.get("title")
    navigation_values = set(item.value for item in NavigationMode)
    submission_values = set(item.value for item in SubmissionMode) 
    navigation_mode = NavigationMode[data.get("navigation_mode")] if data.get("navigation_mode") in navigation_values else NavigationMode.LINEAR
    submission_mode = SubmissionMode[data.get("submission_mode")] if data.get("submission_mode") in submission_values else SubmissionMode.SIMULTANEOUS

    new_part = Part(navigation_mode=navigation_mode, submission_mode=submission_mode, title=title)
    db.session.add(new_part)
    db.session.commit()
    return jsonify(new_part.to_dict())

@part_bp.route('/part', methods=['GET'])
def get_all_parts():
    data = request.json
    parts = Part.query.all()

    return jsonify([part.to_dict() for part in parts])
