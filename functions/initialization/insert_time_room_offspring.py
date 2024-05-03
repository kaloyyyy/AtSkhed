import sqlite3
from config import *


def main():
    # Fetch timeSlotsResults and classroomsResults
    time_slots_query = "SELECT time_id FROM time_slots"
    classrooms_query = "SELECT classroom_id FROM classrooms"

    cursor.execute(time_slots_query)
    time_slots_results = cursor.fetchall()

    cursor.execute(classrooms_query)
    classrooms_results = cursor.fetchall()
    table_name = 'offspring'
    chromosome_table_query = f'''create table if not exists {table_name}
                                    (
                                        time_id       int
                                            constraint offspring_timeSlots_time_id_fk
                                                references timeSlots,
                                        class_id     integer
                                            constraint offspring_classes_class_id_fk
                                                references classes,
                                        classroom_id integer
                                            constraint offspring_classrooms_classroom_id_fk
                                                references classrooms,
                                        constraint offspring_pk
                                            primary key (time_id, classroom_id)
                                    );'''

    cursor.execute(chromosome_table_query)
    # Iterate through timeSlotsResults and classroomsResults
    for time_slot in time_slots_results:
        for classroom in classrooms_results:
            time_slot_id, classroom_id = time_slot[0], classroom[0]
            # print(time_slot_id, classroom_id)

            # Use parameterized query to prevent SQL injection
            schedule_insert_query = "INSERT INTO offspring (time_id, classroom_id, class_id) VALUES (?, ?, NULL)"

            # Execute the query with parameters
            cursor.execute(schedule_insert_query, (time_slot_id, classroom_id))

    # Commit the changes and close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()
    print('insert time room offspring done')

if '__main__' == __name__:
    main()
