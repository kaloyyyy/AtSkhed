from config import *


def initialize_offspring():
    # CON = sqlite3.connect('db/db.sqlite3')
    # CON.row_factory = sqlite3.Row
    # CUR_DB = CON.cursor()
    table_name = 'offspring'
    print(f"{color.CYAN}Initializing offspring", end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print(f'.{color.END}', end=' ')
    time.sleep(0.5)
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
    classroom_res = cursor.execute("select * from classrooms").fetchall()
    time_slot_res = cursor.execute("select * from time_slots").fetchall()

    cursor.execute("delete from offspring")
    conn.commit()

    for row in classroom_res:
        classroom_id = row['classroom_id']
        for time_slot in time_slot_res:
            time_id = time_slot['time_id']

            insertion = "insert into offspring (time_id, classroom_id) values (?, ?)"
            cursor.execute(insertion, (time_id, classroom_id))

    conn.commit()
    print(f'{color.GREEN}init offspring table done{color.END}')


if __name__ == '__main__':
    initialize_offspring()
