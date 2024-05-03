import sys
import os
import django
from django.db import connection

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AtSKhed.settings')
django.setup()

from config import *


def table_transform(offspring_table):
    # Manually create a database connection
    connection.connect()

    # Set row factory to return dictionaries
    connection.cursor().connection.row_factory = sqlite3.Row

    my_query = f"""select day, time_start, time_end, room_name, c3.code, {offspring_table}.time_id, {offspring_table}.class_id, {offspring_table}.classroom_id
                    from {offspring_table}
                        left join main.classes c on {offspring_table}.class_id = c.class_id
                        left join main.prospectus p on c.prospectus_id = p.prospectus_id
                        left join main.courses c3 on p.course_id = c3.course_id
                        left join main.classrooms c2 on c.classroom_id = c2.classroom_id
                        left join main.time_slots ts on {offspring_table}.time_id = ts.time_id
                        order by {offspring_table}.time_id, {offspring_table}.classroom_id"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(my_query)
            my_result = cursor.fetchall()
    except Exception as e:
        print("An error occurred:", e)
        return [["no table"]]

    table = []
    previous_c_room_id = 1
    previous_time_id = 1
    temp = []

    rooms_list = ["time/room"]
    for room in CLASSROOM_RES:
        rooms_list.append(room['room_name'])
    # print(my_result)
    # Append headers to the first row of the table data
    table.append(["Day", "Time/Room"] + [room['room_name'] for room in CLASSROOM_RES])
    temp.append(my_result[0]['day'])
    time_start = f"{my_result[0]['time_start']} - {my_result[0]['time_end']}"
    temp.append(time_start)
    for x in my_result:
        current_c_room_id = x['classroom_id']
        current_time_id = x['time_id']
        current_subject = x['code']
        current_class_id = x['class_id']

        if previous_time_id == current_time_id:
            temp.append(current_class_id)
        else:
            # Add a new row with day, time, and class information

            table.append(temp)
            temp = []
            temp.append(x['day'])
            temp.append(f"{x['time_start']} - {x['time_end']}")

            temp.append(current_class_id)

        previous_c_room_id = current_c_room_id
        previous_time_id = current_time_id

    # Add the last row

    table.append(temp)

    return table


if __name__ == '__main__':
    t = table_transform("offspring_0_0")
    df = pd.DataFrame(t)
    print(df)
