import appid
import aip
import json


class face():
    def __init__(self, ID=appid.ID, KEY=appid.KEY,
                 SK=appid.SK, imageType='BASE64'):
        self.__ID = ID
        self.__KEY = KEY
        self.__SK = SK
        self.imageType = imageType
        self.options = {}
        self.options["face_field"] = appid.FIELD
        self.options["max_face_num"] = 10
        # self.options["face_type"] = "LIVE"
        # self.options["liveness_control"] = "LOW"

    def face(self, b64_img, face_field=appid.FIELD):
        self.faceAPI = aip.AipFace(self.__ID, self.__KEY, self.__SK)
        self.respond = self.faceAPI.detect(
            b64_img, self.imageType, self.options)
        return self.respond

    def getJson(self):
        return json.dumps(self.respond)

    def save(self, path='img.json'):
        with open(path, 'w') as f:
            json.dump(self.respond, f)

    def __call__(self, b64_img):
        self.face(b64_img)
