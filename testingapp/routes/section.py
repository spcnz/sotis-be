from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.testmodels import Section
from testingapp.models.kspacemodels import KnowledgeSpace

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

        kspace = KnowledgeSpace(domain_id=part_id, iita_generated=False)
        kspace.problem.append(new_section)
        db.session.add(kspace)
        db.session.commit()

        return jsonify(new_section.to_dict())
    except Exception as error:
        print(error)
        return Response(status=400)


@section_bp.route('/section/link', methods=['POST'])
def link_sections():
    try:
        data = request.json
        source = Section.query.get(data.get("source"))
        target = Section.query.get(data.get("target"))
        kspaces = KnowledgeSpace.query.filter_by(domain_id=source.part_id, iita_generated=False)
        source_kspace = None
        target_kspace = None
        for node in kspaces:
            if source in node.problem:
                source_kspace = node
            if target in node.problem:
                target_kspace = node
        source_kspace.target_problems.append(target_kspace)                

        db.session.commit()
        return Response(status=200)
    except Exception as error:
        print(error)
        return Response(status=400)


@section_bp.route('/section', methods=['GET'])
def get_part_sections():
    data = request.json
    part_id = request.args.get('part_id')
    print(part_id)
    sections = Section.query.filter_by(part_id = part_id).all()

    return jsonify([section.to_dict(rules=('-items','-part')) for section in sections])