import sys
import os
import time

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def drop_offsprings():
    print(f"{color.PURPLE}Drop offspring tables", end='')
    # Get a list of tables matching the pattern
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print(f'.{color.END}')
    time.sleep(0.5)

    tables = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'offspring_%'").fetchall()
    # cursor.execute("DELETE from classes")
    # cursor.execute("DELETE from assign_section_to_class")
    # cursor.execute("delete from sections")
    # Drop each table
    for table in tables:
        table_name = table[0]
        print(f"{color.RED}dropped table {table_name}")
        cursor.execute(f"DROP TABLE {table_name}")

        # Commit the changes and close the connection
    conn.commit()

    print(f'{color.END}{color.BLUE}dropped generations: {int(generation_count)} {color.END}')


if __name__ == '__main__':
    drop_offsprings()
