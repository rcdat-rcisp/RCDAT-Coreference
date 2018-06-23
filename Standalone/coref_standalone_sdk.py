# coding=utf-8
__author__ = 'Shadi & HO'
### import
import Chunker_dadegan_HO
# import timeit
import codecs
import sys
import subprocess
import uuid


# import web
from zeep import Client
# import soaplib
# from soaplib.serializers.primitive import String, Array
# from soaplib.service import soapmethod
# from soaplib.wsgi_soap import SimpleWSGISoapApp




# from soaplib import soap
# from soaplib.serializers.primitive import String, Any, AnyAsDict
# from soaplib.service import rpc, DefinitionBase
# from soaplib.wsgi import Application
import configparser


# firstOffirst=timeit.default_timer()
folderNum = '1'
# SVMmodel = 'model-newDict_NER_withword_3-7'
# SVMmodel = 'model-withWords'
# SVMmodel = 'model_90-100'
SVMmodel = 'model-shab'
SVMPlace = 'svm_light_windows64'
Dict = 'Fina_shadi_dict.txt'
folder_out = 'outDir'

DependencyParserWSAddr = ''
TaggerWSAddr = ''
NerWSAddr = ''
PreprocessWSAddr = ''


def loadDict():

    open_File = codecs.open(Dict, 'r', 'utf-8')
    dic = open_File.readlines()

    for i in range(len(dic)):
        dic[i] = dic[i].strip('\r\n')
        dic[i] = dic[i].replace(u'ي', u'ی')

    return dic

DictionaryData = loadDict()

def readConfigFile():
    config = configparser.ConfigParser()
    config.read('coref.ini')
    global DependencyParserWSAddr
    DependencyParserWSAddr = config.get('WSSection','DependencyParser')
    global TaggerWSAddr
    TaggerWSAddr = config.get('WSSection','Tagger')
    global NerWSAddr
    NerWSAddr = config.get('WSSection','Ner')
    global PreprocessWSAddr
    PreprocessWSAddr = config.get('WSSection','Preprocess')

    return



def readInputFile(path):
    # file_in = codecs.open('test'+'\\'+'0-9.txt', 'r', 'utf-8')
    file_in = codecs.open(path, 'r', 'utf-8')
    txt = file_in.read()
    return txt

def normalizeText(File_ID, inputText):
    wsdl = 'http://185.130.78.112/preprocess/PreprocessWebService.asmx?WSDL'
    client = Client(wsdl=PreprocessWSAddr)
    correctedText = client.service.CorrectText(inputText, False)
    tokens = client.service.Tokenize(correctedText)

    wordsPerSnt = []
    sentences = client.service.SplitSentence(correctedText)
    for i in range(len(sentences)):
        words = []
        words = client.service.Tokenize(sentences[i])
        for j in range(len(words)):
            wordsPerSnt.append(words[j])
        wordsPerSnt.append('')


    file_out = codecs.open(folder_out + '\\' + 'TKN_' + File_ID, 'w', 'utf-8')
    for i in range(len(tokens)):
        file_out.write(tokens[i]+'\n')
    file_out.flush()
    file_out.close()
    return correctedText, tokens, wordsPerSnt

