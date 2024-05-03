import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def combine_algorithm():
    print(f"{color.CYAN}Combining classes | a* algorithm", end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print(f'.{color.END}', end=' ')
    time.sleep(0.5)
    recurring_course_query = f"""select  classes.class_id, classes.prospectus_id, p.course_id, 
                                    code, description, classes.classroom_id, program_name, p.year, 
                                    college, dept, s.section_id, students
                                from classes
                                    join main.assign_section_to_class astc on classes.class_id = astc.class_id
                                    join main.sections s on astc.section_id = s.section_id
                                    join main.prospectus p on p.prospectus_id = classes.prospectus_id
                                    join main.courses c on c.course_id = p.course_id
                                    join main.programs p2 on p2.program_id = p.program_id
                                WHERE p.course_id IN (
                                    SELECT p.course_id
                                        FROM classes
                                            join main.prospectus p on p.prospectus_id = classes.prospectus_id
                                            join main.courses c2 on p.course_id = c2.course_id
                                    GROUP BY p.course_id
                                    HAVING COUNT(*) > 1)
                                and p.program_id is not 1 and p.program_id is not 2
                                order by p.course_id, students, p.year, program_name, college
                                """
    recurring_course_results = cursor.execute(recurring_course_query).fetchall()
    for class_a in recurring_course_results:
        course_id_a = class_a['course_id']
        code_a = class_a['code']
        class_id_a = class_a['class_id']
        program_name_a = class_a['program_name']
        students_a = class_a['students']

        total_students = students_a
        if class_a in recurring_course_results:
            recurring_course_results.remove(class_a)
        for class_b in recurring_course_results:
            can_combine = False
            course_id_b = class_b['course_id']
            code_b = class_b['code']
            class_id_b = class_b['class_id']
            section_id_b = class_b['section_id']
            #if course_id_b == course_id_a:
                # print('class', course_id_b)
            students_b = class_b['students']
            # print(students_b)
            if students_b + total_students <= 40 and course_id_b == course_id_a:
                can_combine = True
                combine_query = f"update assign_section_to_class set class_id={class_id_a} where class_id={class_id_b} and section_id = {section_id_b}"
                cursor.execute(combine_query)
                delete_class_query = f"delete from classes where class_id={class_id_b}"
                cursor.execute(delete_class_query)
                cursor.execute(f'delete from assign_section_to_class where class_id={class_id_b} and section_id={section_id_b}')
                total_students = students_b + total_students
                recurring_course_results.remove(class_b)
            if can_combine:
                conn.commit()
                #print(f'combining {total_students}')

    print(f'{color.GREEN}a* finished combining{color.END}')

if __name__ == '__main__':
    combine_algorithm()