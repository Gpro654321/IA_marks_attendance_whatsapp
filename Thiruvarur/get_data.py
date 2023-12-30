import gspread
from jinja2 import Template 
import pandas as pd
import os
import datetime
import shutil
import sys
import itertools


from pdfcreator import html_to_pdf

# use the service account credentials
gc = gspread.service_account(
    filename='./ia-marks-whatsapp-3c2e08dd11d9.json'
)


# open the spreadsheet with spreadsheet key
# spreadsheet = gc.open_by_key('10-uabmR_EIqKLtQBt6a7df8yTxw1wJia7U7yS9v53gI')

# test spreadsheet
spreadsheet = gc.open_by_key('19WMSN5aYv2dsN56R0kwD5Ut2nKzV91uYkE0nTzhCeW4')

# spreadsheet = gc.open_by_key('10-uabmR_EIqKLtQBt6a7df8yTxw1wJia7U7yS9v53gI')


# open the worksheet using the sheet name
details = spreadsheet.worksheet('Details')
ia = spreadsheet.worksheet('IA')
attendance = spreadsheet.worksheet('Attendance')

# get all the row data
details_rows = details.get_all_values()
ia_rows = ia.get_all_values()
attendance_rows = attendance.get_all_values()

# convert to pandas dataframe
df_original_details = pd.DataFrame.from_records(details_rows)
df_original_ia = pd.DataFrame.from_records(ia_rows)
df_original_attendance = pd.DataFrame.from_records(attendance_rows)

# try printing the data heads
print(df_original_details.head())
print(df_original_ia.head())
print(df_original_attendance.head())

# create a new dataframe from the original ones to create respective dataframes
# containing only the data without the headers
df_details = df_original_details.iloc[1:]
df_ia = df_original_ia.iloc[1:]
df_attendance = df_original_attendance.iloc[1:]


print("df_details shape", df_details.shape)
print("df_ia shape", df_ia.shape)
print("df_attendance shape", df_attendance.shape)

# gather the column headers from the original dataframe
details_column_headers = df_original_details.iloc[0]
ia_column_headers = df_original_ia.iloc[0]
attendance_column_headers = df_original_attendance.iloc[0]

# assign column header names from the above created column names
df_details.columns = details_column_headers
df_ia.columns = ia_column_headers
df_attendance.columns = attendance_column_headers

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



# Apply the render function to each row and generate the HTML file
for details_row, ia_row, attendance_row in itertools.zip_longest(
    df_details.itertuples(index=False),
    df_ia.itertuples(index=False),
    df_attendance.itertuples(index=False)
):
    print("ia_row", [list(ia_row)])

    now = datetime.datetime.now()
    current_time_string = now.strftime("%Y%m%d%H%M%S%f")
    rendered_html = template.render(
        refno = current_time_string, 
        name = str(details_row.name).upper(),
        roll_no = str(details_row.student_roll_no).upper(),
        ia_table_headers = df_ia.columns,
        ia_table_data = [list(ia_row)],
        attendance_table_headers = df_attendance.columns,
        attendance_table_data = [list(attendance_row)]
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
    html_to_pdf(html_file_path)

    # to prevent clutter of the html_files folder the html files
    # will be moved to a backup directory 
    backup_file_path = os.path.join(html_backup_dir,html_file_name)
    shutil.move(html_file_path, backup_file_path)
