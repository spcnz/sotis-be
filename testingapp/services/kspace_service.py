from testingapp.models.kspacemodels import KnowledgeSpace
from testingapp import db


def save_kspace(iita_kspace, section_ids):
    domen_id = 1
    nodes = {}
    for section_id in section_ids:
        kspace = KnowledgeSpace(
            domen_id=domen_id,
            iita_generated=True,
            problem=section_id
            )
        nodes[section_id] = kspace
    print(nodes)
    for source,target in iita_kspace.get("implications"):
        print(source, target)
        source_node = nodes[section_ids[source]]
        target_node = nodes[section_ids[target]]

        source_node.target_problems.append(target_node)
    for key, node in nodes.items():
        db.session.add(node)
    
    db.session.commit()


def init_probs(test):
    kspace = []
    for part in test.parts:
        nodes = KnowledgeSpace.query.filter_by(domen_id=part.id, iita_generated=True)
        for node in nodes:
            node.probability = (1.0) / nodes.count()
    db.session.commit()

    return kspace