import SOAPpy
import codecs
import sys


def writeOutput(resultFileName,finalOut):
    file_out = codecs.open(resultFileName, 'w', 'utf-8')
    for i in range(len(finalOut)):
        for j in range(len(finalOut[i]) - 1):
            file_out.write(finalOut[i][j] + '\t')
        file_out.write(finalOut[i][j+1] + '\n')
        # file_out.write('\n')

    file_out.flush()
    file_out.close()
    return


def readInputTokensFile(in_path):
    f = codecs.open(in_path,'r','utf-8')
    contents = f.readlines()
    for i in range(len(contents)):
        contents[i] = contents[i].strip('\n')
        contents[i] = contents[i].strip('\r')

    return contents

try:
    programName = sys.argv[0]
    args = sys.argv[0:]
    countArgs = len(args)
    if countArgs < 4 :
        # print('Help: programName   InputFilePath   ResultFilePath   TokensFilePath')
        print('Help Usage 1: programName   InputFilePath   ResultFilePath  tokenFilePath  1')
        print('\n')
        print('Help Usage 2: programName   InputFilePath   ResultFilePath  2')
        print ('\n')
    else:
        server = SOAPpy.SOAPProxy('http://185.130.78.112/coref')
        if sys.argv[3]=='2':
            tkns = readInputTokensFile(sys.argv[1])
            output = server.DoCoref(tkns, sys.argv[3])
            output = output.data

            writeOutput(sys.argv[2], output)

        elif sys.argv[4]=='1':
            f = codecs.open(sys.argv[1],'r','utf-8')
            text = f.read()
            res = server.DoCoref(text, sys.argv[4])
            res = res.data
            chain = res[0][0]
            tokens = res[0][1]
            file = codecs.open(sys.argv[2],'w','utf-8')
            for i in range(len(chain)):
                file.write(chain[i])
            file.flush()
            file.close()
            file = codecs.open(sys.argv[3],'w','utf-8')
            for i in range(len(tokens)):
                file.write(tokens[i])
                file.write('\n')
            file.flush()
            file.close()

            # writeOutput(sys.argv[2], output)

        print('\n .... Coref successfully Done ....')
except:
    print('........ Exception Occured .........')