def preprocess(words,option):
    # file names
    test = 'test'
    file = '0-9.txt'
    pros = 'PRO'
    pathspl = 'SplChCked'
    POS16 = 'POS16'
    POS100 = 'POS100'
    POS16Chunk = 'POS16Chunk'
    POS100NER = 'POS100NER'
    Anim = 'animacy'
    out = 'CorpusMD\\p' + folderNum


    # read File

    def splChcK_and_tokeniz(fileName, pathin):
        # wsdl = 'http://10.10.32.37:5320/PreprocessWebService.asmx?WSDL'
        # client = Client(wsdl=wsdl)
        # # file_in = codecs.open(pathin + '\\' + fileName, 'r', 'utf-8')
        # # text = file_in.read()
        # correctedText = client.service.CorrectText(InText, False)
        # tokens = client.service.Tokenize(correctedText)
        #
        # file_out = codecs.open(folder_out+'\\'+'NRM_'+File_ID, 'w', 'utf-8')
        # file_out.write(correctedText)
        # file_out.flush()
        # file_out.close()
        # subprocess.call(['spellchecker-exe.exe', '-A', pathin + '\\' + fileName, pathOut + '\\' + fileName])
        # f_in = codecs.open(pathOut + '\\' + fileName, 'r', 'utf-8')
        # fin = f_in.read()
        # fin = fin.replace('\n', '')
        # fin = fin.split(' ')
        # # for i in range(len(fin)):
        # #     print(fin[i])
        # f_in.close()
        # f_out = codecs.open(pathOut + '\\' + fileName, 'w', 'utf-8')
        # for f in fin:
        #     f_out.write(f)
        #     f_out.write('\n')
        #     if f == '.' or f == '!' or f == '؟':
        #         f_out.write('\n')
        # for t in tokens:
        #     f_out.write(t)
        #     f_out.write('\n')
        #     if t == '.' or t == '!' or t == '؟':
        #         f_out.write('\n')
        return

    # def Anmacy_(file,pathin,pathout):

    def POS_16(file, inputPro, pathout):
        # finC = codecs.open(pathin + '\\' + file, 'r', 'utf-8')
        # f = finC.readlines()
        # foutC = codecs.open(pathout + '\\' + file, 'w', 'utf-8')
        output = []
        f = inputPro
        for i in range(len(f)):
            tag_splitted = f[i][1].split('-')
            tmp = []
            tmp.append(f[i][0])
            tmp.append(tag_splitted[0])
            # output.append(f[i][0] + '\t' + f[i][1][0] + '\t' + '' + '\n')
            output.append(tmp)

        # for i in range(len(f)):
        #     f[i] = f[i].strip('\r\n')
        #     f[i] = f[i].split('\t')
        #     if len(f[i]) == 1:
        #         foutC.write(f[i][0] + '\n')
        #     else:
        #         f[i][1] = f[i][1].split('-')
        #         foutC.write(f[i][0] + '\t' + f[i][1][0] + '\t' + '' + '\n')
        return output

    def POS_100(file, tokens, pathout):
        wsdl = 'http://185.130.78.112/pos/Tagger_WebService.asmx?WSDL'
        client = Client(wsdl=TaggerWSAddr)
        # file_in = codecs.open(pathin + '\\' + file, 'r', 'utf-8')
        # text = file_in.read()
        output = []
        tkns = []
        for i in range(len(tokens)):
            if tokens[i] != '':
                tkns.append(tokens[i])
            else:
                if len(tkns)==0:
                    break
                input_type = client.get_type('ns0:ArrayOfString')
                inputObj = input_type(tkns)
                # for i in range(len(tokens)):
                #     tkns['soapenc'].append(tokens[i])
                outTag = client.service.GetTagsAdvancedByArray(inputObj, modelname='model-100-new')
                for j in range(len(outTag)):
                    output.append(outTag[j])
                output.append('')
                tkns = []
        #subprocess.call(['TestTagger.exe', '-tag', pathin + '\\' + file, pathout + '\\' + file, 'model-100-new'])
        # finC = codecs.open(pathout + '\\' + file, 'r', 'utf-8')
        # f = finC.readlines()
        # foutC = codecs.open(pathout + '\\' + file, 'w', 'utf-8')
        # for i in range(len(f)):
        #     f[i] = f[i].strip('\r\n')
        #     f[i] = f[i].split('\t')
        #     if len(f[i]) == 1:
        #         foutC.write(f[i][0] + '\n')
        #     else:
        #         foutC.write(f[i][0] + '\t' + f[i][1] + '\t' + '' + '\n')


        # with codecs.open(pathout + '\\' + file, 'w', 'utf-8') as fout:
        #     for item in output:
        #         for i in range(0, len(item.tokens.string)):
        #             fout.write(u"{0}\t{1}\n".format(item.tokens.string[i], item.tags.string[i]))
        #         fout.write('\n')
        return output

    # def NER(file,pathin,pathout):
    #     subprocess.call(['TestTagger.exe','-tag',pathin+'\\'+file,pathout+'\\'+file,'model-100-new'])
    #     return
    def NER(filename, input, pathWrite):
        wsdl = 'http://185.130.78.112/ner/NER_WS.asmx?WSDL'
        client = Client(wsdl=NerWSAddr)
        # file_in = codecs.open(pathRead + '\\' + filename, 'r', 'utf-8')
        # text = file_in.read()
        tokens = []
        tags = []
        for i in range(len(input)):
            tokens.append(input[i][0])
            tags.append(input[i][1])

        ners = []
        tkns = []
        tgs = []
        for i in range(len(tokens)):
            if tokens[i] != '':
                tkns.append(tokens[i])
                tgs.append(tags[i])
            else:
                if len(tkns)==0:
                    break
                array_type = client.get_type('ns0:ArrayOfString')
                tokenObj = array_type(tkns)
                tagObj = array_type(tgs)
                ne = client.service.DoNERWithoutTagAndNormalization(tokenObj, tagObj, 'modelVersion6')
                for j in range(len(ne)):
                    ners.append(ne[j])
                ners.append('')
                tgs = []
                tkns = []
        # subprocess.call(['ChunkerAndNER\\crf_test.exe', 'ChunkerAndNER\\modelVersion6', pathRead + '\\' + filename,
        #                  pathWrite + '\\' + filename])

        # with codecs.open(pathWrite + '\\' + filename, 'w', 'utf-8') as fout:
        #     for item in output:
        #         for i in range(0, len(item.words.string)):
        #             fout.write("{0}\t{1}\t\t{2}\n".format(item.words.string[i].encode('utf-8'), item.tags.string[i].encode('utf-8'), item.ners.string[i].encode('utf-8')))
        return ners

    def NPchunk(filename, inputPos16, pathWrite):
        wsdl = 'http://localhost:1403/NER_WS.asmx?WSDL'
        client = Client(wsdl=NerWSAddr)
        # file_in = codecs.open(pathRead + '\\' + filename, 'r', 'utf-8')
        # text = file_in.read()
        tokens = []
        tags = []
        for i in range(len(inputPos16)):
            tokens.append(inputPos16[i][0])
            tags.append(inputPos16[i][1])

        output = []
        tkns = []
        tgs = []
        for i in range(len(tokens)):
            if tokens[i] != '':
                tkns.append(tokens[i])
                tgs.append(tags[i])
            else:
                array_type = client.get_type('ns0:ArrayOfString')
                tokenObj = array_type(tkns)
                tagObj = array_type(tgs)
                ne = client.service.DoNERWithoutTagAndNormalization(tokenObj, tagObj, 'modelPhase2')
                for j in range(len(ne)):
                    output.append(ne[j])
                output.append('')
                tkns = []
                tgs = []
        # subprocess.call(['ChunkerAndNER\\crf_test.exe', 'ChunkerAndNER\\modelPhase2', pathRead + '\\' + filename,
        #                  pathWrite + '\\' + filename])

        # with codecs.open(pathWrite + '\\' + filename, 'w', 'utf-8') as fout:
        #     for item in output:
        #         for i in range(0, len(item.words.string)):
        #             fout.write("{0}\t{1}\t\t{2}\n".format(item.words.string[i].encode('utf-8'), item.tags.string[i].encode('utf-8'), item.ners.string[i].encode('utf-8')))

        return output


    def copy_by_value(one):
        x = []
        for i in range(len(one)):
            x.append([])
            for j in range(len(one[i])):
                tmp = one[i][j]
                x[i].append(tmp)
        return x

    def Animacy(file, input, pathout):  #####az khorooji pro va mikone!
        # finC = codecs.open(pathin + '\\' + file, 'r', 'utf-8')
        # f1 = finC.readlines()
        # for i in range(len(f1)):
        #     f1[i] = f1[i].strip('\r\n')
        #     f1[i] = f1[i].split('\t')
        # finC.close()
        # fin1C = codecs.open('tmp\\' + file, 'w', 'utf-8')
        # for i in range(len(f1)):
        #     fin1C.write(f1[i][0] + '\n')
        # fin1C.close()
        # subprocess.call(['TestTagger.exe', '-tag', 'tmp\\' + file, pathout + '\\' + file, 'Dadegan_POS_Model.model'])

        wsdl = 'http://185.130.78.112/pos/Tagger_WebService.asmx?WSDL'
        client = Client(wsdl=TaggerWSAddr)
        tokens = []
        for i in range(len(input)):
            tokens.append(input[i][0])

        output = []
        tkns = []
        for i in range(len(tokens)):
            if tokens[i] != '':
                tkns.append(tokens[i])
            else:
                array_type = client.get_type('ns0:ArrayOfString')
                tokensObj = array_type(tkns)
                outTag = client.service.GetTagsAdvancedByArray(tokensObj, modelname='DadeganPOS')
                for k in range(len(outTag)):
                    output.append(outTag[k])
                output.append('')
                tkns = []

        # finC = codecs.open(pathout + '\\' + file, 'r', 'utf-8')
        #
        # f = finC.readlines()
        f = []
        for i in range(len(output)):
            f.append(output[i])
        # foutC = codecs.open(pathout + '\\' + file, 'w', 'utf-8')


        # for i in range(len(f)):
        #     f[i] = f[i].strip('\r\n')
        #     f[i] = f[i].split('\t')
        for i in range(len(f)):
            if len(f) > 0:
                if f[i].find('-IANM') != -1:
                    f[i] = 'NO'
                elif f[i].find('-ANM') != -1:
                    f[i] = 'YES'
                else:
                    f[i] = '-'
        # print(len(f),len(f1),'sd[rfsdldsf')
        for i in range(len(f)):
            if len(input[i]) > 1:
                if input[i][1] == 'PRO' and f[i] != 'NO':
                    f[i] = 'YES'
        # for i in range(len(f)):
        #     if len(f[i]) > 1:
        #         foutC.write(f[i][0] + '\t' + f[i][1] + '\n')
        #     else:
        #         foutC.write('\n')
        outAnimacy = []
        for i in range(len(f)):
            if len(f) > 0:
                tmp = []
                tmp.append(tokens[i])
                tmp.append(f[i])
                outAnimacy.append(tmp)
        return outAnimacy

    def PRO_finder(tags, tokens, pathout):
        # pro = []
        proList_4 = [u'یمان', u'یتان', u'یشان', u'امان', u'اتان', u'اشان', u'يمان', u'يتان', u'يشان']
        proList_3 = [u'مان', u'تان', u'شان']
        proList_2 = [u'یم', u'یت', u'یش', u'ام', u'ات', u'اش', u'يم', u'يت', u'يش']
        proList_1 = [u'م', u'ت', u'ش']
        # finC = codecs.open(pathIN + '\\' + file, 'r', 'utf-8')
        # f = finC.readlines()
        # foutC = codecs.open(pathout + '\\' + file, 'w', 'utf-8')
        f = tags

        output = []
        # for i in range(len(f)):
        #     pro.append([])
        #     f[i] = f[i].strip('\r\n')
        #     f[i] = f[i].split('\t')
        for i in range(len(f)):
            if len(f) > 0:
                if f[i] == 'PRO':
                    tmp = []
                    tmp.append(tokens[i])
                    tmp.append('PRO')
                    output.append(tmp)
                elif f[i].find('NCLITIC') != -1:
                    flag = 0
                    for pro4 in proList_4:
                        if tokens[i].find(pro4, -4) != -1:
                            tmp = []
                            tmp.append(tokens[i][:-4])
                            tmp.append(f[i])
                            output.append(tmp)
                            tmp = []
                            tmp.append(pro4)
                            tmp.append('PRO')
                            output.append(tmp)
                            flag = 1
                    if flag == 0:
                        for pro3 in proList_3:
                            if tokens[i].find(pro3, -3) != -1:
                                tmp = []
                                tmp.append(tokens[i][:-3])
                                tmp.append(f[i])
                                output.append(tmp)
                                tmp = []
                                tmp.append(pro3)
                                tmp.append('PRO')
                                output.append(tmp)
                                flag = 1
                        if flag == 0:
                            for pro2 in proList_2:
                                if tokens[i].find(pro2, -2) != -1:
                                    tmp = []
                                    tmp.append(tokens[i][:-2])
                                    tmp.append(f[i])
                                    output.append(tmp)
                                    tmp = []
                                    tmp.append(pro2)
                                    tmp.append('PRO')
                                    output.append(tmp)
                                    flag = 1
                            if flag == 0:
                                for pro1 in proList_1:
                                    if tokens[i].find(pro1, -1) != -1:
                                        tmp = []
                                        tmp.append(tokens[i][:-1])
                                        tmp.append(f[i])
                                        output.append(tmp)
                                        tmp = []
                                        tmp.append(pro1)
                                        tmp.append('PRO')
                                        output.append(tmp)
                                        flag = 1
                else:
                    tmp = []
                    tmp.append(tokens[i])
                    tmp.append(f[i])
                    output.append(tmp)

        return output



        # for i in range(len(f)):
        #     if len(f.tags.string) > 1:
        #         if f[i][1] == 'PRO':
        #             pro[i].append(f[i][0])
        #             pro[i].append(pro)
        #             foutC.write(f[i][0] + '\t' + 'PRO' + '\t' + '\n')
        #         elif f[i][1].find('NCLITIC') != -1:
        #             flag = 0
        #             for proo in proList_4:
        #                 if f[i][0].find(proo, -4) != -1:
        #                     foutC.write(f[i][0][:-4] + '\t' + f[i][1] + '\t' + '\n')
        #                     foutC.write(proo + '\t' + 'PRO' + '\t' + '\n')
        #                     flag = 1
        #             if flag == 0:
        #                 for poro in proList_3:
        #                     if f[i][0].find(poro, -3) != -1:
        #                         foutC.write(f[i][0][:-3] + '\t' + f[i][1] + '\t' + '\n')
        #                         foutC.write(poro + '\t' + 'PRO' + '\t' + '\n')
        #                         flag = 1
        #                 if flag == 0:
        #                     for poro in proList_2:
        #                         if f[i][0].find(poro, -2) != -1:
        #                             foutC.write(f[i][0][:-2] + '\t' + f[i][1] + '\t' + '\n')
        #                             foutC.write(poro + '\t' + 'PRO' + '\t' + '\n')
        #                             flag = 1
        #                     if flag == 0:
        #                         for poro in proList_1:
        #                             if f[i][0].find(poro, -1) != -1:
        #                                 foutC.write(f[i][0][:-1] + '\t' + f[i][1] + '\t' + '\n')
        #                                 foutC.write(poro + '\t' + 'PRO' + '\t' + '\n')
        #
        #         else:
        #             foutC.write(f[i][0] + '\t' + f[i][1] + '\t' + '\n')
        #     else:
        #         foutC.write('\n')
        #
        # return

    def make_corpus_HO():
        corpus = []
        sentenceNumber = 1
        for i in range(len(outPros)):
            if len(outPros[i][0]) > 0:
                tmp = []
                word = outPros[i][0]
                tmp.append(word)
                tmp.append(outpos16[i][1])
                tmp.append(outNER[i])
                tmp.append(word)
                tmp.append(word)
                tmp.append('-')
                tmp.append('-')
                tmp.append('-')
                tmp.append('-')

                if option=='1':
                    tmp.append(outAnim[i][1])
                elif option=='2':
                    tmp.append('-')
                tmp.append(outNPChunk[i])
                tmp.append(outPros[i][1])
                # ============  Adding Sentence Number =============== #
                tmp.append(sentenceNumber)
                if word == u'.' or word == u'!' or word == u'؟':
                    sentenceNumber += 1
                # ===================================================== #
                corpus.append(tmp)
        return corpus





    def make_corpus(file, NER, chunker, animacy):
        x = codecs.open(chunker + '\\' + file, 'r', 'utf-8')
        pos16Ochunk = x.readlines()
        for i in range(len(pos16Ochunk)):
            pos16Ochunk[i] = pos16Ochunk[i].strip('\r\n')
            pos16Ochunk[i] = pos16Ochunk[i].split('\t')

        anm = codecs.open(animacy + '\\' + file, 'r', 'utf-8')
        anim = anm.readlines()
        for i in range(len(anim)):
            anim[i] = anim[i].strip('\r\n')
            anim[i] = anim[i].split('\t')

        y = codecs.open(NER + '\\' + file, 'r', 'utf-8')
        pos100Oner = y.readlines()
        for i in range(len(pos100Oner)):
            pos100Oner[i] = pos100Oner[i].strip('\r\n')
            pos100Oner[i] = pos100Oner[i].split('\t')


        corpus = codecs.open('TheCorpus', 'w', 'utf-8')
        for i in range(len(pos100Oner)):
            if len(pos100Oner[i]) > 1:
                # print(pos100Oner[i][0])
                # print(pos16Ochunk[i][1],i)
                # print(i)
                corpus.write(
                    pos100Oner[i][0] + '\t' + pos16Ochunk[i][1] + '\t' + pos100Oner[i][2] + '\t' + pos100Oner[i][
                        0] + '\t' + pos100Oner[i][0] + '\t' + '-' + '\t' + '-' + '\t' + '-' + '\t' + '-' + '\t' +
                    anim[i][1] + '\t' + pos16Ochunk[i][2] + '\t' + pos100Oner[i][1] + '\n')
                if pos100Oner[i][0] == u'.' or pos100Oner[i][0] == u'!' or pos100Oner[i][0] == u'؟':
                    corpus.write('\n')
        corpus.close()
        z = codecs.open("TheCorpus", 'r', 'utf-8')
        cor = z.readlines()
        for i in range(len(cor)):
            cor[i] = cor[i].strip('\r\n')
            cor[i] = cor[i].split('\t')
        return cor

    def addSentencrNumber(content):

        k = 0
        i = 0
        while i < len(content):
            k += 1
            while (content[i][0] != '' and content[i][0] != '\n' and i < (len(content) - 1)):
                content[i].append(k)
                i += 1
                if i == len(content):
                    break
            i += 1
        return content


    def makeFiles(finalPath, file, POS100NER, POS16Chunk):
        out_pos100NER = codecs.open(POS100NER + '\\' + file, 'w', 'utf-8')
        for i in range(len(outPros)):
            out_pos100NER.write(outPros[i][0] + '\t' + outPros[i][1] + '\t' + outNER[i] + '\n')
        out_pos100NER.flush()
        out_pos100NER.close()

        out_Pos16Chunk = codecs.open(POS16Chunk + '\\' + file, 'w', 'utf-8')
        for i in range(len(outpos16)):
            out_Pos16Chunk.write(outpos16[i][0] + '\t' + outpos16[i][1] + '\t' + outNPChunk[i] + '\n')
        out_Pos16Chunk.flush()
        out_Pos16Chunk.close()

        out_fileAnim = codecs.open(Anim + '\\' + file, 'w', 'utf-8')
        for i in range(len(outAnim)):
            out_fileAnim.write(outAnim[i][0] + '\t' + outAnim[i][1] + '\n')
        out_fileAnim.flush()
        out_fileAnim.close()
        return

    def finalize_HO(corp):
        output = []
        for i in range(len(corp)):
            if len(corp[i]) > 1:
                tmp = []
                tmp.append(file)
                tmp.append(str(corp[i][-1]))
                for j in range(0, len(corp[i])-1):
                    tmp.append(corp[i][j])
                output.append(tmp)
            else:
                tmp = []
                tmp.append('')
                output.append(tmp)
        tmp = []
        tmp.append(file)
        tmp.append(str(corp[-4][-1]))
        tmp.append('.')
        tmp.append('PUNC')
        tmp.append('O')
        tmp.append('.')
        tmp.append('.')
        tmp.append('-')
        tmp.append('-')
        tmp.append('-')
        tmp.append('-')
        tmp.append('-')
        tmp.append('O')
        tmp.append('DELM')
        output.append(tmp)



        return output


    def finalize(finalPath, file, POS100NER, POS16Chunk):
        content = make_corpus(file, POS100NER, POS16Chunk, Anim)
        cont = addSentencrNumber(content)
        out = codecs.open(finalPath + '\\' + file, 'w', 'utf-8')
        fileOut = finalPath + '\\' + file
        for i in range(len(cont)):
            if len(cont[i]) > 1:
                out.write(file + '\t')
                out.write(str(cont[i][-1]) + '\t')
                for j in range(0, len(cont[i]) - 2):
                    out.write(cont[i][j] + '\t')
                out.write(cont[i][-2] + '\n')
        out.write(file + '\t' + str(
            cont[-4][-1]) + '\t' + '.	PUNC	O	.	.	-	-	-	-	-	O	DELM' + '\n')
        return fileOut

    # start=timeit.default_timer()
    # fname = test + '\\' + '0-9.txt'
    # words = splChcK_and_tokeniz('0-9.txt', test)
    # nrmTxt = normalizeText('0-9.txt', test)
    # words = splChcK_and_tokeniz()

    Tags = POS_100(file, words, POS100)
    ########################################################### pro and shadi chunk
    outPros = PRO_finder(Tags, words, pros)  ### kolan jaye pos100 bayad az pro estefade beshe
    outAnim = Animacy(file, outPros, Anim)
    outNER = NER(file, outPros, POS100NER)
    # outpot16 = POS_16(file, pros, POS16)  #### saxte POS16 az roo pro
    outpos16 = POS_16(file, outPros, POS16)
    # NPchunk(file, POS16, POS16Chunk)
    outNPChunk = NPchunk(file, outpos16, POS16Chunk)
    # makeFiles(out, file, POS100NER, POS16Chunk)
    # finalFile = finalize(out, file, POS100NER, POS16Chunk)
    finalFile = finalize_HO(make_corpus_HO())
    ############################################################
    # ######shabnam chunk
    # NER(file,POS100,POS100NER)
    # shabnamChunk(file,POS16,POS16Chunk)
    # finalFile=finalize(out,file,pros,POS16Chunk)

    # end=timeit.default_timer()

    # print('preprocess:', end-start)
    return finalFile


