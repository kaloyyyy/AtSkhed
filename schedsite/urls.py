from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name='Atskhed'),
    path('prospectus/', views.display_prospectus, name='display_prospectus'),
    path('course/', views.display_courses, name='display_courses'),
    path('generate/', run_script, name='generate_data'),
    path('classroom/', views.display_classrooms, name='display_classrooms'),
    path('program/', views.display_programs, name='display_programs'),
    path('custom_query/', display_custom_query, name='display_custom_query'),
    path('script/', run_script, name='run_script'),
    path('drop_offsprings/', drop_offspring_tables, name='drop_offspring_tables'),
    path('table/<str:offspring_table_name>/', views.generate_table, name='generate_table'),
    path('offsprings/', views.display_offspring_tables, name='offsprings'),
    path('get_class_code/', views.get_class_code, name='get_class_code'),
    path('settings/',settings_page, name = 'settings'),
    path('export-excel/', export_excel, name='export_excel')

]