import os
import pathlib
from weasyprint import HTML


def html_to_pdf(file_path):
    '''
    This function uses the weasyprint library to generate pdf
    '''

    dest_file = os.path.basename(file_path) 
    dest_file_name = dest_file.split(".")[0] + ".pdf"
    dest_file_path = os.path.join('./pdf_files',dest_file_name)
    
    # create the pdf output
    HTML(file_path).write_pdf(dest_file_path)
    return(dest_file_name)