def makeFeatureFile(inputCrpus, normalizedText):
    ####-------------------------places------------------

    # folderNum = '1'
    # inputCorpus = 'CorpusMD\\p' + folderNum
    outPutFiles = 'featureFiles_2'
    main_dict = 'Dictionary_Ver_Final.txt'

    # ______________kharabkari_____________________________
    def kharbKari(inputCorpus, file):
        o = openFile_and_read(inputCorpus, file)
        out = codecs.open(inputCorpus + '\\' + file, 'w', 'utf-8')
        for i in range(len(o)):
            if o[i][1] == '' or o[i][1] == '-' or o[i][1] == '*)':
                o[i][1] = o[i - 1][1]
            for j in range(len(o[i]) - 1):
                out.write(o[i][j] + '\t')
            out.write(o[i][-1])
            out.write('\n')
        # out.write(o[-2][0]+'\t'+o[-2][1]+'\t'+'.	PUNC	O	.	.	-	-	-	-	-	O	DELM'+'\n')
        out.close()

        return

    # ________________readAndWrite_________________________
    def openFile_and_read(inputCorpus, file):
        open_File = codecs.open(inputCorpus + '\\' + file, 'r', 'utf-8')
        one_File = open_File.readlines()
        for i in range(len(one_File)):
            one_File[i] = one_File[i].strip('\r\n')
            one_File[i] = one_File[i].split('\t')

        return one_File

    #

    def Write_results_on_List_HO(input, output):
        tmp = []
        tmp.append(input[0])
        tmp.append(input[1])
        for i in range(2, len(input) - 1):
            tmp.append(str(input[i]))
        tmp.append(input[-1])
        output.append(tmp)
        return


    def Write_results_on_file(x, ooniKeBayadNevesht):
        x.write('"' + ooniKeBayadNevesht[0] + '"' + ';' + '"' + ooniKeBayadNevesht[1] + '"' + ';')
        for i in range(2, len(ooniKeBayadNevesht) - 1):
            x.write(str(ooniKeBayadNevesht[i]) + ';')
        x.write("'" + ooniKeBayadNevesht[-1] + "'")
        x.write('\n')

        return


    def Write_svm_results_on_List_HO(input, output):
        tmp = []
        input[-1].strip('\r\n')
        if input[-1] == 'N':
            tmp.append('-1 ')
        if input[-1] == 'P':
            tmp.append('1 ')
        if input[2] >= 2:
            tmp.append('2:1 ')
        else:
            tmp.append('2:2 ')
        for i in range(3, len(input) - 3):
            if input[i] == 1:
                tmp.append(str(i + 100) + ':2 ')
            else:
                tmp.append(str(i + 100) + ':1 ')
        output.append(tmp)
        return


    def Write_svm_results_on_file(x, ooniKeBayadNevesht):

        ooniKeBayadNevesht[-1].strip('\r\n')
        if ooniKeBayadNevesht[-1] == 'N':
            x.write('-1 ')
        if ooniKeBayadNevesht[-1] == 'P':
            x.write('1 ')
        if ooniKeBayadNevesht[2] >= 2:
            x.write('2:1 ')
        else:
            x.write('2:2 ')
        for i in range(3, len(ooniKeBayadNevesht) - 3):
            if ooniKeBayadNevesht[i] == 1:
                x.write(str(i + 100) + ':2 ')
            else:
                x.write(str(i + 100) + ':1 ')
        x.write('\n')
        return


    def Write_svm_results_on_List_2_HO(input, output):
        input[-1].strip('\r\n')
        input[0] = input[0].split(' ')
        input[1] = input[1].split(' ')
        for i in range(len(input[0])):
            input[0][i] = int(float(input[0][i]))
        for i in range(len(input[1])):
            input[1][i] = int(float(input[1][i]))

        input[0].sort()
        input[1].sort()
        tmp = []
        tmp.append('0 ')
        if int(input[2]) >= 2:
            tmp.append('2:1 ')
        else:
            tmp.append('2:2 ')
        for i in range(3, len(input) - 3):
            if input[i] == '1':
                tmp.append(str(i + 100) + ':2 ')
            else:
                tmp.append(str(i + 100) + ':1 ')

        z = input[0] + input[1]
        word = list(set(z))
        word.sort()
        for i in range(len(word)):
            if word[i] > 0:
                tmp.append(str(word[i] + 200) + ':1 ')

        output.append(tmp)
        return

    def Write_svm_results_on_file_2(x, ooniKeBayadNevesht):
        # print('HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
        ooniKeBayadNevesht[-1].strip('\r\n')
        ooniKeBayadNevesht[0] = ooniKeBayadNevesht[0].split(' ')
        ooniKeBayadNevesht[1] = ooniKeBayadNevesht[1].split(' ')
        for i in range(len(ooniKeBayadNevesht[0])):
            ooniKeBayadNevesht[0][i] = int(float(ooniKeBayadNevesht[0][i]))
        for i in range(len(ooniKeBayadNevesht[1])):
            ooniKeBayadNevesht[1][i] = int(float(ooniKeBayadNevesht[1][i]))

        ooniKeBayadNevesht[0].sort()
        ooniKeBayadNevesht[1].sort()
        # if ooniKeBayadNevesht[-1]=="'N'":
        #     x.write('-1 ')
        # if ooniKeBayadNevesht[-1]=="'P'":
        #     x.write('1 ')
        x.write('0 ')
        if int(ooniKeBayadNevesht[2]) >= 2:
            x.write('2:1 ')
        else:
            x.write('2:2 ')
        for i in range(3, len(ooniKeBayadNevesht) - 3):
            if ooniKeBayadNevesht[i] == '1':
                x.write(str(i + 100) + ':2 ')
            else:
                x.write(str(i + 100) + ':1 ')
        # x.write('\n')
        z = ooniKeBayadNevesht[0] + ooniKeBayadNevesht[1]
        word = list(set(z))
        word.sort()
        for i in range(len(word)):
            if word[i] > 0:
                x.write(str(word[i] + 200) + ':1 ')
        x.write('\n')
        # print(' ******',z)
        # x.write('"'+str(ooniKeBayadNevesht[0])+'"'+';'+'"'+str(ooniKeBayadNevesht[1])+'"'+';')
        # for i in range(2,len(ooniKeBayadNevesht)-1):
        #         # print(ooniKeBayadNevesht[i],i)
        #         x.write(str(ooniKeBayadNevesht[i])+';')
        # x.write("'"+ooniKeBayadNevesht[-1]+"'")
        # x.write('\n')

        return

    # ___________________split Groups______________________
    def split_g(one):  ### NAER based
        grouped = []
        # q=[]
        www = []
        # print(one[0])
        for i in range(len(one)):
            grouped.append([])
        for i in range(len(one)):
            grouped[i].append(one[i])
        for i in range(len(one)):
            # print(i)
            if len(one[i]) > 1:
                if one[i][4].find('B-') != -1:
                    place = i
                    www.append(place)
                    grouped[place].append(one[i][2] + '*' + one[i][3])
                    # grouped[place].append(one[i][0])
                    # grouped[place].append(i)
                    # grouped[i].grouped(one[i][3].strip('B-'))
                    # grouped[i].grouped(one[i][0])
                    i += 1

                    if len(one[i]) > 1:
                        if 'B-' not in one[i][4] and one[i][4] != 'O':
                            while 'I-' in one[i][4]:
                                grouped[place].append(one[i][2] + '*' + one[i][3])
                                i += 1
        x = grouped.count([''])
        for i in range(x):
            grouped.remove([''])
        tmp = []
        m = 2  # line length
        # print(len(grouped[0]))
        for i in range(len(grouped)):
            if len(grouped[i]) > m:
                # print(len(grouped[i]),grouped[i])
                tmp = []
                for j in range(len(grouped[i]) - m):
                    # print('*',(12+j))
                    tmp.append(' ' + str(grouped[i][m + j]))
                    # print(tmp,'6666666666')
                    ####
                grouped[i][0][2] = grouped[i][0][2] + '*' + grouped[i][0][3]
            for k in range(len(tmp)):
                if len(grouped[i]) > m:
                    grouped[i][0][2] = grouped[i][0][2] + tmp[k]
            # print (grouped[i])
            if len(grouped[i]) > m:
                # print(i)
                # print(grouped[i],'999999999999')
                head, word = head_detector(grouped[i])
                grouped[i][0].append(head)
                grouped[i][0][2] = word

                # print (grouped[i])
        # print('8888888888888888888888')
        # print(grouped)
        return grouped

    # ___________________split Groups + chunks______________________
    def split_groups_withChunks_oldChunker(one):
        # print(len(one),'bare')
        # print(one)
        # print(one[0])
        # print(one[10])
        grouped = []
        www = []
        q = 0
        n = 12  # olace of Chunk
        g_type = []
        chunks_split = []
        for i in range(len(one)):
            # print(one[i])
            grouped.append([])
            g_type.append('O')
            chunks_split.append('')
        for i in range(len(one)):
            if len(one[i]) >= 1:
                # print(one[i])
                # print(one[i][0][12])
                chunks_split[i] = (one[i][0][n].split('-'))
                # print(chunks_split[i])
                if chunks_split[i][0] == 'O':
                    chunks_split[i].append('O')

        # print(one[0])
        for i in range(len(one)):

            # print(len(one[i]))
            if len(one[i][0]) >= 1:
                if chunks_split[i][0] == 'B':
                    place = i
                    # print(place)
                    www.append(place)
                    # q.append(place)
                    grouped[place].append(one[i][0])
                    grouped[place].append(i)
                    q += 1
                    # print(i)
                    if chunks_split[i][0] != 'O':
                        g_type[place] = chunks_split[i][1]

                    i += 1
                    # if chunks_split[i][0]!='B':

                    while (chunks_split[i][1] == g_type[place] and chunks_split[i][0] == 'I'):
                        # print('cccchi')
                        # print(one[i][0])
                        grouped[place].append(one[i][0][2] + '*' + one[i][0][3])
                        grouped[i] = ['']
                        i += 1
                        # print(one[i])

                elif chunks_split[i][0] == 'O':
                    place = i
                    # q.append(place)
                    grouped[place].append(one[i][0])
                    grouped[place].append(i)
                    q += 1
                    i += 1

        # for i in range(len(grouped)):
        #     print(grouped[i])

        x = grouped.count([''])
        for i in range(x):
            grouped.remove([''])
        tmp = []
        m = 2
        for i in range(len(grouped)):
            if len(grouped[i]) > m:  ### m  toole yek line dar yek file
                tmp = []
                for j in range(len(grouped[i]) - m):
                    # print('*',(12+j))
                    tmp.append(' ' + str(grouped[i][m + j]))
                    # print(i,grouped[i])
                grouped[i][0][2] = grouped[i][0][2] + '*' + grouped[i][0][3]
            for k in range(len(tmp)):
                if len(grouped[i]) > m:
                    grouped[i][0][2] = grouped[i][0][2] + tmp[k]
            # print (grouped[i])
            if len(grouped[i]) > m:
                # print(i)
                # print(grouped[4])
                head, word = head_detector(grouped[i])
                grouped[i][0].append(head)
                grouped[i][0][2] = word

        # print(grouped,'shad')
        return grouped

    #### __ headDetect
    def head_detector(oneF):
        one = oneF[2]
        # print(oneF,'-----------')
        # print(one[0])
        www = []
        one = one.split(' ')
        # print(one)
        for j in range(len(one)):
            one[j] = one[j].split('*')

        # print(one)
        word = ''
        head = ''
        # print(one,'---------',len(one))
        for i in range(len(one)):
            word = word + ' ' + one[i][0]
            # print(word)
        for i in range(len(one)):
            if len(one[i]) > 1:
                if one[i][1] == 'N' or one[i][1] == 'N-SING-COM' or one[i][1] == 'N-SING-PR' or one[i][1] == 'N-PL-PR' or \
                                one[i][1] == 'N-PL-COM':
                    head = one[i][0]
                    break
                else:
                    head = one[0][0]
        # print(head)
        word = word.strip(' ')
        # print(word)
        return head, word



    def demonstrative_chunks(one):
        demon_chunks=[]
        #oneThis=list(one)

        oneThis=copy_by_value(one)
        demon_List=[u'این',u'آن',u'همین',u'همان',u'چنین',u'چنان',u'همچنین',u'همچنان']

        #demon_List=['این','آن','همین','همان','چنین','چنان','همچنین','همچنان']
        for i in range(len(one)):
            if len(one[i]) > 4:
                if one[i][2] in demon_List and one[i+1][3]=='N':
                    oneThis[i][2]=one[i][2]+' '+one[i+1][2]
                    oneThis[i].append(i)
                    demon_chunks.append(oneThis[i])
        head=''
        for i in range(len(demon_chunks)):
            tmp=demon_chunks[i][2].split(' ')
            head=tmp[1]
            demon_chunks[i].append(head)

        return demon_chunks

    def Dadegan_chunker(one):

        # Path_in = "Example"
        # fileNames = os.listdir(Path_in)
        # for file_e in range(len(fileNames)):
        #     fiii = fileNames[file_e]
        #     print(fiii)
        #     Boundary_Sentences = 'Chunks_' + fiii
        #     # Chunker_dadegan_i.SRL(fiii,Path_in+'\\'+fiii,Boundary_Sentences) #### before sunday changes
        #     Chunker_dadegan_HO.SRL(fiii, Path_in + '\\' + fiii, Boundary_Sentences)

        # chunk = codecs.open("SHADI_Chunks\\Chunks\\chunk_shabnam.txt", 'r', 'utf-8')
        # sc = chunk.readlines()
        sc = Chunker_dadegan_HO.SRL(normalizedText=normalizedText, preprocessWSDL=PreprocessWSAddr, taggerWSDL=TaggerWSAddr, depWSDL=DependencyParserWSAddr)

        for i in range(len(sc)):
            sc[i] = sc[i].strip('\r\n')
            sc[i] = sc[i].split('\t')

        # Out = codecs.open("SHADI_Chunks\\Chunks\\out_chunks.txt", 'w', 'utf-8')
        Out = []
        for i in range(len(sc)):
            if len(sc[i])>2:
                a = sc[i][0].split(' ')
                Out.append(str(len(a) - 1) + '\t' + sc[i][2] + '\n')
        # Out.close()

        oneThis = []
        two = copy_by_value(one)
        ttwo = copy_by_value(one)
        # inn = codecs.open('SHADI_Chunks\\Chunks\\out_chunks.txt', 'r', 'utf-8')
        # sc = inn.readlines()
        sc = Out
        for i in range(len(sc)):
            sc[i] = sc[i].strip('\r\n')
            sc[i] = sc[i].split('\t')
            # chunks.append(oneThis[int(sc[1])])
            tmp = ''
            for j in range(int(sc[i][1]), int(sc[i][1]) + int(sc[i][0])):
                if len(two[j]) > 4:
                    tmp = tmp + ' ' + two[j][2] + '*' + two[j][3]
            oneThis.append(ttwo[int(sc[i][1])])
            oneThis[i].append(int(sc[i][1]))
            oneThis[i][2] = tmp
        for i in range(len(oneThis)):
            head, word = head_detector(oneThis[i])
            oneThis[i][2] = word
            oneThis[i].append(head)

        return oneThis

    def copy_by_value(one):
        x = []
        for i in range(len(one)):
            x.append([])
            for j in range(len(one[i])):
                tmp = one[i][j]
                x[i].append(tmp)
        return x


    # ______________________combine 2 splits _________________
    # ________________ Mention Detection ------------------
    def Is_NER(one, n):  # n=4 ne , n=12 chunk
        chosen = []
        grouped = []
        # print(one[12])
        q = 0
        # n=4 # place of NER
        g_type = []
        chunks_split = []
        for i in range(len(one)):
            # print(one[i])
            grouped.append([])
            g_type.append('O')
            chunks_split.append('')
        for i in range(len(one)):
            if len(one[i]) >= 1:
                # print(one[i])
                # print(one[i][0][12])
                chunks_split[i] = (one[i][n].split('-'))
                # print(chunks_split[i])
                if chunks_split[i][0] == 'O':
                    chunks_split[i].append('O')

        # print(one[0])
        for i in range(len(one)):

            # print(len(one[i]))
            if len(one[i]) >= 1:
                if chunks_split[i][0] == 'B':
                    place = i
                    # print(place)
                    chosen.append(place)
                    grouped[place].append(one[i])
                    grouped[place].append(i)
                    q += 1
                    # print(i)
                    if chunks_split[i][0] != 'O':
                        g_type[place] = chunks_split[i][1]

                    i += 1
                    # if chunks_split[i][0]!='B':

                    while (chunks_split[i][1] == g_type[place] and chunks_split[i][0] == 'I'):
                        # print('cccchi')
                        grouped[place].append(one[i][2])
                        grouped[i] = ['']
                        i += 1
                        # print(one[i])

                elif chunks_split[i][0] == 'O':
                    place = i
                    # q.append(place)
                    grouped[place].append(one[i])
                    grouped[place].append(i)
                    q += 1

        x = grouped.count([''])
        for i in range(x):
            grouped.remove([''])
        tmp = []
        m = 2

        # print(len(grouped[1]))
        for i in range(len(grouped)):
            if len(grouped[i]) > m:  ### m  toole yek line dar yek file
                tmp = []

                for j in range(len(grouped[i]) - m):
                    # print('*',(12+j))
                    tmp.append(' ' + str(grouped[i][m + j]))
            for k in range(len(tmp)):
                if len(grouped[i]) > m:
                    grouped[i][0][2] = grouped[i][0][2] + tmp[k]
            # print(grouped[i])
        #
        print('----------------------------')
        return grouped, chosen

    # ______________________________________
    def pro_extract(one):
        pros = []
        Not_Pro_List = [u'این', u'آن', u'همین', u'همان', u'چنین', u'چنان']
        for i in range(len(one)):
            if one[i][-1] == 'PRO' and one[i][2] not in Not_Pro_List:
                one[i][10] = 'PRO'
                q = list(one[i])

                q.append(i)
                pros.append(q)
        for i in range(len(pros)):
            pros[i].append(pros[i][2])
        return pros

    def n_gram_extractor(one):
        chunks = []
        chunkPlace = []

        def one_gram(sentence):
            for i in range(sentence):
                if one[i][3] == 'N' or one[i][3] == 'PRO':
                    templist = list(one[i])
                    chunks.append(templist)
                    chunkPlace.append(i)
            return

        def two_gram(sentence):
            j = 0
            for i in range((sentence - 1)):

                j = i + 1
                if one[i][1] == one[j][1]:
                    if one[i][3] != 'PRO' and one[i][3] != 'AJ' and one[j][3] != 'P' and one[j][3] != 'RA' and one[i][
                        3] != 'RA' and one[j][3] != 'CON' and one[i][3] != 'CON' and one[i][3] != 'V' and one[i][
                        2] != '.' and one[i][2] != ':' and one[j][3] != 'V' and one[j][2] != '.' and one[j][2] != ':':
                        tmp = one[i][2]
                        one[i][2] = one[i][2] + ' ' + one[j][2]
                        templist = list(one[i])
                        chunks.append(templist)
                        chunkPlace.append(i)
                        one[i][2] = tmp
            return

        def three_gram(sentence):
            k = 0
            j = 0

            # while k<sentence:
            for i in range((sentence - 2)):
                j = i + 1
                k = j + 1
                if one[i][1] == one[j][1] and one[j][1] == one[k][1]:
                    if one[i][3] != 'PRO' and one[i][3] != 'AJ' and one[k][3] != 'P' and one[j][3] != 'P' and one[j][
                        3] != 'RA' and one[i][3] != 'RA' and one[k][3] != 'RA' and one[k][3] != 'CON' and one[i][
                        3] != 'CON' and one[i][3] != 'V' and one[i][3] != '.' and one[i][2] != ':' and one[j][
                        3] != 'V' and one[j][2] != '.' and one[j][2] != ':' and one[k][3] != 'V' and one[k][
                        2] != '.' and one[k][2] != ':':
                        tmp = one[i][2]
                        one[i][2] = one[i][2] + ' ' + one[j][2] + ' ' + one[k][2]
                        templist = list(one[i])
                        chunks.append(templist)
                        chunkPlace.append(i)
                        one[i][2] = tmp
            return

        def four_gram(sentence):
            l = 0
            k = 0
            j = 0

            for i in range((sentence - 3)):
                j = i + 1
                k = j + 1
                l = k + 1
                if one[i][1] == one[j][1] and one[j][1] == one[k][1] and one[l][1] == one[k][1]:
                    if one[i][3] != 'PRO' and one[i][3] != 'AJ' and one[k][3] != 'P' and one[j][3] != 'P' and one[l][
                        3] != 'P' and one[j][3] != 'RA' and one[i][3] != 'RA' and one[k][3] != 'RA' and one[l][
                        3] != 'RA' and one[l][3] != 'CON' and one[i][3] != 'CON' and one[i][3] != 'V' and one[i][
                        2] != '.' and one[i][2] != ':' and one[j][3] != 'V' and one[j][2] != '.' and one[j][
                        2] != ':' and one[k][3] != 'V' and one[k][2] != '.' and one[k][2] != ':' and one[l][
                        3] != 'V' and one[l][2] != '.' and one[l][2] != ':':
                        tmp = one[i][2]
                        one[i][2] = one[i][2] + ' ' + one[j][2] + ' ' + one[k][2] + ' ' + one[l][2]
                        templist = list(one[i])
                        chunkPlace.append(i)
                        chunks.append(templist)
                        one[i][2] = tmp
            return

        def five_gram(sentence):
            l = 0
            m = 0
            k = 0
            j = 0
            for i in range((sentence - 4)):
                j = i + 1
                k = j + 1
                l = k + 1
                m = l + 1
                if one[i][1] == one[j][1] and one[j][1] == one[k][1] and one[l][1] == one[k][1] and one[l][1] == one[m][
                    1]:
                    if one[i][3] != 'V' and one[i][2] != '.' and one[i][2] != ':' and one[j][3] != 'V' and one[j][
                        2] != '.' and one[j][2] != ':' and one[k][3] != 'V' and one[k][2] != '.' and one[k][
                        2] != ':' and one[l][3] != 'V' and one[l][2] != '.' and one[l][2] != ':' and one[m][
                        3] != 'V' and one[m][2] != '.' and one[m][2] != ':':
                        tmp = one[i][2]
                        one[i][2] = one[i][2] + ' ' + one[j][2] + ' ' + one[k][2] + ' ' + one[l][2] + ' ' + one[m][2]
                        templist = list(one[i])
                        chunks.append(templist)
                        chunkPlace.append(i)
                        one[i][2] = tmp
            return

        totalSents = len(one)
        one_gram(totalSents)
        # print(chunks)
        # two_gram(totalSents)
        # three_gram(totalSents)
        # four_gram(totalSents)
        # five_gram(totalSents)

        # print(chunks)
        ch2 = []
        for i in range(len(chunks)):
            ch2.append([])

        for i in range(len(chunks)):
            chunks[i][10] = 'NP'
            ch2[i] = list(chunks[i])
            ch2[i].append(chunkPlace[i])

        # for i in range(len(chunks)):
        #    print(ch2[i])
        return ch2  #### ch2= final chunks plus i of first member

    def NER_and_chunk_finder(one):
        # x = list(one)
        x = copy_by_value(one)
        neS = []
        for i in range(len(x)):
            neS.append([])
        for i in range(len(x)):
            if len(x[i]) > 1:
                if 'B' in x[i][4]:
                    neS[i].append(i)
                    neS[i].append(x[i])
                    place = i
                    i += 1
                    if len(x[i]) > 1:
                        if 'B-' not in x[i][4] and x[i][4] != 'O':
                            while 'I-' in x[i][4]:
                                neS[place].append(x[i][2])
                                i += 1

        final_ne = []
        for i in range(len(neS)):
            if len(neS[i]) > 1:
                final_ne.append(neS[i])

        ners = []
        for i in range(len(final_ne)):
            tmp = ''
            final_ne[i][1].append(final_ne[i][0])
            if len(final_ne[i]) > 2:
                for k in range(2, len(final_ne[i])):
                    tmp = tmp + ' ' + final_ne[i][k]
            final_ne[i][1][10] = 'Entity'
            if final_ne[i][1][4].find(u'شخص') != -1:
                final_ne[i][1][7] = 'Person'
            elif final_ne[i][1][4].find(u'مکان') != -1:
                final_ne[i][1][7] = 'Location'
            elif final_ne[i][1][4].find(u'ارگان') != -1:
                final_ne[i][1][7] = 'Organization'
            final_ne[i][1][2] = final_ne[i][1][2] + ' ' + tmp

            head = final_ne[i][1][2].split(' ')
            final_ne[i][1].append(head[0])
            ners.append(final_ne[i][1])

        return ners

    def remove_extra_chunks(chunks):
        for i in range(len(chunks)):
            for j in range(len(chunks)):
                if j!=i:
                    if chunks[j][2] in chunks[i][2]:
                        chunks[j][2]=''
        i=0
        while i<len(chunks):
            if chunks[i][2]=='':
                chunks.remove(chunks[i])
            i+=1
        return chunks

    # __________________ make Pairs _______________________
    ### تو این البع میتونم هر نوع داده ای که بخوامو بریزم توی جفت کلمه ها
    # حالا باید هر ویژگی که میخوامو برم توی فایل اصلی درست کنم بعد فایل اصلیو بدم به این تابع
    # یادم باشه کلمات استاپ وردو وارد جفتها نکنم
    def paired_data(chunks, ne, pro,demon):
        oneFile = []
        # print(chunks[0])
        # print(chunks[1])
        # print(ne[1])
        for i in range(len(chunks)):
            oneFile.append(chunks[i])
        for i in range(len(ne)):
            oneFile.append(ne[i])
        for i in range(len(pro)):
            oneFile.append(pro[i])
        for i in range(len(demon)):
            oneFile.append(demon[i])
        for i in range(len(oneFile)):
            if len(oneFile[i])>16:
                oneFile[i][-2]=oneFile[i][-3]
        oneFile = sorted(oneFile, key=lambda tup: tup[-2])

        # print(len(oneFile))
        # print(oneFile[-2])
        pairs = []
        x = ''
        # i token - j token - i - j - PNN (pro-ne-np) i - PNN j - ner type i - ner type  j - animacy i - animacy j - pos16 i - pos16 j -
        # stem i - stem j - sentence i - sentence j - number i - number j -gender i - gender j - proper i - proper j
        # print(oneFile[0])

        for i in range(1, len(oneFile)):
            for j in range(i):
                # tmp = oneFile[i][2].split(' ')
                # headi = tmp[0]
                # tmpj = oneFile[j][2].split(' ')
                # headj = tmpj[0]
                headi = oneFile[i][-1]
                headj = oneFile[j][-1]

                if i!=j:
                # if abs(i - j) > 0:
                    # if oneFile[i][-1]!=oneFile[j][-1]:

                    if len(oneFile[i]) > 1 and len(oneFile[j]) > 1:

                        var = u'{0}'.format(oneFile[i][2] + '\t' + oneFile[j][2] + '\t' + str(oneFile[i][-2]) + '\t' + str(
                            oneFile[j][-2]) + '\t' + oneFile[i][10] + '\t' + oneFile[j][10] + '\t' + oneFile[i][
                                         7] + '\t' + oneFile[j][7] + '\t' +
                                     oneFile[i][11] + '\t' + oneFile[j][11] + '\t' + oneFile[i][3] + '\t' + oneFile[j][
                                         3] + '\t' + oneFile[i][5] + '\t' + oneFile[j][5] + '\t'
                                     + oneFile[i][1] + '\t' + oneFile[j][1] + '\t' + oneFile[i][13] + '\t' + oneFile[j][
                                         13] + '\t' + headi + '\t' + headj + '\t')
                        pairs.append(var)
                        # number - gender-proper ina moonde

                        # pairs.append(x)
        # print(pairs[1])
        # print(pairs[2])
        # print(pairs[3])
        # print(pairs[4])
        # print(pairs[5])
        # print(pairs[6])
        # print(pairs[7])
        # print(pairs[8])
        # print(pairs[9])
        return pairs

    def paired_data_efficient(chunks,ne,pro,demon):
        oneFile=[]
        for i in range(len(chunks)):
            oneFile.append(chunks[i])
        for i in range(len(ne)):
            oneFile.append(ne[i])
        for i in range(len(pro)):
            oneFile.append(pro[i])
        for i in range(len(demon)):
            oneFile.append(demon[i])
        # for i in range(len(oneFile)):
        #      print(oneFile[i][-2],i)
        for i in range(len(oneFile)):
            if len(oneFile[i])>16:
                oneFile[i][-2]=oneFile[i][-3]
        oneFile=sorted(oneFile,key=lambda tup: tup[-2])

        pairs=[]
        x=''
        # i token - j token - i - j - PNN (pro-ne-np) i - PNN j - ner type i - ner type  j - animacy i - animacy j - pos16 i - pos16 j -
        # stem i - stem j - sentence i - sentence j - number i - number j -gender i - gender j - proper i - proper j
        # print(oneFile[0])

        # for i in range(len(oneFile)):
        #     for j in range(len(oneFile)):
        for i in range(1,len(oneFile)):
            for j in range(i):
                headi=oneFile[i][-1]
                headj=oneFile[j][-1]

                if i!=j:
                    if len(oneFile[i]) >1 and len(oneFile[j])>1:
                        pairs.append(oneFile[i][2]+'\t'+oneFile[j][2]+'\t'+str(oneFile[i][-2])+'\t'+str(oneFile[j][-2])+'\t'+ oneFile[i][10]+'\t' + oneFile[j][10] +'\t' + oneFile[i][7]+'\t'+oneFile[j][7] + '\t'+
                           oneFile[i][11] + '\t' + oneFile[j][11] + '\t' +oneFile[i][3] + '\t' + oneFile[j][3] + '\t'+ oneFile[i][5] + '\t' + oneFile[j][5]+ '\t'
                           + oneFile[i][1]+ '\t' + oneFile[j][1]+'\t'+oneFile[i][13] + '\t' + oneFile[j][13]+'\t'+headi+'\t'+headj+'\t')
                           # number - gender-proper ina moonde

        # for i in range(len(pairs)):
            # print(pairs[i])

        return pairs


    # ________________________________small Functions____________________________
    def Head_match(a, b):
        if a == b:
            return 1
        else:
            return 0

    def chunk_match(a, b):
        if a == b:
            return 1
        else:
            return 0

    def sbStr(a, b):
        if a in b:
            return 1
        else:
            return 0

    def mod_match(p):  # if head a == mod b or head a == head b
        kol = p[1]  # mod = kole chunk j
        headB = p[19]  # head j
        modJ = kol.replace(headB, '')  # mod J bedoone head j
        y = 0
        x = 0
        a = p[18]  # a = head i
        modJ = modJ.split(' ')
        if a == headB:
            y = 1
        else:
            y = 0
        for i in range(len(modJ)):
            if modJ[i] == a:
                x = 1
                break
            else:
                x = 0
        res = x or y
        return res

    def same_Sentence(x, y):
        if x == y:
            return 1
        else:
            return 0

    def str_cmpr(a, b):
        res = 0
        if a == b:
            res = 1
        return res

    def distance(x, y):
        dist = abs(x - y)
        return dist

    def what_gender(a):
        femaleList = []
        maleList = []
        gender = 'N'  # neutral
        if a in femaleList:
            gender = 'F'
        elif a in maleList:
            gender = 'M'
        else:
            gender = 'N'
        return gender

    def ij_pronount(x):
        if x == 'PRO':
            return 1
        else:
            return 0

    def number_Match(p):
        # print(p)
        proPL = [u'ما', u'شما', u'آنها', u'ایشان', u'شان', u'یشان', u'مان', u'یمان', u'تان', u'یتان', u'امان', u'اتان', u'اشان',
                 u'خودمان',u'یکدیگر',u'همدیگر']
        p[0] = p[0].strip(' ')
        p[1] = p[1].strip(' ')
        # print(p[1])
        # if p[16].find('PRO')==1 :
        if 'PRO' in p[16]:
            if p[0] in proPL:
                p[16] = p[16] + '-PL'
            else:
                p[16] = p[16] + '-SING'

        # if p[17].find('PRO')==1 :
        if 'PRO' in p[17]:
            if p[1] in proPL:
                p[17] = p[17] + '-PL'
            else:
                p[17] = p[17] + '-SING'
        a = p[16]
        b = p[17]
        # print(a,b)
        if 'PL' in a and 'PL' in b:
            # if a.find('PL') ==1 and b.find('PL')==1:
            #     print('1o1')
            return 1
        elif 'SING' in a and 'SING' in b:
            # print('222')
            return 1
        else:
            return 0

    def animacy_match(a, b):
        if a == 'YES' or a == 'YES(*' or a == 'YES*)' or a == 'YES*':
            a = 'Y'
        if b == 'YES' or b == 'YES(*' or b == 'YES*)' or b == 'YES*':
            b = 'Y'
        if a == 'NO' or a == 'NO(*' or a == 'NO*)' or a == 'NO*':
            a = 'N'
        if b == 'NO' or b == 'NO(*' or b == 'NO*)' or b == 'NO*':
            b = 'N'

        if a == 'Y' and b == 'Y':
            return 1
        elif a == 'N' and b == 'N':
            return 1
        else:
            return 0

    def gender_match(a, b):
        if what_gender(a) != 'N' and what_gender(b) != 'N':
            if what_gender(a) == what_gender(b):
                return 1  # sameGen
            else:
                return 0  # notMatch
        elif what_gender(a) == 'N' or what_gender(b) == 'N':
            return -1  # notApplicable

    def demonstrative(x):
        x = x.replace(u'ي', u'ی')
        x = x.split(' ')
        demon_List = [u'این', u'آن', u'همین', u'همان', u'چنین', u'چنان', u'همچنین', u'همچنان']
        if x[0] in demon_List:
            # print('shd',x[0])
            return 1
        else:
            return 0

    def exclude_STOP_words(pair):
        STOP_List = [u'.', u',', u'،', u'!', u'?', u'؟', u'از', u'با', u'به', u'در', u'تا', u'و', u'بر', u':', u'»', u'«', u'(', u')',
                     '[', ']', '/', '%', '*', '@', '-', '_', ';', u'؛']
        if pair[0] in STOP_List or pair[1] in STOP_List:
            for i in range(len(pair)):
                pair[i] = ''
        return pair

    def remove_null(p):
        cnt = 0
        for i in range(len(p)):
            if p[i][0] == '':
                cnt += 1
                p[i] = ''
        for i in range((cnt)):
            p.remove('')
        return p

    def sortByFirstValue(p):

        p = sorted(p, key=lambda tup: tup[3])
        return p

    def is_ner(a, b):
        if a.find('Entity') != -1 and b.find('Entity') != -1:
            return 1
        else:
            return 0

    def ner_type(a, b):
        if a.find('Person') != -1 and b.find('Person') != -1:
            # print('per')
            return 1
        elif a.find('Location') != -1 and b.find('Location') != -1:
            # print('loc')
            return 1
        elif a.find('Organization') != -1 and b.find('Organization') != -1:
            # print('org')
            return 1
        else:
            # print(0)
            return 0

    # ___________________ make pairs more like features ___________
    def Features(p):
        # ajzaye p :
        # 0,1 chunk i,j
        # 2,3 i,j
        # 4,5 Pro i,j
        # 6,7 NE type i,j
        # 8,9 animacy i,j
        # 10,11 POS-16 i,j
        # 12,13 stem i,j
        # 14,15 sentence number i,j
        # 16,17 POS 100 i,j
        # 18,19 head i,j
        out_P = [p[0], p[1], distance(int(p[14]),
                                      int(p[15])), same_Sentence(int(p[14]), int(p[15])), ij_pronount(p[4]),
                 ij_pronount(p[5]), str_cmpr(p[0], p[1]), Head_match(p[19], p[18]), sbStr(p[19], p[18]), mod_match(p),
                 chunk_match(p[0], p[1]), demonstrative(p[1]), number_Match(p), animacy_match(p[8], p[9]),
                 is_ner(p[4], p[5]), ner_type(p[6], p[7]), p[2], p[3], p[-1]]
        # print(p)
        # print(demonstrative(p[1]))# ه)
        # demonstrative boodan baraye dovomin ozv mohem ast
        # out_P.append(gender_match(p[0],p[1])) # gender match   ino felan ta tahiye Female and Male list bikhial
        ####
        # print(p)
        ################## bara clustering!!!

        # print(p[8],p[9])
        # estefade az stem, NE, NP, proper moonde
        ### my features
        ###################finally!!! this should be the last thing in a list
        # print(p[-1])
        # print(out_P)
        ### class P or N
        # print(out_P)
        return out_P

    # _____________________ word to number function_______________
    def search_and_replace(word, dicts):
        word = word.split(' ')
        number = ''

        for j in range(len(word)):
            if word[j].isdigit():
                number = str(float(word[j]))
            elif word[j] in dicts:
                t = dicts.index(word[j])
                number = number + ' ' + str(t + 1)
                # print(word[j])
            else:
                number = number + ' ' + '-99999999'
                # print(word[j],'!!!!!')
        number = number.strip(' ')
        return number


    def wordToNumber_HO(dic, outWithWords):

        tempList = []
        tempList = copy_by_value(outWithWords)

        for i in range(len(outWithWords)):
            # outWithWords[i] = outWithWords[i].strip('\r\n')
            # outWithWords[i] = outWithWords[i].split(';')


            tempList[i][0] = tempList[i][0].replace(u'ي', u'ی')
            tempList[i][0] = tempList[i][0].strip('"')
            tempList[i][0] = tempList[i][0].strip(' ')

            tempList[i][1] = tempList[i][1].replace(u'ي', u'ی')
            tempList[i][1] = tempList[i][1].strip('"')
            tempList[i][1] = tempList[i][1].strip(' ')
            tempList[i][0] = search_and_replace(tempList[i][0], dic)
            tempList[i][1] = search_and_replace(tempList[i][1], dic)
            Write_svm_results_on_List_2_HO(tempList[i], outNumberWordList)

        return

    def wordToNumber(dict, fileToChange):
        ### read Dict file
        open_File = codecs.open(dict, 'r', 'utf-8')
        d_File = open_File.readlines()
        # print(one_File)
        for i in range(len(d_File)):
            d_File[i] = d_File[i].strip('\r\n')
            d_File[i] = d_File[i].replace(u'ي', u'ی')

        ## read arff file
        open_File = codecs.open(SVMPlace + '\\' + fileToChange, 'r', 'utf-8')
        file_to_change = open_File.readlines()
        # print(one_File)
        # print(len(file_to_change),'********')
        for i in range(len(file_to_change)):
            # print(i,file_to_change[i])
            file_to_change[i] = file_to_change[i].strip('\r\n')
            file_to_change[i] = file_to_change[i].split(';')
            # remove Y arabi and '
            file_to_change[i][0] = file_to_change[i][0].replace(u'ي', u'ی')
            file_to_change[i][0] = file_to_change[i][0].strip('"')
            file_to_change[i][0] = file_to_change[i][0].strip(' ')

            file_to_change[i][1] = file_to_change[i][1].replace(u'ي', u'ی')
            file_to_change[i][1] = file_to_change[i][1].strip('"')
            file_to_change[i][1] = file_to_change[i][1].strip(' ')
            ## search
            file_to_change[i][0] = search_and_replace(file_to_change[i][0], d_File)
            file_to_change[i][1] = search_and_replace(file_to_change[i][1], d_File)
            # Write_svm_results_on_file_2(write_on_numberi, file_to_change[i])

        return file_to_change

    # files = os.listdir(inputCorpus)
    # for file in files:
    # print(file)
    # kharbKari(inputCorpus,file)
    # first=timeit.default_timer()
    # print('START!!!!')

    if len(inputCrpus) > 1:
    # for file in files:
        # theOutPut = 'train-withoutWords_SVM_' + file
        # theOutPut_1 = 'withWord_' + file
        # numberWord = 'train-numbersAsWordsSVM' + '.dat'
        # write_on = codecs.open(SVMPlace + '\\' + theOutPut, 'a+b',
        #                        'utf-8')  # svm without Words(or numbers instead of words)
        # write_on_1 = codecs.open(SVMPlace + '\\' + theOutPut_1, 'a+b',
        #                          'utf-8')  # outPut that contains WORDS not numbers
        # write_on_numberi = codecs.open(SVMPlace + '\\' + numberWord, 'a+b',
        #                                'utf-8')  # SVM type with words (numbers instead of words)


        outTrainWithoutWordsSVMList = []
        outWithWordsList = []
        outNumberWordList = []

        # print(file)
        ##kharbKari(inputCorpus,file)
        ##for n in ne:
        ##    print(n)
        # one = openFile_and_read(inputCorpus, file)    # // .............. This Line should be removed ..................

        ne = NER_and_chunk_finder(inputCrpus)
        # chunks = n_gram_extractor(inputCrpus)  ##### good
        chunk1 = Dadegan_chunker(inputCrpus)
        chunks = remove_extra_chunks(chunk1)
        demon_chunks = demonstrative_chunks(inputCrpus)
        pros = pro_extract(inputCrpus)
        print(len(ne) + len(pros) + len(chunks))

        pairs = paired_data_efficient(chunks, ne, pros, demon_chunks)
        for i in range(len(pairs)):
            pairs[i] = pairs[i].split('\t')
            # print('sdsds')
            # print(pairs[0][-1],'dsjhsjkhdsjkhfjkhfjkdfhjkf')
            # print('sdsdds')
            #             #print(pairs[i])
            #        pairs=sortByFirstValue(pairs)
            #        #print(pairs)
            #        for i in range(len(pairs)):
            #             pairs[i]=exclude_STOP_words (pairs[i])
            # pairs=remove_null(pairs)
            # for i in range(len(pairs)):
            # pairs[i]=pairs[i].split('\t')
            #             # print(pairs[i])

        for i in range(len(pairs)):
            feats = Features(pairs[i])
            # Write_results_on_file(write_on,pairs[i])
            # Write_results_on_file(write_on_1, feats)
            Write_results_on_List_HO(feats, outWithWordsList)
            #            #print(khorooj)
            # Write_svm_results_on_file(write_on, feats)
            Write_svm_results_on_List_HO(feats, outTrainWithoutWordsSVMList)

    # write_on.close()
    # write_on_1.close()
    # second=timeit.default_timer()
    print('feature File Made')
    # print('Make Feature File time: ',second-first)
    print('searching in that HUGE! dictionary')
    # x = codecs.open(SVMPlace + '\\' + theOutPut, 'r', 'utf-8')
    # x = x.readlines()
    # y = codecs.open(SVMPlace + '\\' + theOutPut_1, 'r', 'utf-8')
    # y = y.readlines()
    # print(len(x), len(y), '-------------------')
    #o = wordToNumber(main_dict, theOutPut_1)
    wordToNumber_HO(DictionaryData, outWithWordsList)
    # write_on_numberi.close()
    # last=timeit.default_timer()
    # print('Total Time: ',last-first)
    #
    output = []
    output.append(outNumberWordList)
    output.append(outWithWordsList)
    return output


