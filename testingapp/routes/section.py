from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Section

section_bp = Blueprint('section', __name__)

@section_bp.route('/section', methods=['POST'])
def create_section():
    try:
        data = request.json
        title = data.get('title')
        part_id = data.get('part_id')
        print('heree')
        new_section = Section(title=title, part_id=part_id)
        db.session.add(new_section)
        db.session.commit()
        return jsonify(new_section.to_dict())
    except Exception as error:
        print(error)
        return Response(status=400)


@section_bp.route('/section', methods=['GET'])
def get_part_sections():
    data = request.json
    part_id = request.args.get('part_id')
    print(part_id)
    sections = Section.query.filter_by(part_id = part_id).all()

    return jsonify([section.to_dict() for section in sections])