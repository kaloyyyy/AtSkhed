import os
import sqlite3
import subprocess
import pandas as pd

from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from openpyxl import Workbook

from functions.api.trytable import table_transform

from AtSKhed.settings import BASE_DIR
from schedsite.models import Courses, Classes


def export_excel(request):
    # Generate the Excel file
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Offspring Data'

    # Add table_data to the worksheet
    for row_idx, row_data in enumerate(table_data):
        for col_idx, cell_data in enumerate(row_data):
            worksheet.cell(row=row_idx+1, column=col_idx+1, value=str(cell_data))

    # Save the workbook to a BytesIO object
    excel_file = BytesIO()
    workbook.save(excel_file)
    excel_file.seek(0)

    # Create an HttpResponse with the Excel file as attachment
    response = HttpResponse(excel_file.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=offspring_data.xlsx'
    return response




def display_custom_query(request):
    with connection.cursor() as cursor:
        # Your custom SQL query without a specific range condition for program IDs
        sql_query = """
        SELECT p.program_name as program_name, c.code, c.description, c.units, prospectus.year, prospectus.semester
        FROM prospectus
        JOIN courses c ON c.course_id = prospectus.course_id
        JOIN programs p ON p.program_id = prospectus.program_id
        """

        cursor.execute(sql_query)
        result = cursor.fetchall()

    # Organize the data by program name
    programs_data = {}
    for row in result:
        program_name = row[0]
        if program_name not in programs_data:
            programs_data[program_name] = []

        programs_data[program_name].append({
            'code': row[1],
            'description': row[2],
            'units': row[3],
            'year': row[4],
            'semester': row[5],
        })

    # Construct an HTML response directly in the view
    html_response = "<h1>Custom Query Results</h1>"

    for program_name, courses in programs_data.items():
        html_response += (f"<h2>{program_name}</h2><table><thead><tr><th>Code</th><th>Description</th><th>Units</th"
                          f"><th>Year</th><th>Semester</th></tr></thead><tbody>")

        for course in courses:
            html_response += f"<tr><td>{course['code']}</td><td>{course['description']}</td><td>{course['units']}</td><td>{course['year']}</td><td>{course['semester']}</td></tr>"

        html_response += "</tbody></table>"

    return HttpResponse(html_response)


def display_prospectus(request):
    with connection.cursor() as cursor:
        # Your custom SQL query without a specific range condition for program IDs
        sql_query = """
        SELECT p.program_name as program_name, c.code, c.description, c.units, prospectus.year, prospectus.semester
        FROM prospectus
        JOIN courses c ON c.course_id = prospectus.course_id
        JOIN programs p ON p.program_id = prospectus.program_id
        """

        cursor.execute(sql_query)
        result = cursor.fetchall()

    # Organize the data by program name
    programs_data = {}
    for row in result:
        program_name = row[0]
        if program_name not in programs_data:
            programs_data[program_name] = []

        programs_data[program_name].append({
            'code': row[1],
            'description': row[2],
            'units': row[3],
            'year': row[4],
            'semester': row[5],
        })

    return render(request, 'prospectus_result.html', {'programs_data': programs_data})


def display_courses(request):
    with connection.cursor() as cursor:
        sql_query = """
            SELECT c.code, c.description, c.units
            FROM courses c
        """
        cursor.execute(sql_query)
        courses_data = cursor.fetchall()

    # Organize the data by course code
    courses_by_code = {}
    for row in courses_data:
        course_code = row[0]
        if course_code not in courses_by_code:
            courses_by_code[course_code] = []

        courses_by_code[course_code].append({
            'description': row[1],
            'units': row[2]
        })

    return render(request, 'result.html', {'courses_by_code': courses_by_code})


def display_programs(request):
    with connection.cursor() as cursor:
        sql_query = """
            SELECT p.program_name, p.first_years, p.second_years, p.third_years, p.fourth_years
            FROM programs p
        """
        cursor.execute(sql_query)
        programs_data = cursor.fetchall()

    # Organize the data by program name
    programs_by_name = {}
    for row in programs_data:
        program_name = row[0]
        if program_name not in programs_by_name:
            programs_by_name[program_name] = []

        programs_by_name[program_name].append({
            'firstyears': row[1],
            'secondyears': row[2],
            'thirdyears': row[3],
            'fourthyears': row[4]
        })

    return render(request, 'programs_result.html', {'programs_by_name': programs_by_name})


def display_classrooms(request):
    with connection.cursor() as cursor:
        sql_query = """
            SELECT c.classroom_id, c.room_name, c.floor, c.capacity, c.bldg, c.type
            FROM classrooms c
        """
        cursor.execute(sql_query)
        classrooms_data = cursor.fetchall()

    # Organize the data by classroom ID
    classrooms_by_id = {}
    for row in classrooms_data:
        classroom_id = row[0]
        if classroom_id not in classrooms_by_id:
            classrooms_by_id[classroom_id] = []

        classrooms_by_id[classroom_id].append({
            'room_name': row[1],
            'floor': row[2],
            'capacity': row[3],
            'bldg': row[4],
            'type': row[5]
        })

    return render(request, 'classroom_result.html', {'classrooms_by_id': classrooms_by_id})


def generate_table(request, offspring_table_name):
    # Call the table_transform function to get the data for the specific offspring table
    connection.row_factory = sqlite3.Row
    table_data = table_transform(offspring_table_name)

    # Define a mapping of day codes to day names
    day_mapping = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday'
        # Add more day mappings as needed
    }

    # Iterate through the table data and replace the day codes with their names
    for row in table_data:
        day_code = row[0]  # Assuming the day code is the first element in each row
        if day_code in day_mapping:
            row[0] = day_mapping[day_code]

    # Pass the modified table data to the template for rendering
    return render(request, 'table_template.html', {'table_data': table_data, 'offspring_table_name': offspring_table_name})


