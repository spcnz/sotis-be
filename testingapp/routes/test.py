from flask import Blueprint, request, jsonify, Response, send_file
from testingapp import db
from testingapp.models.testmodels import Test, Subject
from testingapp.models.usermodels import User
from testingapp.models.kspacemodels import KnowledgeSpace
from testingapp.utils.authutils import get_user_if_logged_in
from flask_jwt_extended import jwt_required, get_jwt_identity
from testingapp.services.kspace_service import init_probs
import zipfile
import os

test_bp = Blueprint('test', __name__)


@test_bp.route('/test', methods=['GET'])
@jwt_required
def get_all():
    subject_id = request.args.get('subject_id')
    
    return jsonify([test.to_dict(only=('id', 'title')) for test in Test.query.filter_by(subject_id=subject_id)])


@test_bp.route('/test', methods=['POST'])
def create_test():
    try:
        user = get_user_if_logged_in()
        if not user or user.role != 'teacher':
            return Response(status=400)

        data = request.json
        title = data.get('title', 'NO TITLE')
        time_dependency = bool(data.get('time_dependency', False))
        subject_id = data.get('subject_id')
        new_test = Test(title=title, time_dependency=time_dependency, subject_id=subject_id)
        db.session.add(new_test)
        db.session.commit()

        return jsonify(new_test.to_dict())
    except Exception as error:
        print(error)
        return Response(status=400)


@test_bp.route('/test/<id>', methods=['GET'])
@jwt_required
def get_by_id(id):
    test = Test.query.get(id)
    if not test:
        return Response(status=400)


    return jsonify(test.to_dict())

@test_bp.route('/test/<id>/guided', methods=['GET'])
def start_test(id):
    test = Test.query.get(id)
    if not test:
        return Response(status=400)
    #set a priori probability
    kspace = init_probs(test)
    #vrati prvo pitanje (?)
    return jsonify([])

@test_bp.route('/test/<id>/export', methods=['GET'])
def export_test(id):
    test = Test.query.get(id)
    if not test:
        return Response(status=400)
    xml = ("<?xml version='1.0' encoding='UTF-8'?>"
            "<qti-assessment-test "
            "xmlns=\"http://www.imsglobal.org/xsd/imsqti_v3p0\" "
            "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
            f"identifier=\"{test.id}\" "
            f"title=\"{test.title}\" "
            "xsi:schemaLocation=\"http://www.imsglobal.org/xsd/imsqti_v3p0 "
            "https://purl.imsglobal.org/spec/qti/v3p0/xsd/imsqti_asiv3p0_v1p0.xsd\" "
            "xml:lang=\"en-US\"> ")

    for part in test.parts:
        xml += ("<qti-test-part "
                f"identifier=\"{part.id}\" "
                f"navigation-mode=\"{part.navigation_mode.name.lower()}\" "
                f"submission-mode=\"{part.submission_mode.name.lower()}\">")
        for section in part.sections:
            xml += section_xml(section)
            for item in section.items:
                xml += generate_item_xml(item, test.id)
            xml += "</qti-assessment-section>"
        xml += "</qti-test-part>"
    xml += "</qti-assessment-test>"

    with open(f"xml/Test-{test.id}.xml", "w") as fo:
        fo.write(xml)

    zipf = zipfile.ZipFile(f'testingapp/zip/Test-{test.id}.zip','w', zipfile.ZIP_DEFLATED)
    for root,dirs, files in os.walk('xml'):
        for file in files:
            zipf.write(f'xml/{file}')
    zipf.close()

    return send_file(f'zip/Test-{test.id}.zip',
            mimetype = 'zip',
            attachment_filename= f'Test-{test.id}.zip',
            as_attachment = True)


def section_xml(section):
    return (" <qti-assessment-section "
            f"identifier=\"{section.id}\" "
            f"title=\"{section.title}\" "
            "visible=\"true\">")

def generate_item_xml(item, test_id):
    xml = ("<?xml version='1.0' encoding='UTF-8'?>"
            "<qti-assessment-item "
            "xmlns=\"http://www.imsglobal.org/xsd/qti/imsqtiasi_v3p0\" "
            "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
            "xsi:schemaLocation=\"http://www.imsglobal.org/xsd/imsqtiasi_v3p0 "
            "https://www.imsglobal.org/xsd/qti/qtiv3p0/imsqti_itemv3p0_v1p0.xsd\" "
            f"identifier=\"test-{test_id}-item-{item.id}\" "
            "time-dependent=\"false\" " 
            "xml:lang=\"en-US\"> ")

    item_cardinality = "multiple" if item.max_choices > 1 else "single"
    xml += ("<qti-response-declaration "
                "base-type=\"identifier\" "
                f"cardinality=\"{item_cardinality}\" "
                "identifier=\"RESPONSE\"> "
                "<qti-correct-response>")
    for option in item.options:
        if option.is_correct:
            xml += f"<qti-value>{option.name}</qti-value>"
    xml += "</qti-correct-response> </qti-response-declaration>"
    
    xml += ("<qti-outcome-declaration base-type=\"float\" cardinality=\"single\" identifier=\"SCORE\">"
            "<qti-default-value><qti-value>1</qti-value></qti-default-value>"
            "</qti-outcome-declaration>")

    xml += ("<qti-item-body>"
            f"<p>{item.question}</p>"
            f"<qti-choice-interaction max-choices=\"{item.max_choices}\" min-choices=\"1\" response-identifier=\"RESPONSE\" >")
    for option in item.options:
        xml += f"<qti-simple-choice identifier=\"{option.name}\">{option.label}</qti-simple-choice>"
    xml += "</qti-choice-interaction></qti-item-body>"

    xml += "</qti-assessment-item>"
    with open(f"xml/test-{test_id}-item-{item.id}.xml", "w") as fo:
        fo.write(xml)

    return ("<qti-assessment-item-ref "
            f"identifier=\"test-{test_id}-item-{item.id}\" "
            f"href=\"test-{test_id}-item-{item.id}.xml\" />")



