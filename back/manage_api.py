import os
import cv2
import numpy as np
import config
import dbconnect

def insert_face(faceInfo):
    sql = "INSERT INTO "+ config.dbinfo()['database']+" (face_id, user_name, face_path, face_feature) VALUES (%s, %s, %s, %s)"
    val = (faceInfo["face_id"], faceInfo["user_name"], faceInfo["face_path"], faceInfo["face_feature"])
    dbconnect.insert(sql, val)

def update_face(faceInfo):
    sql = "UPDATE " + config.dbinfo()['database'] + " SET user_name = %s, face_path = %s, face_feature = %s WHERE face_id = %s"
    val = (faceInfo["user_name"], faceInfo["face_path"], faceInfo["face_feature"], faceInfo["face_id"])
    dbconnect.insert(sql, val)
    
def get_face(faceId):
    sql = "select from "+ config.dbinfo()['database'] +" where face_id=%s"
    val = (faceId)
    return dbconnect.insert(sql,val)

def delete_face(faceId):
    sql = 'delete from ' +config.dbinfo()['database'] +' where face_id=%s'
    val = (faceId)
    dbconnect.insert(sql,val)

def get_all_faces():
    sql = "select * from " + config.dbinfo()['database']
    return dbconnect.select(sql)

def get_faces_num():
    sql = "select count(*) from " + config.dbinfo()['database']
    return dbconnect.select(sql)