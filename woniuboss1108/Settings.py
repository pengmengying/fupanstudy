# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : Settings.py
@desc: 
@Created on: 2021/10/20 16:59
"""
import os


""" all file PATH meta """
template_path = os.path.join(os.path.dirname(__file__), 'template')
templatehtml_path = os.path.join(template_path, 'template.html')
print(templatehtml_path)
# mainFile = os.path.dirname(__file__) + '\\'

SourceDir = os.path.dirname(os.path.dirname(__file__))
TestDataDir = os.path.join(SourceDir,"woniuboss1108/")
PictureDir = os.path.join(TestDataDir,"Picture/")
print(TestDataDir)
# D:\study\threestudy\fourstudy\catmovie1029\catmovie1029.xls