def SVM_HO(modelToUse, input, file_name):

    def makeInputFile():
        # file_name = str(uuid.uuid4())
        input_file_name = folder_out + '\\' + file_name
        f = codecs.open(input_file_name, 'w', 'utf-8')
        for i in range(len(input)):
            for j in range(len(input[i])):
                f.write(input[i][j])
            f.write('\n')
        f.flush()
        f.close()
        return file_name

    inputFileName = makeInputFile()
    outputFileName = folder_out + '\\' + 'Result_' + inputFileName
    inputFileName = folder_out + '\\' + inputFileName
    model = SVMPlace + '\\' + modelToUse
    subprocess.call([SVMPlace + '\\' + 'svm_classify.exe', inputFileName, model, outputFileName])
    return outputFileName

def SVM(modelToUse):
    input = SVMPlace + '\\' + 'train-numbersAsWordsSVM.dat'
    outPut = SVMPlace + '\\' + 'Result_' + 'train-numbersAsWordsSVM.dat'
    model = SVMPlace + '\\' + modelToUse
    subprocess.call([SVMPlace + '\\' + 'svm_classify.exe', input, model, outPut])
    return

def make_outPut(withWordList, svmResult, fileId):

    svm = codecs.open(svmResult, 'r', 'utf-8')
    svm = svm.readlines()
    output = []
    outWithLen = []

    for i in range(len(svm)):
        score = float(svm[i])
        if score > 0.0:
            tmp = []
            tmpWithLen = []
            words1 = withWordList[i][0].split(' ')
            words2 = withWordList[i][1].split(' ')
            len1 = len(words1)
            len2 = len(words2)

            tmpWithLen.append(withWordList[i][-3])
            tmpWithLen.append(len1)
            outWithLen.append(tmpWithLen)

            tmpWithLen = []

            tmpWithLen.append(withWordList[i][-2])
            tmpWithLen.append(len2)
            outWithLen.append(tmpWithLen)

            tmp.append(withWordList[i][-3])
            tmp.append(withWordList[i][-2])

            b = False
            for j in range(len(output)):
                if tmp[0] in output[j] or tmp[1] in output[j]:
                    output[j] = list(set(output[j]+tmp))
                    b = True
            if b==False:
                output.append(tmp)

    finalOut = []

    for i in range(len(output)):
        finalOut.append([])
        b = False

        if len(output[i]) == 2 and output[i][0]==output[i][1]:
            continue

        for j in range(len(output[i])):
            for k in range(len(finalOut)):
                if output[i][j] in finalOut[k]:
                    finalOut[k] = list(set(finalOut[k] + output[i]))
                    b = True
                    break
            if b == True:
                break
        if b == False:
            finalOut[i] = output[i]

    outpth = folder_out+'\\'+'REL_'+fileId
    file_out = codecs.open(outpth, 'w', 'utf-8')
    for i in range(len(finalOut)):
        if len(finalOut[i]) == 0:
            continue
        for j in range(len(finalOut[i])):
            # file_out.write(finalOut[i][j] + '\t')
            len_phrase = 1
            for k in range(len(outWithLen)):
                if outWithLen[k][0]==finalOut[i][j]:
                    len_phrase = outWithLen[k][1]
                    break
            file_out.write(finalOut[i][j]+','+str(len_phrase)+'\t')
        file_out.write('\n')
    file_out.flush()
    file_out.close()
    return outpth


