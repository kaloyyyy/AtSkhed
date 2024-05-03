import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def aStar(offspring_table):
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
                                order by p.course_id, students, p.year, program_name, college
                                """
    recurring_course_results = cursor.execute(recurring_course_query).fetchall()
    for course in recurring_course_results:
        course_id = course['course_id']
        code = course['code']
        program_name = course['program_name']
        program_id = course['program_id']
if __name__ == '__main__':
    ...
