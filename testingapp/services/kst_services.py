from .kst import iita
import pandas as pd


def create_df(query_set):
    student_ids = {result.student_id for result in query_set}
    item_ids = {result.item_id for result in query_set}
    df_dict = {item_id: [] for item_id in item_ids}

    for item in item_ids:
        for student in student_ids:
            is_correct_answer = get_answer(query_set, student, item)
            df_dict[item].append(is_correct_answer)

    print(pd.DataFrame(df_dict))

    return (item_ids, pd.DataFrame(df_dict))


def create_knowledge_space(df, version):
    return iita(df, version)


def get_answer(query_set, student_id, item_id):
    item_result = None

    for result in query_set:
        if result.student_id == student_id and result.item_id == item_id:
            item_result = result

    return int(item_result.is_correct) if item_result is not None else 0
