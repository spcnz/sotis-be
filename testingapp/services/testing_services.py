import numpy as np
from random import randrange

from testingapp import db
from testingapp.models.kspacemodels import KnowledgeSpace
from testingapp.services.kspace_service import init_probs_by_domain


def get_next_question(domain_id):
    best_state = questioning_rule(domain_id)
    print(best_state, " PROBLEMI")

    possible_questions = [section.items for section in best_state.problem]
    index = randrange(len(possible_questions))
    print("INDEX ", index)
    print(possible_questions[index].first())

    return possible_questions[index].first() if best_state.target_problems is not None else None


def questioning_rule(domain_id):
    try:
        all_states = KnowledgeSpace.query.filter_by(domain_id=domain_id, iita_generated=True)
        Ln = np.array([np.abs(2 * state.probability - 1) for state in all_states])
        min_index = np.argmin(Ln)
        return all_states[min_index]
    except:
        init_probs_by_domain(domain_id)
        all_states = KnowledgeSpace.query.filter_by(domain_id=domain_id, iita_generated=True)
        Ln = np.array([np.abs(2 * state.probability - 1) for state in all_states])
        min_index = np.argmin(Ln)
        return all_states[min_index]


def update_rule(domain_id, item_result):
    all_states = KnowledgeSpace.query.filter_by(domain_id=domain_id, iita_generated=True)
    Ln = {state.id: calculate_likelihood(state, item_result) for state in all_states}

    for state in all_states:
        numerator = Ln[state.id]
        denominator = np.sum([Ln[iter_state.id] for iter_state in all_states if iter_state != state])
        state.probability = numerator / denominator

    db.session.commit()


def calculate_likelihood(current_state, item_result):
    item = item_result.item

    r = bool(item_result.is_correct)

    ni = 1.2 if (item.section.id in [problem.id for problem in current_state.problem]) == r else 1
    print(ni, ' je ni')

    return ni * current_state.probability
