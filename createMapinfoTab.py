#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
import osr
try:
    from osgeo import ogr
except:
    import ogr



# 在GDAL 中 feature 指的就是 mapinfo中的 点 线 折线  区域等
#driver = ogr.GetDriverByName("ESRI Shapefile")    # .shp 文件驱动
driver = ogr.GetDriverByName("Mapinfo File")      # mapinfo   .tab 文件驱动




class CreateMapFeature():
    def __init__(self,path):
        self.path = path

    def newFile(self, filename, fieldList):
        #创建新文件
        self.filename = filename                        #filename文件名,不包含路径 字符串格式
        self.fieldList = fieldList                      #fieldList ,图层的表格字段  列表格式,(("index", 0), ("name",(4,255)), ("lon", 2), ("lat" , 2))
                                                        # 列表为 字段的名字 和 数据类型, 0代表整数 , 2 代表 浮点数 , 4代表字符串(如果是字符串格式 则列表的第二个元素为 4和字符串的长度的列表
        if os.path.isfile(self.path + self.filename):  # 如果文件存在的话 重新起一个文件名
            self.filename = self.path + r"/new_" + self.filename
            print("File is exist,Create anothor, Name is :" + self.filename)
        else:
            self.filename = self.path + self.filename
            print("Create file, Name is :" + self.filename)
        self.dataSource = driver.CreateDataSource(self.filename)        # 创建 文件
        self.newLayer = self.dataSource.CreateLayer('newLayer')  # 创建图层testLayer2
        for self.field in self.fieldList:                 #创建字段名字典中的所有字段
            if self.field[1] == 0 :
                self.fieldType = ogr.OFTInteger
                self.newField = ogr.FieldDefn(self.field[0], self.fieldType)  # 添加一个新字段
            elif self.field[1] == 2 :
                self.fieldType = ogr.OFTReal
                self.newField = ogr.FieldDefn(self.field[0], self.fieldType)  # 添加一个新字段
            elif self.field[1][0] == 4 :
                self.fieldType = ogr.OFTString
                self.newField = ogr.FieldDefn(self.field[0], self.fieldType)  # 添加一个新字段
                self.newField.SetWidth(self.field[1][1])          #如果新字段是字符串类则必须要指定宽度
            self.newLayer.CreateField(self.newField)  # 将新字段指配到layer
        return  self.newLayer                           # 返回值为新建文件的图层 Layer 对象


    def deleteFile(self, filename):
        self.filename = filename
        self.filename = self.path + self.filename
        if os.path.isfile(self.filename):  # 如果文件存在的话删除
            driver.DeleteDataSource(self.filename)  # 删除一个文件
            print("File well be delete :" + self.filename)
        else:
            print("File is not exist :" + self.filename + ",Plase Check it!")


    def createPoint(self, layer, x, y):        #layer 为要将Feature添加到的 Layer x ,y 为 坐标
        self.layer = layer
        self.x = x
        self.y = y
        # 添加一个新的Feature
        self.featureDefn = newLayer.GetLayerDefn()  # 获取Feature 的类型
        self.newFeature = ogr.Feature(self.featureDefn)  # 创建Feature
        # 设定几何形状
        self.point = ogr.Geometry(ogr.wkbPoint)  # 创建一个点
        self.point.AddPoint(self.x, self.y)  # 设置 point的坐标
        self.newFeature.SetGeometry(self.point)  # 设置Featur的几何形状为point
        #设定Featur某字段的数值,这里设置 index 字段的值为 12
        self.newFeature.SetField('index', 12)
        # 将newFeature写入 newLayer
        self.layer.CreateFeature(self.newFeature)
        self.point.Destroy()  # 释放对象内存
        return  self.newFeature                  # 返回值为Feature 对象

    def createLine(self, layer,pointList):           #layer 为要将Feature添加到的 Layer , points 为折线的节点x,y坐标的列表如 :((1,1),(3,3),(4,2))
        self.layer = layer
        self.pointList = pointList
        # 添加一个新的Feature
        self.featureDefn = newLayer.GetLayerDefn()  # 获取Feature 的类型
        self.newFeature = ogr.Feature(self.featureDefn)  # 创建Feature
        # 设定几何形状
        self.line = ogr.Geometry(ogr.wkbLineString)  # 创建一条折线
        for self.pointPos in self.pointList :
            self.line.AddPoint(self.pointPos[0], self.pointPos[1])  # 循环添加所有的节点
        self.newFeature.SetGeometry(self.line)  # 设置Featur的几何形状为line
        #设定Featur某字段的数值,这里设置 index 字段的值为 12
        self.newFeature.SetField('index', 12)
        # 将newFeature写入 newLayer
        self.layer.CreateFeature(self.newFeature)
        self.line.Destroy()  # 释放对象内存
        return  self.newFeature                  # 返回值为Feature 对象






    def close(self,layer):
        layer.ResetReading()  # 复位
        self.dataSource.Destroy()  # 关闭数据源，相当于文件系统操作中的关闭文件




"""
newLayer = dataSource.CreateLayer('testLayer2', geom_type=ogr.wkbPoint)    #创建图层testLayer2

newField = ogr.FieldDefn('index', ogr.OFTInteger)#添加一个新字段，只能在layer里面加
#fieldDefn.SetWidth(4)                            #如果新字段是字符串类则必须要指定宽度
newLayer.CreateField(newField)                       #将新字段指配到layer

#########################################################################
#添加一个新的Feature
featureDefn = newLayer.GetLayerDefn()        # 获取Feature 的类型
newFeature = ogr.Feature(featureDefn)      #创建Feature

#设定几何形状
point = ogr.Geometry(ogr.wkbPoint)          #创建一个点
point.AddPoint(10,20,10)                       #设置 point的坐标
newFeature.SetGeometry(point)              #设置Featur的几何形状为point
newFeature.SetField('index',12)            #设定Featur某字段的数值,这里设置 index 字段的值为 12
newLayer.CreateFeature(newFeature)          #将newFeature写入 newLayer
#################################################################################


#设定几何形状
line = ogr.Geometry(ogr.wkbLineString)          #创建一条直线(折线)
line.AddPoint(10,10)                       #给line添加一个点
line.AddPoint(20,20)                       #给line添加一个点
line.AddPoint(0,20)                       #给line添加一个点
line.SetPoint(1,25,25)                      #修改 line 的第 1 个点的坐标 为 25,25
print(line.GetPointCount())                 #获取 直线line的 节点数
print(line.GetX(0))                         #读取0号点的x坐标和y坐标
print(line.GetY(0))






"""


if __name__ == '__main__':
    newMap = CreateMapFeature('E:\\工具\\资料\\宝鸡\\研究\\Python\\python3\\gaode_range\\tab\\')
    fieldList = (("index", 0), ("name",(4,255)), ("lon", 2), ("lat" , 2))
    newLayer = newMap.newFile('assss.tab', fieldList)
    newMap.createPoint(newLayer, 10, 10)
    newMap.createPoint(newLayer, 10, 15)
    newMap.createPoint(newLayer, 10, 17)
    newMap.createPoint(newLayer, 10, 18)

    newMap.createLine(newLayer,((0,0),(3,4),(5,6),(7,8)))
    newMap.createLine(newLayer,((10,10),(8,9),(7,6),(3,5)))
    newMap.close(newLayer)