def make_outPut1(withWordList, svmResult, fileId):
    svm = codecs.open(svmResult, 'r', 'utf-8')
    svm = svm.readlines()
    output = []
    for i in range(len(svm)):
        score = float(svm[i])
        tmp = []
        if score > 0.0:
            tmp.append(withWordList[i][0])
            tmp.append(withWordList[i][1])
            tmp.append(withWordList[i][-3])
            tmp.append(withWordList[i][-2])
            output.append(tmp)

    outpth = folder_out + '\\' + 'REL_' + fileId
    file_out = codecs.open(outpth, 'w', 'utf-8')
    for i in range(len(output)):
        words1 = output[i][0].split(' ')
        words2 = output[i][1].split(' ')
        len1 = len(words1)
        len2 = len(words2)
        file_out.write(output[i][0]+'\t'+output[i][1]+'\t'+output[i][2]+','+str(len1)+'\t'+output[i][3]+','+str(len2)+'\n')

    file_out.flush()
    file_out.close()
    return outpth


def testResult(numberWordFile, wordi, finalFile):
    Gold = SVMPlace + '\\' + numberWordFile
    system = SVMPlace + '\\' + 'Result_' + numberWordFile
    print(wordi)
    text = SVMPlace + '\\' + wordi
    print(text)
    asliF = finalFile
    ### openFile Gold
    g = open(Gold, 'r')
    gold = g.readlines()
    for i in range(len(gold)):
        gold[i] = gold[i].strip('\r\n')
        gold[i] = gold[i].split(' ')
    ### openFile and modify system
    s = open(system, 'r')
    sys = s.readlines()
    for i in range(len(sys)):
        sys[i] = sys[i].strip('\r\n')
        # print(sys[i])
        if float(sys[i]) > 0:
            sys[i] = '1'
        else:
            sys[i] = '-1'
    ### deghat
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    # print(sys[0])
    x = 0
    for i in range(len(sys)):
        if gold[i][0] == '1':
            x += 1
        if gold[i][0] == '1' and sys[i] == '1':
            # print(1)
            tp += 1
        elif gold[i][0] == '-1' and sys[i] == '-1':
            tn += 1
        elif gold[i][0] == '1' and sys[i] == '-1':
            fn += 1
        elif gold[i][0] == '-1' and sys[i] == '1':
            fp += 1

    print(tp, fp, tn, fn)
    if tp + fp != 0:
        precision = tp / (tp + fp)
    if tp + fn != 0:
        recall = tp / (tp + fn)
        f1 = (2 * precision * recall) / (precision + recall)
        print(tp, tn, fn, fp)
        print('P: ', precision, 'R: ', recall, 'F1: ', f1)

    o = codecs.open(text, 'r', 'utf-8')
    o = o.readlines()
    print(len(sys), len(o))
    for i in range(len(sys)):
        # print(i)
        o[i] = o[i].strip('\r\n')
        o[i] = o[i].split(';')
        # print(o[i][0])
    out = codecs.open(SVMPlace + '\\' + 'out ' + wordi, 'w', 'utf-8')
    chainolen = []
    chainolen1 = []
    for i in range(len(o)):
        if sys[i] == '1':
            out.write(o[i][0] + '\t' + o[i][1] + '\t' + o[i][-2] + '\t' + o[i][-3] + '\t' + sys[i] + '\n')

            o[i][1] = o[i][1].strip('"')
            o[i][0] = o[i][0].strip('"')
            o[i][1] = o[i][1].strip(' ')
            o[i][0] = o[i][0].strip(' ')
            o[i][1] = o[i][1].split(' ')
            o[i][0] = o[i][0].split(' ')

            len1 = len(o[i][1])
            len0 = len(o[i][0])

            # out.write(str(len0)+'\t'+str(len1)+'\t'+o[i][-2]+'\t'+o[i][-3]+'\t'+sys[i]+'\n')
            chainolen.append((o[i][-2]))  # words
            chainolen1.append(len1)  # lens
            chainolen.append((o[i][-3]))
            chainolen1.append(len0)
    # print(len(chainolen),len(chainolen1))
    out.close()

    def chainYesareKon(chains):
        finalChains = []
        for i in range(len(chains)):
            if len(chains[i]) > 1:
                aa = list(set(chains[i]))
                finalChains.append(aa)
        return finalChains

    def corefChainMaker():
        chains = []
        inp = codecs.open(SVMPlace + '\\' + 'out ' + wordi, 'r', 'utf-8')
        inp = inp.readlines()
        for i in range(len(inp)):
            inp[i] = inp[i].strip('\n')
            inp[i] = inp[i].split('\t')
            chains.append([])
            chains[i].append(inp[i][-2])
            chains[i].append(inp[i][-3])
        for i in range(len(chains)):
            for j in range(i, len(chains)):
                chainHa(chains, i, j)
        return chains, inp

    # def chainOword(chains,):

    def chainHa(chains, a, b):
        for k in range(len(chains[b])):
            if chains[b][k] in chains[a]:
                chains[a].append(chains[b][0])
                chains[a].append(chains[b][1])
                t1 = chains[b][0]
                t2 = chains[b][1]
                chains[b].remove(t1)
                chains[b].remove(t2)
                break
        return

    chains, a = corefChainMaker()
    # print(a)
    for i in range(len(chains)):
        for j in range(i, len(chains)):
            chainHa(chains, i, j)
    finalChains = (chainYesareKon(chains))
    print(chainolen)
    print(finalChains)
    print(chainolen1)
    benevis = []

    leneThatChunk = 0
    z = 0
    # print(len(benevis))

    asli = codecs.open(asliF, 'r', 'utf-8')
    asli = asli.readlines()
    for i in range(len(asli)):
        benevis.append('-')
    outFinal = codecs.open('theOutPut_12.txt', 'w', 'utf-8')
    for i in range(len(finalChains)):
        for j in range(len(finalChains[i])):

            z = chainolen.index(finalChains[i][j])
            leneThatChunk = chainolen1[z]
            t = int(finalChains[i][j]) + 1
            # print((finalChains[i][j]),leneThatChunk)
            if leneThatChunk > 2:
                benevis[int(finalChains[i][j])] = '(' + str(i)
                for k in range(t, t + leneThatChunk - 1):
                    benevis[k] = '*'
                benevis[int(finalChains[i][j]) + leneThatChunk - 1] = str(i) + ')'
            elif leneThatChunk == 1:
                benevis[int(finalChains[i][j])] = '(' + str(i) + ')'
            else:
                benevis[int(finalChains[i][j])] = '(' + str(i)
                benevis[int(finalChains[i][j]) + 1] = str(i) + ')'
    for i in range(len(benevis)):
        outFinal.write('text' + '\t' + benevis[i] + '\n')

    return

