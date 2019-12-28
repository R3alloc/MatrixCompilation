#$OS-$CUDA_VERSION-$MPI_VERSION-$CMAKE_VERSION-$FINAL_RESULT
#axis
#axis_str = "OS-CUDA_VERSION-MPI_VERSION-CMAKE_VERSION-FINAL_RESULT"
#axis_list = axis_str.split('-')
##实际上就是下面这段代码
##axis_list = ['OS', 'CUDA_VERSION', 'MPI_VERSION','GCC_VERSION','CMAKE_VERSION', 'FINAL_RESULT']
##显式声明一个列表
#axis_value_list = list()
#axis_value_list.append(['centos7'])
#axis_value_list.append([9.0, 9.2, 10.0, 10.1])
#axis_value_list.append([3.0, 3.2])
#axis_value_list.append([3.3, 3.5, 3.8])

import re

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


#递归函数
def matrixGen(i, j, recursionStr, axis_value_list, axis_list):
    #当前层的变量名
    curVar=axis_list[i]
    if curVar == 'FINAL_RESULT':
        return
    #输出当前层的变量
    #print(curVar)
    #输出本次循环中的
    if curVar != 'CMAKE_VERSION':

        for j in range(len(axis_value_list[i])):
            # 每个var取值拼接得到的字符串
            #需要一个新的字符串来承接前面所有变量相同的值
            newRecursionStr = recursionStr
            #然后加上每次循环中，当前变量不同的值
            if i == 0:
                newRecursionStr += str(axis_value_list[i][j])
            else:
                newRecursionStr += '-' + str(axis_value_list[i][j])

            #最后形成的字符串，在这个循环中，也就是最后一个变量不同。
            matrixGen(i+1, j, newRecursionStr, axis_value_list, axis_list)

        return

    else:
        recursionStrList = recursionStr.split('-')
        for strItem in recursionStrList:
            print('|'+ str(strItem), end=' ')

        #遍历所有的CMAKE_VERSION中的item
        for cmakeItem in axis_value_list[i]:
            #首先存储之前每次递归（也就是在cmake之前）得到的字符串
            finalStr = recursionStr
            finalStr += '-' + str(cmakeItem)
            recordFile = './record.txt'
            with open(recordFile, 'r') as record:
                #读取文件中所有内容，然后进行匹配，找到对应的那一行
                recordInFile = record.readline()
                while recordInFile:
                    recordResult = re.search(finalStr, str(recordInFile))
                    #如果找到了匹配行,则打印相关信息
                    if recordResult:
                        compileResult = str(recordInFile).rstrip('\n').split('-')[-1]
                        print('|'+compileResult, end='\t')
                    recordInFile = record.readline()

                #找到匹配的行之后，最后一个元素就是编译的结果
                #compileResult = recordResultStr.split('-')[-1]
                #print('|'+compileResult, end=" ")
        #在这一行所有结果输出完毕之后，换行
        print()
        return


##写测试，这部分将模拟生成record文件,并且以utf-8的encoding
#recordFile = './record.txt'
#with open(recordFile, 'w') as record:
#    record.write('OS-CUDA_VERSION-MPI_VERSION-CMAKE_VERSION-FINAL_RESULT\n')
#    record.write('centos7-9.0-3.0-3.3-SuccessBuild\n')
#    record.write('centos7-9.0-3.0-3.5-SuccessBuild\n')
#    record.write('centos7-9.0-3.0-3.8-SuccessBuild\n')
#    record.write('centos7-9.0-3.2-3.3-SuccessBuild\n')
#    record.write('centos7-9.0-3.2-3.5-SuccessBuild\n')
#    record.write('centos7-9.0-3.2-3.8-SuccessBuild\n')
#    record.write('centos7-9.2-3.0-3.3-SuccessBuild\n')
#    record.write('centos7-9.2-3.0-3.5-SuccessBuild\n')
#    record.write('centos7-9.2-3.0-3.8-SuccessBuild\n')
#    record.write('centos7-9.2-3.2-3.3-SuccessBuild\n')
#    record.write('centos7-9.2-3.2-3.5-SuccessBuild\n')
#    record.write('centos7-9.2-3.2-3.8-SuccessBuild\n')
#    record.write('centos7-10.0-3.0-3.3-cmakeerror\n')
#    record.write('centos7-10.0-3.0-3.5-cmakeerror\n')
#    record.write('centos7-10.0-3.0-3.8-cmakeerror\n')
#    record.write('centos7-10.0-3.2-3.3-cmakeerror\n')
#    record.write('centos7-10.0-3.2-3.5-cmakeerror\n')
#    record.write('centos7-10.0-3.2-3.8-makeerror\n')
#    record.write('centos7-10.1-3.0-3.3-makeerror\n')
#    record.write('centos7-10.1-3.0-3.5-makeerror\n')
#    record.write('centos7-10.1-3.0-3.8-makeerror\n')
#    record.write('centos7-10.1-3.2-3.3-makeerror\n')
#    record.write('centos7-10.1-3.2-3.5-makeerror\n')
#    record.write('centos7-10.1-3.2-3.8-makeerror\n')

#这一段打开文件操作是读取record文件中的每一行，生成所需的列表。
recordFile = './record.txt'
with open(recordFile,'r') as record:
    #读取第一行，获取所有变量的名字
    axis_str = record.readline()
    axis_list = axis_str.split('-')
    #创建最终要使用的列表
    axis_value_list = list()
    #变量的数量
    varNum = len(axis_list) - 1

    tmpList = list()
    #首先向列表当中添加几个set
    for i in range(0, varNum):
        tmpList.append(set())


    #接下来读取每一行，使用split分解，开始统计每个变量的取值
    line = record.readline()
    #当line不为空的时候，也就是一直读文件直到读取完毕每一行
    while line:
        varSplit = str(line).split('-')
        for i in range(0, varNum):
            #将读入的每一行字符串分解后的值各自填入。由于使用的是set，所以碰到新的值的时候才会加入进去
            #如果分解的字符串是纯数字（含小数点），则转换为float类型的变量存储。
            if is_number(varSplit[i]):
                tmpFLoat = float(varSplit[i])
                tmpList[i].add(tmpFLoat)
            else:
                tmpList[i].add(varSplit[i])
        #读入下一行
        line = record.readline()

    #对所有的set内的值进行排序
    for i in range(0, varNum):
        # 将读入的每一行字符串分解后的值各自填入。由于使用的是set，所以碰到新的值的时候才会加入进去
        tmpList[i] = sorted(tmpList[i])

    axis_value_list = tmpList


#下面这一段是为了在phabricator上形成表格
headLineSpaceNum = len(axis_list) - 3

for i in range(headLineSpaceNum):
    print('|', end='\t')

print('|cmake', end='\t')

#axis_value_list当中最后一个元素是存储cmakeVersion的列表
for cmakeItem in axis_value_list[-1]:
    print('|' + str(cmakeItem), end='\t')

print()

for item in axis_list[0:-2]:
    print('|'+str(item), end="\t")
for cmakeItem in axis_value_list[-1]:
    print('|', end='\t')
print()

#到这里形成了完整的表格头

#下面开始生成表格中各个变量搭配的编译结果
matrixGen(0, 0, '', axis_value_list, axis_list)

#到这里整张表格完成

