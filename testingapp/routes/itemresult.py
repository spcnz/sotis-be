from flask import Blueprint, request, jsonify, Response
from testingapp import db
from testingapp.models.kspacemodels import KnowledgeSpace
from testingapp.models.testmodels import Item, Option, ItemResult, Section
from testingapp.services.kst_services import create_knowledge_space, create_df
from testingapp.utils.authutils import get_user_if_logged_in
from testingapp.services.kspace_service import save_kspace

item_result_bp = Blueprint('itemresult', __name__)


@item_result_bp.route('/itemresult', methods=['POST'])
def create_item_result():
    try:
        user = get_user_if_logged_in()
        if not user: #or user.role != 'student':
            return Response(status=400)

        data = request.json
        responses = data.get("reponses")
        for item_response in responses:
            is_correct = True
            for option in item_response.get('options'):
                option_obj = Option.query.filter_by(id=option['option_id']).first_or_404()
                is_correct = False if option_obj.is_correct != bool(option["checked"]) else is_correct

            item_id = item_response.get('item_id')
            new_result = ItemResult(is_correct=is_correct, student_id=user.id, item_id=item_id)

            db.session.add(new_result)
            db.session.commit()
        
        return Response(status=200)
    except Exception as error:
        print(error)
        return Response(status=400)


@item_result_bp.route('/itemresult', methods=['GET'])
def get_item_results():
    data = request.json
    result_id = request.args.get('result_id')
    items = ItemResult.query.filter_by(id=result_id).all()
    return jsonify([item.to_dict() for item in items])

@item_result_bp.route('/itemresult/generate', methods=['GET'])
def create_ks():
    item_results_query_set = ItemResult.query.all()
    sections_query_set = Section.query.all()

    kspace = KnowledgeSpace.query.filter_by(domain_id=1)
    if (kspace.count() == 0):
        keys, df = create_df(sections_query_set, item_results_query_set)
        knowledge_space = create_knowledge_space(df, version=1)

        save_kspace(knowledge_space, list(keys),domain_id = 1)
        kspace = KnowledgeSpace.query.filter_by(domain_id=1)
    # add_full(1)
    return jsonify([node.to_dict(only=("id", "target_problems", "problem")) for node in kspace])
