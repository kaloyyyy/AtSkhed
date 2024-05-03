import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


# TODO Before doing this, must do the assign RLE courses function
def RLE_schedule_conflict(offspring_table):
    raise NotImplementedError("haha tinatamad pa ako")
    offspring_query = f"""select * from {offspring_table}"""
    for row in RLE_RES:
        ...


if __name__ == '__main__':
    ...
