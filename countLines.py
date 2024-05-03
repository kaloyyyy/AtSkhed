import os


def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)


def count_lines_in_directory(directory):
    lines = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                lines += count_lines(file_path)
    return lines


if __name__ == "__main__":
    total_lines = 0

    target_directory = ["C:/Users/kaloy/Documents/GitHub/py/AtSKhed/functions/api",
                        "C:/Users/kaloy/Documents/GitHub/py/AtSKhed/functions/genetic",
                        "C:/Users/kaloy/Documents/GitHub/py/AtSKhed/functions/initialization"]
    for directory in target_directory:
        total_lines += count_lines_in_directory(directory)
    total_lines += count_lines("C:/Users/kaloy/Documents/GitHub/py/AtSKhed/main.py")
    total_lines += count_lines("C:/Users/kaloy/Documents/GitHub/py/AtSKhed/config.py")

    print(f"Total lines of Python code: {total_lines}")
