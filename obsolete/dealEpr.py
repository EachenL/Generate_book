from EPRReaderPY.src.eprRead import EPRread
from olderEPRReader import oldEPRread
from recReader import RECreader
import os
import xlwt
import xlrd
import re

#'test'


def getfiles(dir):
    all = os.walk(dir)
    filepaths = []
    filenames = []
    for root, dirs, files in all:
        filenames = filenames + files
        for file in files:
            filepaths.append(os.path.join(root, file))
    return filepaths, filenames

if __name__ == "__main__":
    round = '第五批'
    doc_names = ['张悦', '韩阳', '李宝月', '李玲辉', '王晓琴']
    for doc_name in doc_names:
        # path = r'C:\Users\shund\Desktop\EPR数据\1-5批注释信息'+'\\'+round
        oripath = r'C:\Users\shund\Desktop\注视信息'
        path = oripath + '\\' + doc_name
        slidepath = r'Z:\pathology_group\Database\WsisAnalysisWithGaze\2021.11.13病理读片会\合格的\病理切片'
        slidepath = slidepath + '\\' + doc_name
        totalpath = r'Z:\pathology_group\Database\WsisAnalysisWithGaze\皮肤病理数据集（全部）'
        result = xlwt.Workbook()
        resdir = os.path.join(oripath, doc_name+'res.xls')
        sheet = result.add_sheet('shit1')
        dirs = os.listdir(path)
        all = os.walk(path)
        count = 0
        p, n = getfiles(totalpath)
        for root, dirs, files in all:
            for file in files:
                if file.__contains__('.epr') or file.__contains__('.rec'):
                    if round == '第五批' or round == '第四批':
                        eprfile = EPRread(os.path.join(root, file))
                        typestr = eprfile.typeStr
                        name = eprfile.slideName
                        sheet.write(count, 0, name)
                        nname = name.split('_')[0]
                        nnum = name.split('_')[1]
                        name = nname + '_' + nnum
                        for i in range(len(p)):
                            if p[i].__contains__(name):
                                sheet.write(count, 1, p[i])
                                break
                        sheet.write(count, 2, typestr)
                        count = count + 1
                    if round == '第三批':
                        eprfile = oldEPRread(os.path.join(root, file))
                        typestr = eprfile.typeStr
                        name = eprfile.slideName
                        num = ' '
                        name = name.split('.')[0]
                        try:
                            numstr = name.split('(')[1]
                            numstr = numstr.split(')')[0]
                            n = name.split('(')[0]
                            name = n.rstrip()
                            num = numstr
                            werqwer = 1
                        except:
                            qwer = 1
                            num = '0'
                        s = name + '_' + num

                        # sheet.write(count, 0, name)
                        for i in range(len(p)):
                            if p[i].__contains__(s):
                                sheet.write(count, 0, os.path.split(p[i])[1])
                                sheet.write(count, 1, p[i])
                                sheet.write(count, 2, typestr)
                                count = count + 1
                                break

                    if round == '第二批':
                        eprfile = oldEPRread(os.path.join(root, file))
                        typestr = eprfile.diag
                        name = eprfile.slideName

                        p1 = re.compile(r'\d{5}')
                        p2 = re.compile(r'\(\d\)')
                        p3 = re.compile(r'\d')

                        m1 = p1.match(name)
                        m2 = p2.findall(name)
                        m3 = ''
                        m1g = ''
                        if m1:
                            m1g = m1.group()
                        if m2:
                            m3 = p3.findall(m2[0])[0]
                        for i in range(len(p)):
                            if p[i].__contains__(m1g+'_'+m3):
                                sheet.write(count, 0, os.path.split(p[i])[1])
                                sheet.write(count, 1, p[i])
                                sheet.write(count, 2, typestr)
                                count = count + 1
                                break

                    if round == '第一批':
                        if file.__contains__('.rec'):
                            recfiledir = os.path.join(root, file)
                            ercfiledir = os.path.splitext(recfiledir)[0] + '.erc'

                            if os.path.isfile(recfiledir) and os.path.isfile(ercfiledir):
                                eprfile = RECreader(recfiledir, ercfiledir)
                                try:
                                    typestr = eprfile.type
                                    name = os.path.split(eprfile.fileName)[1]
                                except:
                                    print(recfiledir)
                                    break

                                p1 = re.compile(r'\d{5}')
                                p2 = re.compile(r'\(\d\)')
                                p3 = re.compile(r'\d')
                                m1 = p1.match(name)
                                m2 = p2.findall(name)
                                m3 = ''
                                m1g = ''
                                if m1:
                                    m1g = m1.group()
                                if m2:
                                    m3 = p3.findall(m2[0])[0]

                                for i in range(len(p)):
                                    if p[i].__contains__(m1g+'_'+m3):
                                        sheet.write(count, 0, os.path.split(p[i])[1])
                                        sheet.write(count, 1, p[i])
                                        sheet.write(count, 2, typestr)
                                        count = count + 1
                                        break
        result.save(resdir)

