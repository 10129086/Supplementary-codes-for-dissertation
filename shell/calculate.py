#coding=UTF-8
import pandas as pd
import argparse
import os
from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser('Parameter error, please enter the correct parameter!')
parser.add_argument('-bp', help='Default base path for files to be processed')
parser.add_argument('-ep', help='Default excel generated path')
args = parser.parse_args()


def countCharInFile(charStr, filePath):
    '''
    Count the number of times the character appears in file
    :param charStr: character
    :param filePath: filepath
    :return: number of times
    '''
    import re
    with open(filePath, 'r') as f1:
        message = ''
        for item in f1:
            message += item.rstrip()
    counter = re.findall(charStr, message)
    return len(counter)


def validateStrInFile(str, filePath):
    '''
    Determine if the file contains the specified string
    :param str: character string
    :param filePath: filepath
    :return: whether contains yes-1
    '''
    with open(filePath, 'r') as f1:
        for item in f1:
            if item.find(str) != -1:
                return 1


def countbase(str, filePath):
    '''
    Get the number of bases in the file
    :param str: ARAF001(>ARAF001_1_g)
    :param filePath: filepath
    :return: number of bases
    '''
    with open(filePath, 'r') as f1:
        for line in f1:
            if line.startswith('>'):
                if line.find(str) != -1:
                    nextline = f1.readline()
                    return len(nextline)


base_path=args.bp
excel_path=args.bp

result_file_path = base_path + "/result.txt"
file_result = pd.DataFrame(pd.read_table(result_file_path, header=None))[[0, 1]]
file_result.drop_duplicates(inplace=True)
# print("=" * 100)
# print()

# Add a column to result.txt showing the number of strains covered by each gene
column = file_result[[1]]
file_result_new_column = []
for i, line in column.itertuples():
    file_name = line.split('/')[1]
    count = countCharInFile('>', base_path + "/unify/" + file_name)-1
    file_result_new_column.insert(i, count)
file_result.insert(loc=len(file_result.columns), column=2, value=file_result_new_column)
file_result.to_excel(excel_path+"/new_result.xlsx")


# Set the horizontal and vertical coordinates of the table to be created later
y_axis_list = []
counter = 0
for f in [f for f in os.listdir(base_path + "/unify/") if os.path.isfile(os.path.join(base_path + "/unify/", f))]:
    with open(base_path + "/unify/" + f, 'r') as rf:
        while True:
            line = rf.readline()
            if line == '':
                break
            elif line.startswith('>'):
                item = line.split('_')[0][1:] + '_'
                y_axis_list.insert(counter, item)
                counter = counter + 1
y_axis_list = list(set(y_axis_list))
y_axis_list = sorted(y_axis_list)
# print(y_axis_list)
x_axis_list = file_result[[0]]
# print(x_axis_list)

# Generate a new excel, 1 if the gene contains a strain, 0 if it does not
df_map = {}
df_map[' '] = y_axis_list
for index, column_val in x_axis_list.itertuples():
    column_index_list = []
    for i, row_index in enumerate(y_axis_list):
        file_name = file_result[file_result[0] == column_val].iloc[0][1].split('/')[1]
        value = validateStrInFile(row_index, base_path + "/unify/" + file_name)
        column_index_list.insert(i, value)
        df_map[column_val] = column_index_list
# print(df_map)
excel_df_01 = pd.DataFrame(df_map)
excel_df_01.set_index([" "], inplace=True)
excel_df_01.to_excel(excel_path+"/contains.xlsx")


# Generate another new excel with the number of bases for each gene in each strain
df_map[' '] = y_axis_list
for index, column_val in x_axis_list.itertuples():
    column_index_list = []
    for i, row_index in enumerate(y_axis_list):
        file_name = file_result[file_result[0] == column_val].iloc[0][1].split('/')[1]
        value = countbase(row_index, base_path + "/unify/" + file_name)
        column_index_list.insert(i, value)
        df_map[column_val] = column_index_list
# print(df_map)
excel_df_02 = pd.DataFrame(df_map)
excel_df_02.set_index([" "], inplace=True)
excel_df_02.to_excel(excel_path+"/basenumber.xlsx")