def display_offspring_tables(request):
    # Execute a raw SQL query to retrieve the names of the offspring tables and their fitness scores
    with connection.cursor() as cursor:
        cursor.execute("SELECT offspring_table, fitness FROM fitness")
        rows = cursor.fetchall()

    # Generate HTML links for each offspring table along with their fitness scores
    offspring_links_html = ''
    for row in rows:
        offspring_table_name, fitness_score = row
        table_link = reverse('generate_table', args=[offspring_table_name])
        offspring_links_html += f'<p><a href="{table_link}">{offspring_table_name}</a> - Fitness Score: {fitness_score}</p>'

    # Render the template with the links to offspring tables and their fitness scores
    return render(request, 'table_template.html', {'offspring_links_html': offspring_links_html})

def get_class_code(request):
    class_id = request.GET.get('class_id')
    if class_id is None:
        return JsonResponse({'error': 'Class ID not provided'}, status=400)

    try:
        class_instance = Classes.objects.get(class_id=class_id)
        class_code = class_instance.prospectus_id.course_id.code
        class_section = class_instance.class_section_letter
        return JsonResponse({'class_code': f"{class_code} - {class_section}"})
    except Courses.DoesNotExist:
        return JsonResponse({'error': 'Class not found'}, status=404)


def drop_offspring_tables(request):
    current_env = os.environ.copy()
    output = ''
    try:
        process = subprocess.Popen(['python', f'{BASE_DIR}/functions/initialization/drop_offspring_tables.py'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Read output from the subprocess
        stdout, stderr = process.communicate()

        # Decode the output from bytes to string
        output = stdout.decode('utf-8')

        if process.returncode == 0:
            result = "Script executed successfully"
            return render(request, 'drop_offspring.html', {'result': result, 'output': output})

        else:

            result = f"Script execution failed with error: {stderr.decode('utf-8')}"

    except Exception as e:
        result = f"An error occurred: {str(e)}"
        return JsonResponse({'result': result, 'output': output})
    return JsonResponse({'result': result, 'output': output})


def run_script(request):
    try:
        process = subprocess.Popen(['python', f'{BASE_DIR}/main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Read output from the subprocess
        stdout, stderr = process.communicate()

        # Decode the output from bytes to string
        output = stdout.decode('utf-8')

        # Print the output to the console
        print(output)

        if process.returncode == 0:
            result = "Script executed successfully"
            return render(request, 'generate_offspring.html', {'result': result, 'output': output})
        else:
            result = f"Script execution failed with error: {stderr.decode('utf-8')}"

        # Format the output for better readability
        formatted_output = parse_output(output)

    except Exception as e:
        result = f"An error occurred: {str(e)}"
        formatted_output = None
        return JsonResponse({'result': result, 'output': formatted_output})
    return JsonResponse({'result': result, 'output': formatted_output})


def parse_output(output):
    lines = output.strip().split('\n')

    parsed_output = {
        'tables_dropped': [],
        'offspring_created': [],
        'offspring_details': [],
        'function_execution_time': None
    }

    for line in lines:
        if line.startswith('dropping table'):
            parsed_output['tables_dropped'].append(line.split('dropping table ')[1])
        elif line.startswith('Creating Chromosome'):
            chromosome = line.split(' ')[1]
            parsed_output['offspring_created'].append(chromosome)
        elif line.startswith('offspring_'):
            details = line.split('|')
            chromosome, info = details[0].strip(), details[1].strip()
            parsed_output['offspring_details'].append({'chromosome': chromosome, 'info': info})
        elif line.startswith('Function genetic_algorithm()'):
            time_str = line.split('Took ')[1]
            parsed_output['function_execution_time'] = float(time_str.split(' ')[0])

    return parsed_output


def settings_page(request):
    # Fetch current settings from the database
    current_settings = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT setting_name, setting_value FROM settings")
        rows = cursor.fetchall()
        for row in rows:
            current_settings[row[0]] = row[1]

    if request.method == 'POST':
        # Process the form submission
        updated_settings = {}
        for key in current_settings.keys():
            # Update settings with values from the form if available, otherwise keep the current value
            updated_settings[key] = request.POST.get(key, current_settings[key])

        # Save the updated settings to the database
        with connection.cursor() as cursor:
            for key, value in updated_settings.items():
                cursor.execute("UPDATE settings SET setting_value = %s WHERE setting_name = %s", [value, key])

        # Fetch the updated settings from the database
        with connection.cursor() as cursor:
            cursor.execute("SELECT setting_name, setting_value FROM settings")
            updated_rows = cursor.fetchall()
            updated_settings = {row[0]: row[1] for row in updated_rows}

        context = {
            'settings': updated_settings
        }
        return render(request, 'settings.html', context)

    # Render the template with the current settings
    context = {
        'settings': current_settings
    }
    return render(request, 'settings.html', context)


def home(request):
    return render(request, 'home.html')


def settings(request):
    return render(request, 'settings.html')
