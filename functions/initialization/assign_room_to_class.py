import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def assign_room_to_class():
    print(f"{color.CYAN}Assigning room to classes | a* algorithm", end="")
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print(f'.{color.END}', end=' ')
    time.sleep(0.5)
    classes_query = f'select * from classes'
    classes_result = cursor.execute(classes_query).fetchall()
    pathfit = cursor.execute(f"select course_id from courses where code like '%PATHFIT%'").fetchall()
    pathfit_list = []
    sorted_rooms = cursor.execute(
        f"select classroom_id from classrooms where classroom_id < 63 order by capacity").fetchall()
    classroom_pool = [row['classroom_id'] for row in sorted_rooms]
    for course in pathfit:
        pathfit_list.append(course['course_id'])
    for classes in classes_result:
        student_count = 0
        prospectus_id = classes['prospectus_id']
        class_id = classes['class_id']
        # check if there are other sections
        check_sections_query = f"select * from main.assign_section_to_class join main.sections s on assign_section_to_class.section_id = s.section_id where class_id = {class_id}"
        check_sections_result = cursor.execute(check_sections_query).fetchall()
        # count students
        for section in check_sections_result:
            student_count += section['students']
        sorted_rooms = cursor.execute(f"""SELECT classes.*, capacity, COUNT(*) as references_count
                                            FROM classes
                                            JOIN main.classrooms c ON c.classroom_id = classes.classroom_id
                                            WHERE c.classroom_id < 63
                                            GROUP BY classes.classroom_id
                                            ORDER BY references_count, capacity;""").fetchall()
        classroom_pool = [row['classroom_id'] for row in sorted_rooms]
        course_id = cursor.execute(
            f"select course_id from prospectus where prospectus_id = {prospectus_id}").fetchone()
        # print("course id: ", course_id['course_id'])
        if course_id['course_id'] in pathfit_list:
            PE_rooms = cursor.execute(f"""SELECT classes.*, capacity, COUNT(*) as references_count
                                            FROM classes
                                            JOIN main.classrooms c ON c.classroom_id = classes.classroom_id
                                            WHERE c.classroom_id >= 63
                                            GROUP BY classes.classroom_id
                                            ORDER BY references_count, capacity;""").fetchall()
            if len(PE_rooms) < 4:
                classroom_id = choice([63, 64, 65, 66, 67, 68])
            else:
                classroom_id = PE_rooms[0]['classroom_id']

        else:
            while True:
                classroom_cap = 0
                classroom_rank_query = f"""SELECT c.classroom_id, capacity, COUNT(classes.class_id) as references_count
                                            FROM main.classrooms c
                                                     LEFT JOIN classes ON c.classroom_id = classes.classroom_id
                                            WHERE c.classroom_id < 63
                                            GROUP BY c.classroom_id
                                            ORDER BY references_count, capacity;"""
                classroom_rank_results = cursor.execute(classroom_rank_query).fetchall()
                if classroom_rank_results:
                    for classroom in classroom_rank_results:
                        classroom_id = classroom['classroom_id']
                        check_classroom_query = f"select * from main.classrooms where classroom_id = {classroom_id}"
                        check_classroom_result = cursor.execute(check_classroom_query).fetchone()
                        classroom_cap = check_classroom_result['capacity']
                        # print(classroom_cap, student_count, class_id, classroom_id)
                        if classroom_id in classroom_pool:
                            classroom_pool.remove(classroom_id)
                        if classroom_cap >= student_count:
                            break
                else:

                    # print(f"    else {len(classroom_pool)}", classroom_cap, student_count, class_id, None, end="    ")
                    for room in classroom_pool:
                        check_classroom_query = f"select * from main.classrooms where classroom_id = {room} "
                        check_classroom_result = cursor.execute(check_classroom_query).fetchone()
                        classroom_cap = check_classroom_result['capacity']
                        classroom_id = check_classroom_result['classroom_id']
                        if classroom_cap >= student_count:
                            classroom_pool.remove(classroom_id)
                            break

                if classroom_cap >= student_count:
                    break
        class_update_query = f"UPDATE classes SET classroom_id = {classroom_id} WHERE class_id = {class_id}"
        # print(class_update_query)
        cursor.execute(class_update_query)
        conn.commit()
    print(f"{color.GREEN}a* finished assigning rooms{color.END}")


if __name__ == '__main__':
    assign_room_to_class()
