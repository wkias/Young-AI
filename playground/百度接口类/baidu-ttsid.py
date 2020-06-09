from aip import AipSpeech
import appid


client = AipSpeech(appid.ID, appid.KEY, appid.SK)
result = client.synthesis('你好', 'zh', 1, {
    'vol': 5,
})

if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)
