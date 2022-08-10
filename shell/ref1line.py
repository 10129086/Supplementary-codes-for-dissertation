#coding=UTF-8

import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser('Parameter error, please enter the correct parameter!')
parser.add_argument('-bp', help='basepath')
parser.add_argument('-ref', help='refpath')
args = parser.parse_args()


#base_path = "./"
base_path = args.bp
#ref_path="./result/ref/"
ref_path = args.ref

if not os.path.isdir(ref_path):
    os.mkdir(ref_path)

result_file_path = base_path+"/result/result.txt"
file_result = pd.DataFrame(pd.read_table(result_file_path, header=None))[[0, 1]]
file_result.drop_duplicates(inplace=True)


with open(base_path + "/referencegene.fasta", 'r') as f1:
    msg = ""
    flag = ""
    while True:
        item = f1.readline()
        if item.startswith(">") or item == '':
            if msg != "":
                if not file_result[file_result[0] == flag].empty:
                    file_name = file_result[file_result[0] == flag].iloc[0][1].split('/')[1]
                    with open((ref_path+"/{}").format(file_name),'w') as newf:
                        with open(base_path + "/pancentroids/" + file_name, "r") as originfile:
                            newf.write(msg+'\n')
                            msg = ""
                            newf.write(originfile.read())
            flag = item.replace('\n', '')[1:]
        msg += item
        if item == '':
            break