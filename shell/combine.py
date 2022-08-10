import os
import argparse

parser = argparse.ArgumentParser('Parameter error, please enter the correct parameter!')
parser.add_argument('-d', help='pancentroids')
parser.add_argument('-f', help='sum_file.fasta')
args = parser.parse_args()

# Name of the final summary file
sum_file_name = args.f

# Enter the path where the file to be processed is located
base_path = args.d
file_path = base_path+"/pancentroids/"

with open(base_path+'/'+sum_file_name, 'w') as wf:
    for file_name in os.listdir(file_path):
        if os.path.isfile(file_path+file_name):
            with open(file_path+file_name, 'r') as rf:
                while True:
                    line = rf.readline()
                    if line == '':
                        break
                    elif line.startswith('>'):
                        wf.write(line.replace('\n', '/')+file_name+'\n')
                        # print(line.replace('\n', '/')+file_name)
                    else:
                        wf.write(line)
                        # print(line)