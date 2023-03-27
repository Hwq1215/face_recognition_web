import os
import cv2
import numpy as np
import config
import dbconnect

def factoryFace(face_id=0, user_name="unkown", fake=0 ,img_name="default#1.jpg",):
    faceInfo = {}
    faceInfo["face_id"] = face_id
    faceInfo["user_name"] = user_name
    faceInfo["fake"] = fake
    faceInfo["img_name"] = img_name
    return faceInfo

def insert_face(faceInfo):
    sql = "INSERT INTO face_info(face_id,user_name, fake, img_name) VALUES (%s ,%s, %s, %s)"
    val = (faceInfo["face_id"],faceInfo["user_name"], faceInfo["fake"], faceInfo["img_name"])
    dbconnect.insert(sql, val)

def update_face(faceInfo):
    sql = "UPDATE face_info SET user_name = %s, fake = %s, img_name = %s WHERE face_id = %s"
    val = (faceInfo["user_name"], faceInfo["fake"], faceInfo["img_name"], faceInfo["face_id"])
    dbconnect.insert(sql, val)
    
def get_face(faceId):
    sql = "select * from face_info where face_id=%d"
    val = (faceId)
    return dbconnect.insert(sql,val)

def has_face(faceId):
    sql = "select count(*) from face_info where face_id=%d"
    val = (faceId)
    return dbconnect.insert(sql,val)!=0

def delete_face(faceId):
    sql = "delete from face_info where face_id = %s"
    val = (str(faceId),)
    dbconnect.insert(sql,val)

def get_all_faces():
    sql = "select * from face_info" 
    face_infos = dbconnect.select(sql)
    result = []
    for face_info in face_infos:
        result.append({
            'faceId':face_info[0],
            'name':face_info[1],
            'imgSrc': face_info[3]
        })
    return result

def get_faces_by_page(page,page_size):
    page_size = int(page_size)
    page = int(page)
    sql = "select * from face_info limit %s,%s" 
    val = (page_size*(page-1),page_size)
    face_infos = dbconnect.select_param(sql,val)
    result = []
    for face_info in face_infos:
        result.append({
            'faceId':face_info[0],
            'name':face_info[1],
            'imgSrc': face_info[3]
        })
    return result

def get_faces_num():
    sql = "select count(*) from face_info" 
    return dbconnect.select(sql)[0][0]

def get_faces_maxid():
    sql = "select max(face_id) from face_info" 
    return dbconnect.select(sql)[0][0]