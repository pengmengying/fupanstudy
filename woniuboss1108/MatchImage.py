# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : MatchImage.py
@desc: 
@Created on: 2021/10/22 10:51
"""
import os
import time

from PIL import ImageGrab
from cv2 import cv2

from woniuboss1108.Settings import PictureDir


class MatchImage():

    def find_image_pos(self,template_image,threshold=0.8,is_delete=1):
        # 使用cv2 模块读取模板图片内容
        tempng = cv2.imread(template_image)
        # 获取 模板图片的 一半宽 一半高  目的：用于后期定位中心点
        width = int(tempng.shape[1] / 2)
        height = int(tempng.shape[0] / 2)

        time.sleep(2)

        # 使用 ImageGrab 截取当前屏幕保存到 b.png
        screen =PictureDir+ str(int(time.time()*1000))+".png"
        print(screen)
        ImageGrab.grab().save(screen)
        screenpng = cv2.imread(screen)

        res = cv2.matchTemplate(screenpng, tempng, cv2.TM_CCOEFF_NORMED)

        min, max, min_loc, max_loc = cv2.minMaxLoc(res) # 0.5    0.8  0.75
        print(min, max, )
        print("min_loc", min_loc)
        print("max_loc", max_loc)  # （width，height）

        if is_delete:
            os.remove(screen)
        if max< threshold: # 匹配的最佳结果小于我们的阈值 说明 没有匹配到
            return -1,-1
        else: # 说明有匹配到的结果
            # 得到目标在屏幕的坐标
            target_pos = (max_loc[0] + width, max_loc[1] + height)
            return target_pos


if __name__ == '__main__':
    res = MatchImage().find_image_pos(r"D:\Pycharm\PythonProject\auto-test45\Test\i.png",)
    print(res)