#!/bin/bash
###################define_path
BASE_PATH="$(dirname $0)"
RESULT_DIR="${BASE_PATH}/result"

REF_3="${RESULT_DIR}/ref/"
UNIFY_PATH="${RESULT_DIR}/unify/"
MUSCLE_PATH="${RESULT_DIR}/muscle/"
STABLE_PATH="${RESULT_DIR}/stable/"
SNP_PATH="${RESULT_DIR}/snp/"

R_FILE='biomart_get_sequence.r'

SUM_FILE_NAME='sum_file.fasta'
###################define_path



#1.1 Extracting the gene sequences from genelist.txt by R,$1 is the first argument in command line
echo '[ LOG ] step(1.1) START===>>'
R_res=`Rscript ${R_FILE} $1 ${BASE_PATH}`
echo '[ LOG ] step(1.1) END<<===${R_res}'

#1.2 run combine.python
echo '[ LOG ] step(1.2) START===>>'
py_res=`python ${BASE_PATH}/combine.py -d ${BASE_PATH} -f ${SUM_FILE_NAME}`
echo '[ LOG ] step(1.2) END<<===${py_res}'


#2.blast
echo '[ LOG ] step(2.2) START===>>'
res=`makeblastdb -in ${BASE_PATH}/sum_file.fasta  -dbtype nucl -out AF1163`
# res=`makeblastdb -in ${BASE_PATH}/sum_file.fasta  -dbtype nucl -out AF1163 -blastdb_version 4`
echo '[ LOG ] step(2.2) END<<===${res}'
echo '[ LOG ] step(2.3) START===>>'
if [ ! -d ${RESULT_DIR} ];then
	mkdir ${RESULT_DIR}
fi
res=`blastn -query ${BASE_PATH}/referencegene.fasta -db AF1163 -max_target_seqs 1 -outfmt 6 -out "${RESULT_DIR}/result.txt"`
echo '[ LOG ] step(2.2) END<<===${res}'


#3.1 run ref1line.py
echo '[ LOG ] step(3.1) START===>>'
if [ ! -d ${REF_3} ];then
	mkdir ${REF_3}
fi
res=`python ${BASE_PATH}/ref1line.py -bp ${BASE_PATH} -ref ${REF_3}`
echo '[ LOG ] step(3.1) END<<===${res}'

#3.2 run unify.py
echo '[ LOG ] step(3.2) START===>>'
res=`python ${BASE_PATH}/unify.py -ref ${REF_3} -u ${UNIFY_PATH}`
echo '[ LOG ] step(3.2) END<<===${res}'

#3.3 run calculate.py
echo '[ LOG ] step(3.3) START===>>'
res=`python ${BASE_PATH}/calculate.py -bp "${RESULT_DIR}" -ep "${RESULT_DIR}"`
echo '[ LOG ] step(3.3) END<<===${res}'


# 4.1 muscle
echo '[ LOG ] step(4.1) START===>>'
if [ ! -d ${MUSCLE_PATH} ];then
	mkdir ${MUSCLE_PATH}
fi
for file in `ls ${UNIFY_PATH}`
do
if [ -d "${UNIFY_PATH}$file" ]
then
  echo "$file is directory"
elif [ -f "${UNIFY_PATH}$file" ]
then
  echo "START muscle---> $file"
  muscle_res=`./muscle -in ${UNIFY_PATH}$file -out ${MUSCLE_PATH}$file`
  echo "FINISH muscle---> $file"
fi
done
echo '[ LOG ] step(4.1) END<<===${muscle_res}'

# 4.2 muscle stable
echo '[ LOG ] step(4.2) START===>>'
if [ ! -d ${STABLE_PATH} ];then
	mkdir ${STABLE_PATH}
fi
for file in `ls ${UNIFY_PATH}`
do
if [ -d "${UNIFY_PATH}$file" ]
then
  echo "$file is directory"
elif [ -f "${UNIFY_PATH}$file" ]
then
  echo "START stable python shell"  
  py_res=`python ${BASE_PATH}/stable.py ${UNIFY_PATH}$file ${MUSCLE_PATH}$file > ${STABLE_PATH}$file`
echo "FINISH process python shell"
fi
done
echo '[ LOG ] step(4.2) END<<===${py_res}'


# 5.snp-site
echo '[ LOG ] step(5) START===>>'
if [ ! -d ${SNP_PATH} ];then
	mkdir ${SNP_PATH}
fi
for file in `ls ${STABLE_PATH}`
do
if [ -d "${STABLE_PATH}$file" ]
then
  echo "$file is directory"
elif [ -f "${STABLE_PATH}$file" ]
then
  echo "START snp---> $file"
  snp_res=`snp-sites -v -m -p -o ${SNP_PATH}$file  ${STABLE_PATH}$file`
  echo "FINISH snp---> $file"
fi
done
echo '[ LOG ] step(5) END<<===${snp_res}'



