def generateWords(corpus):

    words = []
    for i in range(len(corpus)-1):
        words.append(corpus[i][2])

    return words

def readRelPath(relPath):
    f = codecs.open(relPath, 'r', 'utf-8')
    f = f.readlines()

    return f

def makeFinalOutputFile(out_data, chains,tokens):

    # Build Output Format Here
    # s = ''
    # s.index()
    finalOut = []
    count = 0
    num_chain = 0
    for i in range(len(tokens)):
        tmp = []
        tmp.append(tokens[i])
        b = False
        for j in range(len(chains)):
            if j==0:
                num_chain = 1
            else:
                m=0
                while m<j:
                    num_chain = num_chain+len(chains[m])
                    m = m+1

            if str(i) in chains[j]:
                count = count + 1
                tmp.append(count)
                b = True
                break
        if b:
            tmp.append(num_chain)
        else:
            tmp.append('-')
            tmp.append('-')

        finalOut.append(tmp)

            #     for k in range(len(out_data)):
            #         if tokens[i] in out_data[k]:
            #             parts1 = out_data[k][0].split(' ')
            #             parts2 = out_data[k][1].split(' ')
            #
            #             len1 = len(parts1)
            #             len2 = len(parts2)
            #             if len1 > 1:
            #                 indx1 = out_data[k][2]
            #                 if tokens[i] in parts1:
            #                     ix = out_data[k][2].index(tokens[i])
            #                     tokens[indx1-ix]



