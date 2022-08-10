coding="UTF-8"
import os
import argparse

parser = argparse.ArgumentParser('Parameter error, please enter the correct parameter!')
parser.add_argument('-ref', help='ref')
parser.add_argument('-u', help='unify')
args = parser.parse_args()

# Enter the path where the file to be processed is located
file_path=args.ref
#Enter the path where the file to be generated
result_dir=args.u

if not os.path.exists(result_dir):
    os.mkdir(result_dir)


for file_name in os.listdir(file_path):
    
        if os.path.isfile(file_path+file_name):
            with open(file_path+file_name, 'r') as rf:      
                with open(result_dir+"/{}".format(file_name),'w') as newf:
                    for line in rf:    
                        if line == '':
                            break
                        elif line.startswith('>'):
                            line=str(line)
                            line1=line.split('_')[0]+'_'+'\n'
                            newf.write(line1)
                        else:
                            newf.write(line)
                  