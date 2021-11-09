from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Item

item_bp = Blueprint('item', __name__)


@item_bp.route('/item', methods=['POST'])
def create_item():
    try:
        data = request.json
        score = data.get('score')
        question = data.get('question')
        section_id = data.get('section_id')
        max_choices = data.get('max_choices')

        new_item = Item(score=score, question=question, section_id=section_id, max_choices=max_choices)
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict())
    except Exception as error:
        print(error)
        return Response(status=400)


@item_bp.route('/item', methods=['GET'])
def get_section_items():
    data = request.json
    section_id = request.args.get('section_id')
    print(section_id)
    items = Item.query.filter_by(section_id = section_id).all()

    return jsonify([item.to_dict() for item in items])

