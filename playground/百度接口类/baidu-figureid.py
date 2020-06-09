from aip import AipSpeech
import appid


APP_ID = appid.ID
API_KEY = appid.KEY
SECRET_KEY = appid.SK

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content('example.jpg')

""" 调用人体关键点识别 """
client.bodyAnalysis(image)
