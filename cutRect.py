# -*- coding:UTF-8 -*-

import json
import requests
import time

def cutRect(leftTop,rightBottom):
    #参数为 左上角 和 右下角坐标的 列表    例如 leftTop:[0,10]   rightBottom:[10,0]
    #把矩形框分割为四等份
    rects = []            #列表用于保存分割后的四个矩形
    leftTopRect = []      #用于左上角矩形的坐标
    rightTopRect = []       #用于右上角矩形的坐标
    leftBottomRect = []      #用于左下角矩形的坐标
    rightBottomRect = []       #用于右下角矩形的坐标

    width = rightBottom[0] - leftTop[0]             #Rect的宽度
    height = leftTop[1] - rightBottom[1]            #Rect的高度

    leftTopRect = [[leftTop[0],leftTop[1]],[leftTop[0] + width/2 ,rightBottom[1] + height/2]]   #左上角Rect的坐标

    rightTopRect = [[leftTop[0] + width/2, leftTop[1]],[rightBottom[0], rightBottom[1] + height/2]]  # 右上角Rect的坐标

    leftBottomRect = [[leftTop[0], rightBottom[1] + height/2], [leftTop[0] + width/2, rightBottom[1]]]  # 左下角Rect的坐标

    rightBottomRect = [[leftTop[0] + width/2 ,rightBottom[1] + height/2], [rightBottom[0], rightBottom[1]]]  # 左下角Rect的坐标

    rects = [leftTopRect, rightTopRect, leftBottomRect, rightBottomRect]

    return rects

if __name__ == '__main__' :
    leftTop = [0, 10]
    rightBottom = [10,0]
    rects = cutRect(leftTop, rightBottom)
    for rect in rects:
        print(rect)