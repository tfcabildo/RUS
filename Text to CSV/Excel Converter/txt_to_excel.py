# This code converts text files inside multiple folders into a single csv and Excel file.
# This first column of the output file is the file name of the text file.
# The text file is comma-delimited. Any bad lines or with different separator than a comma are neglected. 
# The output excel file has the cells auto-fixed to a certain width and data center-aligned.
# This code is used for the summarization of the CN0566 validation data.

# Author: Trisha Cabildo
# Date: February 9, 2023

import os
import pandas as pd
import openpyxl

folder_path = './text_files'
csv_file = 'text_files_transposed.csv'
excel_file = 'summary_text_files.xlsx'

def to_csv(folder_path, csv_file):
    dfs = []

    # Go into the directory and subdirectories to find text file. Then, append to a dataframe along with the file name.
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = subdir + os.sep + file
            if file_path.endswith(".txt"):
                df = pd.read_csv(file_path, header=None, sep=',', error_bad_lines=False)
                df.loc[-1] = [file] + [None] * (df.shape[1] - 1)
                df.index = df.index + 1
                df = df.sort_index()
                df = df.transpose()
                dfs.append(df)            
                dfs.append(pd.DataFrame(index=[0], columns=[0]))

    # Append to the dataframe
    df = pd.concat(dfs, axis=0, ignore_index=True)

    # Convert the dataframe into csv
    df.to_csv(csv_file, index=False, header=False)

def to_excel():
    # Load the CSV file into a pandas dataframe
    df1 = pd.read_csv(csv_file)

    # Save the dataframe as an Excel file
    df1.to_excel(excel_file, index=False)

    # Load the CSV file into an Excel workbook
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active
    ws.column_dimensions['A'].width = 40
    ws.column_dimensions['B'].width = 19
    ws.column_dimensions['C'].width = 19
    ws.column_dimensions['D'].width = 19
    ws.column_dimensions['E'].width = 19
    ws.column_dimensions['F'].width = 19
    ws.column_dimensions['G'].width = 23

    # Center the data in each cell
    for row in ws.rows:
        for cell in row:
            cell.alignment = openpyxl.styles.Alignment(horizontal='center')

    # Save the Excel workbook
    wb.save(excel_file)

def main():
    to_csv(folder_path, csv_file)
    to_excel()

if __name__ == '__main__':
    main()

