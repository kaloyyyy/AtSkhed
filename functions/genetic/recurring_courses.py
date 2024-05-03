import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def recurring_courses(offspring_table):
    recurring_courses_query = f"""SELECT astc.class_id, s.section_id, program_name, s.year, s.students, code
                                    FROM classes
                                        join main.assign_section_to_class astc on classes.class_id = astc.class_id
                                        join main.sections s on astc.section_id = s.section_id
                                        join main.prospectus p on classes.prospectus_id = p.prospectus_id
                                        join main.courses c on p.course_id = c.course_id
                                        join main.programs p2 on p2.program_id = p.program_id
                                    WHERE c.course_id IN (
                                        SELECT course_id FROM main.prospectus 
                                        GROUP BY course_id HAVING COUNT(*) > 1)
                                        and students <= 20
                                    ORDER BY code, students;"""

    recurring_courses_result = conn.execute(recurring_courses_query).fetchall()

    # print(f"recurring courses: {len(recurring_courses_result)}")
    return(len(recurring_courses_result))

if __name__ == '__main__':
    recurring_courses('offspring_0_0')
