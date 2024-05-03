import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *

def assign_rle_to_sections():
    print(f"{color.CYAN}Assigning RLE schedules",end="")
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print(f'.{color.END}', end=' ')
    time.sleep(0.5)

    nursing_sections_query = f"select * from sections where program_id = 1 and year < 4"
    nursing_sections_results = cursor.execute(nursing_sections_query).fetchall()
    for section in nursing_sections_results:
        sec_year = section['year']
        rle_schedule_query = f"select * from main.RLE_schedule where section_id is null and year = {sec_year}"
        rle_schedule_results = cursor.execute(rle_schedule_query).fetchone()
        sched = rle_schedule_results
        rle_schedule_id = sched['RLE_id']
        time_id = sched['time_id']
        rle_save_query = f"update RLE_schedule set section_id = {section['section_id']} where RLE_id = {rle_schedule_id}"
        print(rle_save_query)
        cursor.execute(rle_save_query)
    conn.commit()
    print(f"{color.CYAN}RLE schedule done{color.END}")

if __name__ == '__main__':
    assign_rle_to_sections()