# ==========================  Uncompleted  Code  ============================ #

                    # for t in range(len(out_data[k])):
                    #     if tokens[i] in


    return finalOut


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





# urls = (
#     '/coref/(.*)','Coref'
# )
#
# app = web.application(urls,globals())
# class CorefService():

def DoCoref(text,option):
    # wordTaggedFile = 'withWord_0-9.txt'
    # taggedFile = 'train-numbersAsWordsSVM.dat'
# def GET(self,name):
#     i = web.input()
#     pth = web.websafe(i.txt)
#     text = readInputFile(pth)

    finalFile = []

    if option=='2':
        finalFile = preprocess(words=text, option=option)

    elif option=='1':
        file_id = str(uuid.uuid4())
        nrmText, words, wordsPerSentence = normalizeText(file_id, text)
        finalFile = preprocess(words = wordsPerSentence,option=option)
        words = generateWords(finalFile)
        outFeatList = makeFeatureFile(finalFile, nrmText)
        outSVM = SVM_HO(SVMmodel, outFeatList[0], file_id)

        rel_path = make_outPut(outFeatList[1], outSVM, file_id)

        # rel_path = make_outPut1(outFeatList[1], outSVM, file_id)
        out = []
        tmp = []
        tmp.append(readRelPath(rel_path))
        tmp.append(words)
        out.append(tmp)
        # return 'Completed Successfully!'

        # finalOut = makeFinalOutputFile(out, chains, words)

        finalFile = out


    return finalFile

