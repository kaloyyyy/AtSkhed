import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def testing():
    # for i in range(126, 150):
    #     print(i - (i % 6) + 1)
    # for i in range(1, 23):
    #     print(i - (i % 3) + 2)
    for i in range(26, 50):
        print(i, end=" ")
        print(i - (i % 3)+3)

    # for i in range(102, 121):
        # friday
        # print(i, end=" ")
        # print(i - (i % 6))


if __name__ == '__main__':
    testing()
