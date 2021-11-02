from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Test, Subject

option_bp = Blueprint('option', __name__)


@option_bp.route('/option', methods=['POST'])
def create_option():
    try:
        data = request.json
        title = data.get('title', 'NO TITLE')
        time_dependency = data.get('time_dependency', False)
        subject_id = data.get('subject_id')
        new_test = Test(title, time_dependency, subject_id=subject_id)
        db.session.add(new_test)
        db.session.commit()
        return jsonify(new_test)
    except Exception as error:
        print(error)
        return Response(status=400)
