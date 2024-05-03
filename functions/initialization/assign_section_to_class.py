# assign classes to sections
import string
from random import random, sample, choice

from config import *


def assign_section_to_class():
    print(f"{color.CYAN}Assigning sections to classes", end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print(f'.{color.END}', end=' ')
    time.sleep(0.5)
    counter = 0
    cursor.execute("DELETE from classes")
    cursor.execute("DELETE from assign_section_to_class")
    conn.commit()
    pathfit = cursor.execute(f"select course_id from courses where code like '%PATHFIT%'")
    pathfit_list = []
    for course in pathfit:
        pathfit_list.append(course['course_id'])
    current_course_id = PROSPECTUS_RES[0]['course_id']
    previous_course_id = -1
    alpha_count = 0
    alphabet = generate_alphabet_combinations()
    classroom_pool = list(range(1, 63))
    for pros in PROSPECTUS_RES:  # prospectus_res order by course the program
        current_course_id = pros['course_id']

        if previous_course_id != current_course_id:
            # A to ZZ letters
            alphabet = generate_alphabet_combinations()
            alpha_count = 0

        program_id = (pros['program_id'])
        year = (pros['year'])
        sections_query = "SELECT section_id, program_id, year, section FROM sections  where program_id = ? AND year = ?"
        section_res = cursor.execute(sections_query, (program_id, year)).fetchall()
        prospectus_id = pros['prospectus_id']

        for section in section_res:

            section_id = section['section_id']
            class_insert = "insert into classes (prospectus_id, class_section_letter, course_id) values (?, ?,?)"
            section_assignment = "insert into assign_section_to_class (section_id, class_id) values (?, ?)"
            cursor.execute(class_insert, (prospectus_id, alphabet[alpha_count], current_course_id))
            class_id = cursor.lastrowid
            cursor.execute(section_assignment, (section_id, class_id))
            counter += 1
            alpha_count += 1
        previous_course_id = current_course_id
    conn.commit()
    print(f'{color.GREEN}assign class section done{color.END}')


def generate_alphabet_combinations():
    alphabet = string.ascii_uppercase
    combinations = []

    for char1 in alphabet:
        combinations.append(char1)

    for char1 in alphabet:
        for char2 in alphabet:
            combinations.append(char1 + char2)

    return combinations




if __name__ == '__main__':
    assign_section_to_class()