import gspread
from jinja2 import Template 
import pandas as pd
import os
import datetime
import shutil
import sys
import itertools
import requests
import urllib.parse


from dotenv import load_dotenv

from pdfcreator import html_to_pdf
from send_via_whatsapp import sendFileViaWhatsapp_post

# load the environment variables

load_dotenv('./.param.env')

# use the service account credentials
access_key_file_path = os.getenv('ACCESS_KEY_FILE_PATH')
gc = gspread.service_account(
    filename=access_key_file_path
)

operation_mode = str(
                        input(
                        "Is this test or production?\n"+
                        "type 'test' if test environment\n"+
                        "else type 'production' if the environment is production\n"
                       ) 
                    )
print("The operation mode is ", operation_mode)

if operation_mode == 'test':
    print("running test mode")

    # test spreadsheet
    test_spreadsheet_key = os.getenv('TEST_SPREADSHEET_KEY')
    spreadsheet = gc.open_by_key(test_spreadsheet_key)

if operation_mode == 'production':
    print("running production mode")
    # production spreadsheet
    prod_spreadsheet_key = os.getenv('PROD_SPREADSHEET_KEY')
    spreadsheet = gc.open_by_key(prod_spreadsheet_key)

token = os.getenv('TOKEN')
print(token)

# open the worksheet using the sheet name
details = spreadsheet.worksheet('Details')
ia_theory = spreadsheet.worksheet('IA_Theory')
ia_practical = spreadsheet.worksheet('IA_Practical')
attendance_theory = spreadsheet.worksheet('Attendance_Theory')
attendance_practical = spreadsheet.worksheet('Attendance_Practical')

# get all the row data
details_rows = details.get_all_values()
ia_theory_rows = ia_theory.get_all_values()
ia_practical_rows = ia_practical.get_all_values()
attendance_theory_rows = attendance_theory.get_all_values()
attendance_practical_rows = attendance_practical.get_all_values()

# convert to pandas dataframe
df_original_details = pd.DataFrame.from_records(details_rows)
df_original_ia_theory = pd.DataFrame.from_records(ia_theory_rows)
df_original_ia_practical = pd.DataFrame.from_records(ia_practical_rows)
df_original_attendance_theory = pd.DataFrame.from_records(attendance_theory_rows)
df_original_attendance_practical = pd.DataFrame.from_records(attendance_practical_rows)

# try printing the data heads
print(df_original_details.head())
print(df_original_ia_theory.head())
print(df_original_ia_practical.head())
print(df_original_attendance_theory.head())
print(df_original_attendance_practical.head())

# create a new dataframe from the original ones to create respective dataframes
# containing only the data without the headers
df_details = df_original_details.iloc[1:]
df_ia_theory = df_original_ia_theory.iloc[1:]
df_ia_practical = df_original_ia_practical.iloc[1:]
df_attendance_theory = df_original_attendance_theory.iloc[1:]
df_attendance_practical = df_original_attendance_practical.iloc[1:]


print("df_details shape", df_details.shape)
print("df_ia theory shape", df_ia_theory.shape)
print("df_ia practical shape", df_ia_practical.shape)
print("df_attendance theory shape", df_attendance_theory.shape)
print("df_attendance practical shape", df_original_attendance_practical.shape)

# gather the column headers from the original dataframe
details_column_headers = df_original_details.iloc[0]

# The column header of the internal assessment sheet is of the form IA-30, where
# the part after the "-" is the maximum mark
ia_theory_column_headers_split = df_original_ia_theory.iloc[0].str.split("-")
# The first part of hte split
ia_theory_column_headers = ia_theory_column_headers_split.str.get(0)
# The pandas series with the maximum marks
ia_theory_column_max_marks = pd.Series(ia_theory_column_headers_split.str.get(1), dtype="string") 

# do the same as above for practicals
# The column header of the internal assessment sheet is of the form IA-30, where
# the part after the "-" is the maximum mark
ia_practical_column_headers_split = df_original_ia_practical.iloc[0].str.split("-")
# The first part of hte split
ia_practical_column_headers = ia_practical_column_headers_split.str.get(0)
# The pandas series with the maximum marks
ia_practical_column_max_marks = pd.Series(ia_practical_column_headers_split.str.get(1), dtype="string") 


attendance_theory_column_headers = df_original_attendance_theory.iloc[0]
attendance_practical_column_headers = df_original_attendance_practical.iloc[0]

# assign column header names from the above created column names
df_details.columns = details_column_headers
df_ia_theory.columns = ia_theory_column_headers
df_ia_practical.columns = ia_practical_column_headers
df_attendance_theory.columns = attendance_theory_column_headers
df_attendance_practical.columns = attendance_practical_column_headers


print("df_details.columns,", df_details.columns)

# create a template object
template = Template(open('./html_templates/base.html').read())

# create a directory to put the newly created html files
html_dir = "./html_files"
if not os.path.exists(html_dir):
    print("html_dir NOT found, creating it...")
    os.makedirs(html_dir)

