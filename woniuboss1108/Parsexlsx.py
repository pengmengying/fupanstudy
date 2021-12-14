# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : Parsexlsx.py
@desc: 读取表格里面的信息
@Created on: 2021/10/20 9:57
"""

import xlrd


class ParseXls():
    """解析execl 将execl 提取成我们所需要的数据"""

    def __init__(self,filename,index):
        execl = xlrd.open_workbook(filename)
        self.table = execl.sheet_by_index(index)

    def get_caseid(self,row): # 告诉你行号 获取对应的caseid
        return self.table.cell_value(row,0)

    def get_row_bycaseid(self,caseid): # 根据caseid获取行号
        res = self.table.col_values(0)
        row = res.index(float(caseid))
        return row

    def get_res_bycol(self,caseid,col): #通过传入不同的列获取对应的结果
        row = self.get_row_bycaseid(caseid)
        return self.table.cell_value(row, col)

    def get_step(self,caseid): #  根据行号 获取指定case的步骤   根据caseid获取行号
        stepstr= self.get_res_bycol(caseid,6)
        # print(stepstr)
        steplist = stepstr.split("\n")
        # print(steplist)
        return steplist

    def get_desc(self,caseid): #获取描述信息
        return self.get_res_bycol(caseid, 2)

    def get_precond(self,caseid):
        """获取前置条件的方法"""
        return self.get_res_bycol(caseid, 5)

    def get_expectres(self,caseid): #
        return self.get_res_bycol(caseid, 4)

    def get_module(self,caseid):  #获取模块
        return self.get_res_bycol(caseid, 1)

    def get_all_caseid(self):
        return self.table.col_values(0,start_rowx=3)
if __name__ == '__main__':
    table = ParseXls(r"D:\study\threestudy\fupan_study\woniuboss1108\catmovie_1029.xls",0)
    # print(table.get_caseid(2))
    step = table.get_step(1)
    print(step)# ${ styel}
    # res  = step.split("\n")
    # print(res)
    # print(table.get_step(2),type(table.get_step(2)))
    # print(table.get_all_caseid())