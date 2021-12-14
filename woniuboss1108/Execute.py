# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : Execute.py
@desc: 
@Created on: 2021/10/20 14:07
"""
import json
import os
import time

from woniuboss1108.DataCollect import DataCollect
from woniuboss1108.KDT import KDT
from woniuboss1108.Parsexlsx import ParseXls
from woniuboss1108.Settings import TestDataDir, template_path, templatehtml_path

HTML_IMG_TEMPLATE = """
    <a href="data:image/png;base64, {}">
    <img src="data:image/png;base64, {}" width="800px" height="500px"/>
    </a>
    <br></br>
"""

class ExecuteCase():

    def __init__(self,filename,index=0,type="Firefox"):
        self.table = ParseXls(filename,index)
        self.kdt =KDT(type)
    def docase(self,caseid_list:list=None,outputpath="res.html"): # [1,3,5]
        init_time =time.time()

        if not caseid_list:
            caseid_list =self.table.get_all_caseid()

        for caseid in caseid_list:
            casedesc = self.table.get_desc(caseid)
            module = self.table.get_module(caseid)
            caseinfo = {"caseid":caseid,"description":casedesc,"className":module,"log":[]} # 记录每个case运行过程的详细数据
            start_time = time.time()
            result = "成功"
            # 开始执行case
            try:
                precond = self.table.get_precond(caseid) # nologin
                if precond:
                    getattr(self.kdt,precond)()
                steplist = self.table.get_step(caseid)
                for step in steplist:
                    # print('------------',step)
                    line_data = step.strip().split(",")  # ["open","Chrome","http://localhost:8080/WoniuSales-20180508-V1.4-bin/\n"]
                    # print("++++++++++++++=",line_data)
                    getattr(self.kdt , line_data[0])(*line_data[1:])  # ['Chrome', 'http://localhost:8080/WoniuSales-20180508-V1.4-bin/']

                DataCollect.testPass += 1
            except Exception as e:
                data = self.kdt.driver.get_screenshot_as_base64()
                cont = HTML_IMG_TEMPLATE.format(data, data)
                caseinfo['log'].append(str(e))
                caseinfo['log'].append(cont)
                result = "失败"

                DataCollect.testFail +=1
            # case执行完成
            case_run_time = str(round(time.time()-start_time,2)) + " s"
            caseinfo['spendTime'] = case_run_time
            caseinfo['status'] = result

            DataCollect.testResult.append(caseinfo) # 将每个case信息 存储到testResult中

        totaltime =str(round( time.time()- init_time,2)) +" s"
        DataCollect.totalTime = totaltime
        DataCollect.beginTime =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(init_time))

        # print(DataCollect.totalTime)
        # print(DataCollect.beginTime)
        # print(DataCollect.testResult)
        # print("测试通过",DataCollect.testPass)
        # print("测试失败",DataCollect.testFail)

        self.output_report(TestDataDir+outputpath)

    def output_report(self,reportpath, theme='theme_default'): # 'theme_default'
        """
            生成测试报告到指定路径下
        :return:
        """

        def render_template(params: dict, template: str):
            for name, value in params.items():
                name = '${' + name + '}' # title
                template = template.replace(name, value)
            return template
        # resultdata {“testName”: ,Testpass:,TestResult:}
        resultdata = { "testName":DataCollect.testName,"testPass":DataCollect.testPass,"testFail":DataCollect.testFail,
                       "testAll":DataCollect.testFail+DataCollect.testPass,"beginTime":DataCollect.beginTime,
                       "totalTime":DataCollect.totalTime,"testResult":DataCollect.testResult}
        with open(os.path.join(template_path, theme + '.json'), 'r') as theme:
            render_params = {
                **json.load(theme), # 将theme_default.json的数据 读取出来解析
                'resultData': json.dumps(resultdata, ensure_ascii=False, indent=4) # 将刚才收集好的数据变成json字符串
            }


        with open(templatehtml_path, 'rb') as file:
            body = file.read().decode('utf-8') # body就是template.html的内容
        with open(reportpath, 'w', encoding='utf-8', newline='\n') as write_file:
            html = render_template(render_params, body) # 渲染模板
            write_file.write(html)

if __name__ == '__main__':

    ex = ExecuteCase(r'D:\study\threestudy\fupan_study\woniuboss1108\catmovie_1029.xls',0,"Firefox")
    ex.docase([1,2])