html_backup_dir = "./html_backup"
if not os.path.exists(html_backup_dir):
    print("html_backup_dir NOT found, creating it...")
    os.makedirs(html_backup_dir)

# create a directory to put the newly created pdf files
pdf_dir = "./pdf_files"
if not os.path.exists(pdf_dir):
    print("pdf_dir NOT found, creating it ..")
    os.makedirs(pdf_dir)

# create a directory to put the pdf files that were sent
sent_dir = "./sent"
if not os.path.exists(sent_dir):
    print("sent_dir NOT found, creating it ...")
    os.makedirs(sent_dir)



# Apply the render function to each row and generate the HTML file
for (details_row, 
    ia_theory_row, 
    ia_practical_row,
    attendance_theory_row,
    attendance_practical_row) in itertools.zip_longest(
    df_details.itertuples(index=False),
    df_ia_theory.itertuples(index=False),
    df_ia_practical.itertuples(index=False),
    df_attendance_theory.itertuples(index=False),
    df_attendance_practical.itertuples(index=False),
):

    
    # theory marks as frac
    # generate the ia marks in the form obtained/max eg 15/30
    print("ia_theory_row", [list(ia_theory_row)])
    ia_theory_marks_space_seperated = ((ia_theory_row + ia_theory_column_max_marks).astype("string"))
    ia_theory_marks_obtained_max_list = ia_theory_marks_space_seperated.str.split(" ")
    print(ia_theory_marks_space_seperated.str.split(" "))
    separator = " / "
    ia_theory_marks_frac = ia_theory_marks_obtained_max_list.apply(lambda x: separator.join(x))
    print(ia_theory_marks_frac)


    # practical marks as frac
    # generate the ia marks in the form obtained/max eg 15/30
    print("ia_practical_row", [list(ia_practical_row)])
    ia_practical_marks_space_seperated = ((ia_practical_row + ia_practical_column_max_marks).astype("string"))
    ia_practical_marks_obtained_max_list = ia_practical_marks_space_seperated.str.split(" ")
    print(ia_practical_marks_space_seperated.str.split(" "))
    separator = " / "
    ia_practical_marks_frac = ia_practical_marks_obtained_max_list.apply(lambda x: separator.join(x))
    print(ia_practical_marks_frac)
    
    #Theory
    # convert the attendance percentages to 2 significant digits
    attendance_theory_row = pd.Series(attendance_theory_row, dtype="float64")
    attendance_theory_row = attendance_theory_row.apply(lambda x: round(x, 2))

    #Practical
    # convert the attendance percentages to 2 significant digits
    attendance_practical_row = pd.Series(attendance_practical_row, dtype="float64")
    attendance_practical_row = attendance_practical_row.apply(lambda x: round(x, 2))

    now = datetime.datetime.now()
    current_time_string = now.strftime("%Y%m%d%H%M%S%f")
    rendered_html = template.render(
        refno = current_time_string, 
        name = str(details_row.name).upper(),
        roll_no = str(details_row.student_roll_no).upper(),
        ia_theory_table_headers = df_ia_theory.columns,
        ia_practical_table_headers = df_ia_practical.columns,
        ia_theory_table_data = [list(ia_theory_marks_frac)],
        ia_practical_table_data = [list(ia_practical_marks_frac)],
        attendance_theory_table_headers = df_attendance_theory.columns,
        attendance_practical_table_headers = df_attendance_practical.columns,
        attendance_theory_table_data = [list(attendance_theory_row)],
        attendance_practical_table_data = [list(attendance_practical_row)],
    )
    
    candidate_name = details_row.name 
    roll_no = str(details_row.student_roll_no).upper().zfill(4)
    # write the rendered html string to a file
    html_file_name = f"student_report_{roll_no}_{candidate_name}.html"
    html_file_path = os.path.join(html_dir, html_file_name)
    with open(html_file_path, 'w') as f:
        print("creating file ",roll_no)
        f.write(rendered_html)


    print("creating pdf file", roll_no)
    pdf_file_name = html_to_pdf(html_file_path)
    pdf_file_path = os.path.join(pdf_dir, pdf_file_name)
    print("pdf file path", pdf_file_path)

    # to prevent clutter of the html_files folder the html files
    # will be moved to a backup directory 
    backup_file_path = os.path.join(html_backup_dir,html_file_name)
    shutil.move(html_file_path, backup_file_path)

    
    # send the the file via whatsapp
    # the following are the post parameters
    phone = str(91) + str(details_row.mobile_no)
    print("phone_no", phone)



    test_caption = ("Dear Parent,\n" +
                    "The document attached above," +
                    "contains the performance evaluation of [son/daughter] in the Department of Physiology."+
                    "\n\n"+
                    "HOD of Physiology,\n"+
                    "Govt. Medical College, Namakkal")

    if operation_mode == "test":
        pass
    elif operation_mode == "production":
        sendFileViaWhatsapp_post(token, phone, pdf_file_path, test_caption)
    

    # to prevent clutter of the pdf files that were sent
    # will be moved to the sent directory
    sent_file_path = os.path.join(sent_dir,pdf_file_name)
    shutil.move(pdf_file_path, sent_file_path)

