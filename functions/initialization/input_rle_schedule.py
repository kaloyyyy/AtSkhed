import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def input_rle_schedule():
    sections_per_year = []
    for x in range(4):
        sections_per_year.append(int(input(f'sections in {x + 1} year')))

    # print(sections_per_year)

if __name__ == '__main__':
    input_rle_schedule()
