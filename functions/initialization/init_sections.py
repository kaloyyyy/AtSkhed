import sys
import os
import time

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def initialize_sections():
    print(f"{color.CYAN}Initializing sections", end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print(f'.{color.END}', end=' ')
    time.sleep(0.5)
    cursor.execute("delete from sections")
    conn.commit()
    years = ['first_years', 'second_years', 'third_years', 'fourth_years']
    students_per_program_year = []
    index_student_per_year = 0
    for row in PROGRAMS_RES:
        programID = row['program_id']
        sections = [row['group_first'], row['group_second'], row['group_third'], row['group_fourth']]

        year = 1
        if year == 4:
            year = 1


        for section in sections:
            students_per_program_year.append(row[years[year-1]])
            if section != 0 and section is not None and students_per_program_year[index_student_per_year]>40:
                students_div = int(np.ceil(students_per_program_year[index_student_per_year]/section))

            groupCount = 0
            groups = alphabet = [chr(letter) for letter in range(ord('A'), ord('Z') + 1)]
            if section is not None and section != 0:

                for x in range(section):
                    # distribute as evenly as possible xD
                    quotient = students_per_program_year[index_student_per_year] // section
                    remainder = students_per_program_year[index_student_per_year] % section
                    result = [quotient] * (section - remainder) + [quotient + 1] * remainder
                    students = result[x]
                    group = groups[groupCount]
                    sectionData = (programID, year, group, students)
                    newSectionQuery = "INSERT INTO sections (program_id, year,  section, students) VALUES (?, ?, ?, ?)"
                    # Execute the query with parameters
                    cursor.execute(newSectionQuery, sectionData)
                    groupCount += 1
            year += 1
            index_student_per_year +=1

    conn.commit()

    print(f"{color.GREEN}init sections done{color.END}")


if __name__ == "__main__":
    initialize_sections()
