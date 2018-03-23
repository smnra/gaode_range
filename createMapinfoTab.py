#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2013-8-27

@author: chenll
'''
import os, sys
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import numpy


# 读取shap文件
def readShap():
    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    # 注册所有的驱动
    ogr.RegisterAll()
    # 数据格式的驱动
    #driver = ogr.GetDriverByName('ESRI Shapefile')    #.shp 格式文件驱动
    driver = ogr.GetDriverByName("Mapinfo File")    #mapinfo tab文件驱动
    ds = driver.Open(r'C:\Users\Administrator\Desktop\mapinfo\Grid_Mro_le_110Data.TAB')
    if ds is None:
        print('Grid_Mro_le_110Data.TAB')
        sys.exit(1)
    # 获取第0个图层
    layer0 = ds.GetLayerByIndex(0)
    # 投影
    spatialRef = layer0.GetSpatialRef()
    # 输出图层中的要素个数
    print('要素个数=%d', layer0.GetFeatureCount(0))
    print('属性表结构信息')
    defn = layer0.GetLayerDefn()
    iFieldCount = defn.GetFieldCount()
    for index in range(iFieldCount):
        oField = defn.GetFieldDefn(index)
        print('%s: %s(%d.%d)' % (
        oField.GetNameRef(), oField.GetFieldTypeName(oField.GetType()), oField.GetWidth(), oField.GetPrecision()))

    feature = layer0.GetNextFeature()
    # 下面开始遍历图层中的要素
    while feature is not None:
        # 获取要素中的属性表内容
        for index in range(iFieldCount):
            oField = defn.GetFieldDefn(index)
            line = " %s (%s) = " % (oField.GetNameRef(), oField.GetFieldTypeName(oField.GetType()))
            if feature.IsFieldSet(index):
                line = line + "%s" % (feature.GetFieldAsString(index))
            else:
                line = line + "(null)"
            print(line)
            # 获取要素中的几何体
        geometry = feature.GetGeometryRef()
        print(geometry)
        # 为了演示，只输出一个要素信息
        break
    feature.Destroy()
    ds.Destroy()


# 创建shap文件
def createShap():
    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    # 注册所有的驱动
    ogr.RegisterAll()
    # 数据格式的驱动
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource("E:\\arcgis\\point")
    shapLayer = ds.CreateLayer("poi", geom_type=ogr.wkbPoint)
    # 添加字段
    fieldDefn = ogr.FieldDefn('id', ogr.OFTString)
    fieldDefn.SetWidth(4)
    shapLayer.CreateField(fieldDefn)
    # 创建feature
    defn = shapLayer.GetLayerDefn()
    feature = ogr.Feature(defn)
    # 添加属性
    feature.SetField("id", "liu")
    # 添加坐标
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(float(113.56647912), float(22.16128203))
    feature.SetGeometry(point)
    shapLayer.CreateFeature(feature)
    feature.Destroy()
    # 指定投影
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(32612)
    prjFile = open("E:\\arcgis\\point\\poi.prj", 'w')
    sr.MorphToESRI()
    prjFile.write(sr.ExportToWkt())
    prjFile.close()
    ds.Destroy()


def main():
    readShap()
    createShap()


if __name__ == "__main__":
    main()
