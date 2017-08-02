# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 09:39:44 2017

@author: Xie
"""

import xlrd
from Match import Match
from predict_disease import Diagnosis

INDEX_OF_DEPT = 0
HUNDRED = 100

def main():
    fname='分诊评测集标注.xlsx'
    bk=xlrd.open_workbook(fname)
    sh = bk.sheet_by_name("Sheet1")

    #获取行数
    nrows = sh.nrows
    #获取列数
    ncols = sh.ncols

    #获取第八列数据 
    DES_list = []
    for i in range(1,nrows):
        DESvalue = sh.cell_value(i,7)
        DES_list.append(DESvalue)
   
    # Get the departments (correct results)
    DEP_list=[]
    for i in range(1,nrows):
        DEPvalue = sh.cell_value(i,0)
        DEP_list.append(DEPvalue)

    count = 0
    i = 0
    d = Diagnosis()
    # report to log discrepancies between prediction and actual results
    report = {}

    # Process the natural language and extract keywords
    matcher = Match()
    matcher.load("disease_symptom.json")
    for describe in DES_list:
        # Extracting keywords takes place here
        describe = matcher.match(describe).rstrip()
        request = [{'request':{'text':describe}}]
        response = d.run(json.dumps(request, ensure_ascii = False))
        predictedDept = response.get('text')[INDEX_OF_DEPT]
        if predictedDept == DEP_list[i]:
            count += 1
        else:
            report[describe] = [predictedDept, DEP_list[i]]
        i += 1

    percentage = (count/nrows) * HUNDRED
    print ("Estimated accuracy: " + percentage + "%")
    print ("Incorrect results: ")
    print (report)

if __name__ == '__main__':
    main()
