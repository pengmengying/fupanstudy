# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : KDT.py
@desc: 
@Created on: 2021/10/19 17:23
"""
import time

# 导入显性等待的API需要的模块
# 1> 等待对象模块
from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
# 2> 导入等待条件模块
from selenium.webdriver.support import expected_conditions as EC
# 3> 导入查询元素模块
from selenium.webdriver.common.by import By

from woniuboss1108.ExceptClass import assertException


class GetDriver():
    driver = {}

    @classmethod
    def get_driver(cls,type,noscreen=0):
        if not cls.driver.get(type):

            options = webdriver.ChromeOptions()
            options.add_argument('--disable-gpu')  # 禁用gpu，解决一些莫名的问题
            options.add_argument('--no-sandbox')  # 取消沙盒模式
            options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
            options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 以键值对的形式加入参数  规避被检查识别
            options.add_argument(
                'user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"')

            # 无界面 模式选项
            if noscreen:
                options.add_argument('--headless')  # 开启无界面模式

            if type=="Chrome":
                cls.driver[type] = webdriver.Chrome(
                    executable_path=r'D:\study\threestudy\fupan_study\woniuboss1108\drivers\chromedriver.exe',chrome_options=options)
            elif type=="Firefox":
                cls.driver[type]  = webdriver.Firefox()
        return  cls.driver[type]

class KDT():
    """创建一个关键字文档"""
    BY = {
        "class":"class name",
        "tag":"tag name",
        "id":"id",
        "xpath":"xpath",
        "name": "name",
        "css":"css selector",
        "link":"link text",
        "partiallink":"partial link text"
    }

    def __init__(self,type):
        self.driver = GetDriver.get_driver(type)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        self.f = Faker('zh_CN')

    def open(self,url):
        # 参数三 检查元素时间间隔

        self.driver.get(url)


    def get_element(self,by,value,):
        return self.wait.until(lambda driver: self.driver.find_element(  self.BY.get(by,by),value  ))

    def get_elements(self,by,value):
        return self.wait.until(lambda driver: self.driver.find_elements(self.BY.get(by, by), value))

    def selectbyname(self,by,value,name):
        sel = Select(self.driver.find_element(by,value))
        sel.select_by_visible_text(name)

    def sendkeys(self,by,value,text=None):
        if not  text:
            text = self.f.random_number(10)
        elif text=="批次总数量":
            content =self.get_element("id","goodsname").get_attribute("value") # 测试数据，该批次总数量为：10
            text = content.split("：")[1]
        self.get_element(by,value).clear()
        print(text)
        self.get_element(by,value).send_keys(text)
        # self.driver.find_element(self.BY.get(by,by),value).send_keys(text)
    def handle(self):
        print(self.driver.window_handles)
        self.driver.switch_to.window(self.driver.window_handles[-1])
    def myifram(self,by,value):  #当ui界面里出现了框中框，有fram的情况下这样进入fram
        dd = self.get_element(by,value)
        self.driver.switch_to.frame(dd)
     #当然如果想从iframe切出来，那么怎么办？
    # driver.switch_to.parent_frame()#从子frame切回到父frame
    # driver.switch_to.default_content()#切回主文档
    def myparent_frame(self):  #在同级fram的状况下，需要再切出来，再进去，，这里是切出来
        # dd = self.get_element(by,value)
        self.driver.switch_to.parent_frame()#从子frame切回到父frame
    def sendkeybyele(self,by,value,eleby,elevalue,type):
        """
        通过页面已有元素的值 输入到当前输入框
        :param by:  当前输入框定位的方式
        :param value:  当前输入框定位的方式 对应的值
        :param eleby:  目标元素定位的方式
        :param elevalue: 目标元素定位的方式  对应的值
        :param type:  目标元素获取  那种类型的值 text  属性：value
        :return:
        """
        text =  self.getelecont(eleby,elevalue,type)
        self.get_element(by, value).send_keys(text)

    def alertaccept(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    def click(self,by,value,index=None):
        if index:
            self.getelementbyindex(by,value,index).click()
        else:
            self.get_element(by, value).click()
        # self.driver.find_element(self.BY[by],value).click()

    def sleep(self,sec):
        time.sleep(int(sec))
        print("---------")
    def assertres(self,by,value,execpt,type="text"):  #断言
        content = self.getelecont(by,value,type)
        try:
            assert  content ==execpt
        except Exception as e:
            raise assertException(f"期望的结果 {execpt} 不等于实际的结果  {content} ")
        # if content ==execpt:
        #     print("测试通过")
        # else:
        #     print("测试失败")
        # assert content==execpt

    def assertresweb(self,execpt):  #断言web出现的弹窗问题
        content = self.driver.switch_to.alert.text
        try:
            assert  content ==execpt
        except Exception as e:
            raise assertException(f"期望的结果 {execpt} 不等于实际的结果  {content} ")

    def getelecont(self,by,value,type):
        if type == "text":
            content = self.get_element(by, value).text
        # content = self.driver.find_element(self.BY[by],value).text
        elif type == "value":
            content = self.get_element(by, value).get_attribute("value") #获得元素标签里的内容

        # print(content)
        return content

    def getelementbyindex(self,by,value,index:int):
        return self.get_elements(by,value)[int(index)]

    # def loginsuccess(self):
    def nologin(self):
        self.driver.delete_all_cookies()



if __name__ == '__main__':
    # kdt = KDT("Chrome")
    # getattr(kdt,"open") ("http://localhost:8080/WoniuSales-20180508-V1.4-bin/")
    # getattr(kdt,"sendkeys") ('id','password','123456')
    # getattr(kdt,"sendkeys") ('id','username','admin')
    # getattr(kdt,"click") ('class','form-control.btn-primary')
    # time.sleep(5)
    dr=webdriver.Firefox()
    dr.get('http://192.168.9.66:8080/WoniuBoss4.0/login')
