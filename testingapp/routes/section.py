from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Part

section_bp = Blueprint('section', __name__)

@section_bp.route('/section', methods=['POST'])
def create_section():
    try:
        data = request.json
        title = data.get('title', 'NO TITLE')
        time_dependency = data.get('time_dependency', False)
        part_id = data.get('part_id')

        new_test = Part(title, time_dependency, part_id=part_id)
        db.session.add(new_test)
        db.session.commit()
        return jsonify(new_test)
    except Exception as error:
        print(error)
        return Response(status=400)