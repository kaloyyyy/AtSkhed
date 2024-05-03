import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
sys.path.append(project_dir)

from config import *


# noinspection DuplicatedCode
def update_generations(new_generation_count: int):
    update_query = f"UPDATE settings SET setting_value = '{new_generation_count}' WHERE setting_name = 'generation_count'"
    cursor.execute(update_query)
    conn.commit()


def update_offspring_count(new_offspring_count: int):
    update_query = f"UPDATE settings SET setting_value = '{new_offspring_count}' where setting_name = 'offspring_count'"
    cursor.execute(update_query)
    conn.commit()


def update_conflict_weight(new_conflict_weight: float):
    update_query = f"UPDATE settings SET setting_value = {new_conflict_weight} WHERE setting_name = 'conflict'"
    cursor.execute(update_query)
    conn.commit()


def update_long_break_weight(new_long_break_weight: float):
    update_query = f"UPDATE settings SET setting_value = {new_long_break_weight} WHERE setting_name = 'long_break'"
    cursor.execute(update_query)
    conn.commit()


# noinspection DuplicatedCode
def update_RLE_schedule_weight(new_RLE_schedule_weight: float):
    update_query = f"UPDATE settings SET setting_value ={new_RLE_schedule_weight} WHERE setting_name = 'RLE_schedule'"
    cursor.execute(update_query)
    conn.commit()


def update_classroom_preference_weight(new_classroom_preference_weight: float):
    update_query = f"UPDATE settings SET setting_value = {new_classroom_preference_weight} WHERE setting_name = 'classroom_preference'"
    cursor.execute(update_query)
    conn.commit()


def update_first_to_last_class_weight(new_first_to_last_class_weight: float):
    update_query = f"UPDATE settings SET setting_value = {new_first_to_last_class_weight} WHERE setting_name = 'first_to_last_class'"
    cursor.execute(update_query)
    conn.commit()


def update_concurrent_course_weight(new_concurrent_course_weight: float):
    update_query = f"UPDATE settings SET setting_value = {new_concurrent_course_weight} WHERE setting_name = 'concurrent_course'"
    cursor.execute(update_query)
    conn.commit()


if __name__ == '__main__':
    update_generations(10)
    update_offspring_count(20)
    update_conflict_weight(0.6)
    update_long_break_weight(0.2)
    update_RLE_schedule_weight(0.3)
    update_classroom_preference_weight(0.3)
    update_first_to_last_class_weight(0.2)
    update_concurrent_course_weight(0.2)
    conn.commit()
