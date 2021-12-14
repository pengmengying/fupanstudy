# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : run.py
@desc: 
@Created on: 2021/10/20 16:49
"""
import os
import sys

from woniuboss1108.Execute import ExecuteCase
from woniuboss1108.Settings import TestDataDir

print(sys.argv) # [ run.py ,filename=woniu.xlsx ,type=Chrome ]
argv_dict = {}
for i in sys.argv[1:]:
    key_value = i.split("=") # [filename,woniu.xlsx]
    argv_dict[key_value[0]] = key_value[1]

print(argv_dict)  # {'filename': 'woniu.xlsx', 'type': 'Chrome', 'caselist': '[1,2]'}
filename = TestDataDir+"\catmovie_1029.xls"
print(filename)
index = argv_dict.get("index",0)
type = argv_dict.get("type","Firefox")
caseidlist = eval(argv_dict.get('caselist','[]') )# '[1,2]'
reportname  =  argv_dict.get("reportname","res.html")
ex = ExecuteCase(filename,index,type)
ex.docase(caseidlist,reportname)