def readInputFile(in_path):
    f = codecs.open(in_path,'r','utf-8')
    contents = f.read()
    return contents

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
    if countArgs < 4:
        print('Help Usage 1: programName   InputFilePath   ResultFilePath  tokenFilePath  1')
        print('\n')
        print('Help Usage 2: programName   InputFilePath   ResultFilePath  2')
        print ('\n')
    else:
        readConfigFile()

        if sys.argv[3]=='2':
            tkns = readInputTokensFile(sys.argv[1])
            output = DoCoref(tkns,sys.argv[3])

            writeOutput(sys.argv[2], output)

        elif sys.argv[4]=='1':
            text = readInputFile(sys.argv[1])
            output = DoCoref(text,sys.argv[4])

            chain = output[0][0]
            tokens = output[0][1]
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

        print('\n .... Coref successfully Done ....')
except:
    print('........ Exception Occured .........')



# if __name__ == "__main__":
    # from wsgiref.simple_server import make_server
    # server = make_server('localhost',5454,CorefService())
    # server.serve_forever()
    # readConfigFile()
    # DoCoref()

    # server = SOAPpy.SOAPServer(('localhost',5454))
    # server.registerFunction(DoCoref)
    # server.serve_forever()

    # from wsgiref.simple_server import make_server
    # soap_app = soaplib.wsgi.Application([CorefService],'tns')
    # wsgi_app = wsgi.Application(soap_app)
    # server = make_server('localhost',5454,wsgi_app)
    # server.serve_forever()

    # app.run()