import appid
import time
import rec
from aip import AipSpeech

client = AipSpeech(appid.ID, appid.KEY, appid.SK)
file_name = str(time.time())
rec.rec(file_name)
with open(file_name, 'rb') as fp:
    file_context = fp.read()
res = client.asr(file_context, 'pcm', 16000, {
    'dev_pid': 1536,
})

print(res)
