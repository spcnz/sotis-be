from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Item, Option, ItemResult
from testingapp.utils.authutils import get_user_if_logged_in

item_result_bp = Blueprint('item_result', __name__)


@item_result_bp.route('/item-result', methods=['POST'])
def create_item_result():
    try:
        user = get_user_if_logged_in()
        if not user: #or user.role != 'student':
            return Response(status=400)

        data = request.json
        is_correct = True
        for option in data['options']:
            option_obj = Option.query.filter_by(id=option['option_id']).first_or_404()
            is_correct = False if option_obj.is_correct != bool(option["checked"]) else is_correct

        item_id = data.get('item_id')
        new_result = ItemResult(is_correct=is_correct, student_id=user.id, item_id=item_id)

        db.session.add(new_result)
        db.session.commit()
        return jsonify(new_result.to_dict())
    except Exception as error:
        print(error)
        return Response(status=400)


@item_result_bp.route('/item-result', methods=['GET'])
def get_item_results():
    data = request.json
    result_id = request.args.get('result_id')
    items = ItemResult.query.filter_by(id=result_id).all()
    return jsonify([item.to_dict() for item in items])
