import gspread
from jinja2 import Template 
import pandas as pd
import os
import datetime
import shutil
import sys


# use the service account credentials
gc = gspread.service_account(
    filename='./ia-marks-whatsapp-3c2e08dd11d9.json'
)


# open the spreadsheet with spreadsheet key
spreadsheet = gc.open_by_key('10-uabmR_EIqKLtQBt6a7df8yTxw1wJia7U7yS9v53gI')


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

