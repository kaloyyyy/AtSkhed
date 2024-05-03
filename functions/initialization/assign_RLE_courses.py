import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


# TODO Do this function before doing the RLE schedule conflict function
def assign_RLE_courses():
    find_bsn_id = cursor.execute(f"select program_id from programs where program_name like '%nursing%'").fetchone()[0]
    bsn_id = find_bsn_id
    nursing_section_query = f"select * from sections where program_id = {bsn_id}"
    nursing_sections = cursor.execute(nursing_section_query).fetchall()



    rle_per_year = []
    # loop making a list for each year's RLE
    for x in range(4):
        nursing_prospectus_query = f"select course_id from prospectus where program_id = {bsn_id} and semester = {semester} and year ={x + 1} "
        nursing_prospectus = cursor.execute(nursing_prospectus_query).fetchall()

        nursing_prospectus = [row[0] for row in nursing_prospectus]

        rle_current_year = [element for element in RLE_courses if element in nursing_prospectus]
        rle_per_year.append(rle_current_year)
    # print(rle_per_year)
    for section in nursing_sections:
        section_id = section['section_id']
        year = section['year']
        RLE_schedule_update_query = f"update RLE_schedule set course_id = ? where section_id = ?"
        for x in rle_per_year[year - 1]:

            cursor.execute(RLE_schedule_update_query, (x, section_id))
    conn.commit()

if __name__ == '__main__':
    assign_RLE_courses()