import datetime
import zlib
import hashlib
import os
from imgid.img2b64 import img2b64
from imgid.img_api import face
import sqliteDB


def db(respond, json, img_hash, bytes_img):
    for i in range(0, respond['result']['face_num']):
        faceContent = (
            respond['result']['face_list'][i]['face_token'],
            datetime.datetime.now(),
            respond['result']['face_list'][i]['age'],
            respond['result']['face_list'][i]['beauty'],
            respond['result']['face_list'][i]['expression']['type'],
            respond['result']['face_list'][i]['face_shape']['type'],
            respond['result']['face_list'][i]['gender']['type'],
            respond['result']['face_list'][i]['glasses']['type'],
            respond['result']['face_list'][i]['race']['type'],
            respond['result']['face_list'][i]['quality']['blur'],
            respond['result']['face_list'][i]['quality']['illumination'],
            respond['result']['face_list'][i]['quality']['completeness'],
            respond['result']['face_list'][i]['emotion']['type'],
            respond['result']['face_list'][i]['face_type']['type'],
            json,
            img_hash,
        )
        faceDB.insert(faceContent)
        print(faceContent)
    for i in range(0, respond['result']['face_num']):
        probContent = (
            respond['result']['face_list'][i]['face_token'],
            respond['result']['face_list'][i]['face_probability'],
            respond['result']['face_list'][i]['age'],
            respond['result']['face_list'][i]['beauty'],
            respond['result']['face_list'][i]['expression']['probability'],
            respond['result']['face_list'][i]['face_shape']['probability'],
            respond['result']['face_list'][i]['gender']['probability'],
            respond['result']['face_list'][i]['glasses']['probability'],
            respond['result']['face_list'][i]['race']['probability'],
            respond['result']['face_list'][i]['emotion']['probability'],
            respond['result']['face_list'][i]['face_type']['probability'],
        )
        probDB.insert(probContent)
    picDB.insert((img_hash, bytes_img))


def main(path=None):
    if path is not None:
        bytes_img = img2b64.file(path)
    else:
        bytes_img = img2b64.cv()
    b64_img = img2b64.b64(bytes_img)
    respond = api.face(b64_img)
    img_hash = hashlib.md5(bytes_img).hexdigest()
    if respond['error_msg'] == 'SUCCESS':
        json = zlib.compress(api.getJson().encode('utf-8'))
        # api.save()
        db(respond, json, img_hash, bytes_img)
    else:
        print(respond['error_msg'])


api = face()
faceDB = sqliteDB.sqliteDB('face')
probDB = sqliteDB.sqliteDB('face_probability')
picDB = sqliteDB.sqliteDB('img')

# 以下两种方式任选一种

# 使用摄像头
main()

# 使用测试文件
# files = ['img/' + x for x in os.listdir('img')]
# for i in files:
#     print(i)
#     main(i)
