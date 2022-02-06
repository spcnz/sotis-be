from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Option

option_bp = Blueprint('option', __name__)


@option_bp.route('/option', methods=['POST'])
def create_option():
    try:
        data = request.json
        name = data.get('name')
        label = data.get('label')
        item_id = data.get('item_id')
        correct_answer = data.get('correct_answer')

        new_option = Option(item_id=item_id, name=name, label=label, is_correct=correct_answer)
        db.session.add(new_option)
        db.session.commit()
        return jsonify(new_option.to_dict())
    except Exception as error:
        print(error)
        return Response(status=400)



@option_bp.route('/option', methods=['GET'])
def get_item_options():
    data = request.json
    item_id = request.args.get('item_id')
    print(item_id)
    options = Option.query.filter_by(item_id = item_id).all()

    return jsonify([option.to_dict() for option in options])