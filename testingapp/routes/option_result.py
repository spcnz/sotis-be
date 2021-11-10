from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import OptionResult
from testingapp.utils.authutils import get_user_if_logged_in
from flask_jwt_extended import jwt_required

option_result_bp = Blueprint('option_result', __name__)


@option_result_bp.route('/option-result', methods=['POST'])
@jwt_required
def submit_response():
    try:
        data = request.json
        checked = data.get('checked')
        user = get_user_if_logged_in()
        test_id = data.get('test_id')
        option_id = data.get('option_id')
        result = OptionResult(checked=checked, test_id=test_id, option_id=option_id, student_id=user.id)
        db.session.merge(result)
        db.session.commit()
        return jsonify(result.to_dict())
    except Exception as error:
        print(error)
        return Response(status=400)
