import datetime
import os
import requests

today = datetime.date.today()
todayStr = str(today)
formatedToday = today.strftime("%Y%m%d")
urlist = []
for i in range(1, 21):
    if(i < 10):
        order = "0"+str(i)
    else:
        order = str(i)
    urlist.append("http://paper.people.com.cn/rmrb/page/" +
                  todayStr[:7]+"/"+todayStr[8:]+"/"+order +
                  "/rmrb"+formatedToday+order+".pdf")
savePath = ".\\RMRB"
if(not os.path.exists(savePath)):
    try:
        os.makedirs(savePath)
    except:
        print(savePath+" can not be created!")
for i in urlist:
    resp = requests.get(i)
    with open(savePath+"\\"+i[-14:], "wb") as pdf:
        pdf.write(resp.content)


def getFileName(filedir):

    file_list = [os.path.join(root, filespath)
                 for root, dirs, files in os.walk(filedir)
                 for filespath in files
                 if str(filespath).endswith('pdf')
                 ]
    return file_list if file_list else []


def MergePDF(savePath, outFile):
    output = PyPDF2.PdfFileWriter()
    outputPages = 0
    pdfFile = getFileName(savePath)
    if pdfFile:
        for f in pdfFile:
            print("路径：%s" % f)

            # 读取源PDF文件
            input = PyPDF2.PdfFileReader(open(f, "rb"))

            # 获得源PDF文件中页面总数
            pageCount = input.getNumPages()
            outputPages += pageCount
            print("页数：%d" % pageCount)

            # 分别将page添加到输出output中
            for iPage in range(pageCount):
                output.addPage(input.getPage(iPage))

        print("合并后的总页数:%d." % outputPages)
        # 写入到目标PDF文件
        outputStream = open(os.path.join(savePath, outFile), "wb")
        output.write(outputStream)
        outputStream.close()
        print("PDF文件合并完成！")
    else:
        print("没有可以合并的PDF文件！")


outFile = formatedToday + ".pdf"
MergePDF(savePath, outFile)
