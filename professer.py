import os, re
def getFilePaths(dir, suffix):
    # 获取指定目录（包含子孙目录）下所有指定后缀的文件的路径
    paths = []
    suffix = '.' + suffix
    walkGenerator = os.walk(dir)
    for root_path, dirs, files in walkGenerator:
        if len(files) < 1:
            continue
        for file in files:
            file_name, suffix_name = os.path.splitext(file)
            if suffix_name == suffix:
                paths.append(os.path.join(root_path, file))

    return paths

def getLineCnt(path):
    # 获取指定文件的行数，剔除空行
    lineCnt = 0
    with open(path, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            if not line.isspace():
                lineCnt += 1
    return lineCnt

def getCleanFile(path):
    # 剔除指定文件中的空行和注释，返回无空行、注释的内容、长度
    newData = []

    singleComment = '//.*'
    multComment = r'/\*(?:.|\s)*?\*/'

    target0 = re.compile(singleComment)
    target1 = re.compile(multComment)
    with open(path, 'r', encoding='UTF-8') as f:
        data = f.read()
        result0 = target0.findall(data)
        result = target1.findall(data)
        result += result0
        for r in result:
            data = data.replace(r, '')

        # 剔除空行
        datas = data.splitlines()
        for d in datas:
            if d.strip():
                newData.append(d)

    return newData, len(newData)


def clearContent(path):
    '''清空内容'''
    with open(path, 'w') as f:
        f.write('')

def addContent(path, data):
    '''追加内容,data为数组'''
    with open(path, 'a') as f:
        for d in data:
            f.write(d+'\n')

if __name__ == '__main__':
    # 指定目录
    targetDir = './front/face_front'
    # 指定后缀
    suffix = 'vue'
    paths = getFilePaths(targetDir, suffix)

    '''
    # 获取总行数（剔除空行）
    lineCnt = 0
    for p in paths:
        lineCnt += getLineCnt(p)
    print('行数：', lineCnt)
    '''

    # 获取3000行，指定最后的内容
    targetLength = 1000
    lastPath = 'front/face_front/src/App.vue'
    lastData, lastLength = getCleanFile(lastPath)
    targetLength -= lastLength

    outputPath = '全部代码.txt'
    clearContent(outputPath)
    for p in paths:
        if p == lastPath:
            continue
        data, length = getCleanFile(p)
        addContent(outputPath, data)
        targetLength -= length
        if targetLength <= 0:
            break
    addContent(outputPath, lastData)
    print('全部代码整理完成！')