import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def init_fitness_table():
    # Get a list of tables matching the pattern
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'offspring%'")
    tables = cursor.fetchall()
    clear_fitness_table_query = "DELETE FROM fitness"
    cursor.execute(clear_fitness_table_query)
    for table in tables:
        table_name = table[0]

        # Assuming you have a function called get_fitness_score() to calculate fitness
        # Replace it with your actual fitness function
        fitness_score = 0

        # Insert fitness score into the fitness table
        insert_fitness_query = "INSERT INTO fitness (offspring_table, fitness) VALUES (?, ?)"
        cursor.execute(insert_fitness_query, (table_name, fitness_score))
    conn.commit()

if __name__ == '__main__':
    init_fitness_table()
