from config import *


def concurrent_course(offspring_table: str) -> None:
    """
    Concurrent course this function lets you how many subjects occurring in the same time. well might as well distribute it
    """
    offspring_table_query = f"""select c.class_id, p.course_id, time_id
                                    from {offspring_table}
                                    join main.classes c on c.class_id = {offspring_table}.class_id
                                    join main.prospectus p on c.prospectus_id = p.prospectus_id
                                    join main.courses c2 on p.course_id = c2.course_id 
                                    order by  time_id, p.course_id"""

    offspring_table_result = cursor.execute(offspring_table_query).fetchall()
    previous_course = 1
    previous_time = 1
    previous_class = 1
    concurrent_count = 0
    for row in offspring_table_result:
        class_id = row['class_id']
        course_id = row['course_id']
        time_id = row['time_id']

        if (previous_time == time_id) and (previous_course == course_id):
            concurrent_count += 1
            # print(course_id, time_id, previous_course, previous_time)
        previous_time = time_id
        previous_course = course_id
        previous_class = class_id

    all_course = cursor.execute(f"""select * from classes join prospectus p on p.prospectus_id join main.courses c on c.course_id = p.course_id""")
    recurring_course = cursor.execute(f"""SELECT distinct p.course_id
                                            from classes
                                                join main.prospectus p on p.prospectus_id = classes.prospectus_id
                                                join main.courses c on c.course_id = p.course_id
                                            where semester = 2""")
    result_recurring = len(all_course.fetchall()) - len(recurring_course.fetchall())
    print(f"recurring courses: {result_recurring} | concurrent courses: {int(concurrent_count)}")
    return concurrent_count


if __name__ == '__main__':
    for val in range(int(offspring_count)):
        concurrent_course(f"offspring_0_{val}")
