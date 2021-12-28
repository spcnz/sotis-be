from .kst import iita
import pandas as pd


def create_df(sections_qs, results_qs):
    student_ids = {result.student_id for result in results_qs}
    section_ids = {section.id for section in sections_qs}
    df_dict = {section_id: [] for section_id in section_ids}

    for section in section_ids:
        for student in student_ids:
            is_correct_answer = get_answer(results_qs, student, section)
            df_dict[section].append(is_correct_answer)

    return (section_ids, pd.DataFrame(df_dict))


def create_knowledge_space(df, version):
    return iita(df, version)


def get_answer(results_qs, student_id, section_id):
    section_results = 0
    items_count = 0

    for result in results_qs:
        if result.student_id == student_id and result.item.section.id == section_id:
            section_results += int(result.is_correct)
            items_count += 1
    result = section_results / (items_count or 1)

    return int(result > 0.5)

