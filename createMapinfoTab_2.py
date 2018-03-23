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

    def createPoint(self, layer, x, y, values = []):        #layer 为要将Feature添加到的 Layer x ,y 为 坐标 values 为字段值列表
        self.layer = layer
        self.x = x
        self.y = y
        self.values = values
        # 添加一个新的Feature
        self.featureDefn = newLayer.GetLayerDefn()  # 获取Feature 的类型
        self.newFeature = ogr.Feature(self.featureDefn)  # 创建Feature
        # 设定几何形状
        self.point = ogr.Geometry(ogr.wkbPoint)  # 创建一个点
        self.point.AddPoint(self.x, self.y)  # 设置 point的坐标
        self.newFeature.SetGeometry(self.point)  # 设置Featur的几何形状为point

        self.fields = ("poiName", "poiId", "Bound")
        for self.tmpValue  in (self.values,self.fields) :
            #设定Featur某字段的数值,这里设置 index 字段的值为 12
            self.newFeature.SetField(self.tmpValue[0],self.tmpValue[1])
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

    def createPolygon(self, layer,ringList):           #layer 为要将Feature添加到的 Layer ,
        self.layer = layer                              #rings 为封闭的折线ring 的列表,可以有1个或者2个元素(内环和外环)
        self.ringList = ringList                   #如:1个环:((0,0),(0,10),(10,10),(10,0))     2个环: (((0,0),(0,10),(10,10),(10,0)),((2.5,2.5),(7.5,2.5),(7.5,7.5),(2.5,7.5)))
        # 添加一个新的Feature
        self.featureDefn = newLayer.GetLayerDefn()  # 获取Feature 的类型
        self.newFeature = ogr.Feature(self.featureDefn)  # 创建Feature
        # 设定几何形状
        self.polygon = ogr.Geometry(ogr.wkbPolygon)  # 创建polygon区域
        self.ring = []      #定义ring的列表
        for i,self.ringPos in enumerate(self.ringList) :
            self.ring.append(ogr.Geometry(ogr.wkbLinearRing)) # 创建一个环 ring 并添加到列表 self.ring 中
            for self.tmpRing in self.ringPos :
                self.ring[i].AddPoint(self.tmpRing[0], self.tmpRing[1])  #循环添加点到Ring中
            self.ring[i].CloseRings()  # 用CloseRings闭合Ring，
            self.polygon.AddGeometry(self.ring[i])   # 把环 ring添加到  polygon
        self.newFeature.SetGeometry(self.polygon)   #设置Featur的几何形状为polygon (设置newFeature 为 区域 polygon )
        #设定Featur某字段的数值,这里设置 index 字段的值为 12
        self.newFeature.SetField('index', 13)
        # 将newFeature写入 newLayer
        self.layer.CreateFeature(self.newFeature)
        self.polygon.Destroy()  # 释放对象内存
        return  self.newFeature                  # 返回值为Feature 对象


    def setFieldValue(self,layer,valueList):
        self.layer = layer
        self.valueList = valueList
        pass

    def close(self,layer):
        layer.ResetReading()  # 复位
        self.dataSource.Destroy()  # 关闭数据源，相当于文件系统操作中的关闭文件




if __name__ == '__main__':
    newMap = CreateMapFeature('E:\\工具\\资料\\宝鸡\\研究\\Python\\python3\\gaode_range\\tab\\')
    fieldList = (("index", 0), ("name",(4,255)), ("lon", 2), ("lat" , 2))
    newLayer = newMap.newFile('assss.tab', fieldList)
    newMap.createPoint(newLayer, 10, 10,("","",""))
    newMap.createPoint(newLayer, 10, 15,("","",""))
    newMap.createPoint(newLayer, 10, 17,("","",""))
    newMap.createPoint(newLayer, 10, 18,("","",""))

    newMap.createLine(newLayer,((0,0),(3,4),(5,6),(7,8)))
    newMap.createLine(newLayer,((10,10),(8,9),(7,6),(3,5)))

    newMap.createPolygon(newLayer,(((0, 0), (0, 10), (10, 10), (10, 0)), ((2.5, 2.5), (7.5, 2.5), (7.5, 7.5), (2.5, 7.5))))

    newMap.close(newLayer)