# coding=utf-8
import codecs
import subprocess, sys
import os
from zeep import Client
# def SRL(fiii,File,Boundary_Sentences):
def SRL(normalizedText,preprocessWSDL,taggerWSDL,depWSDL):
    # path_out="SHADI_Chunks"
    # subprocess.call(['spellchecker-exe.exe','-N',File,path_out+'\\'+'Data_normalized.txt'])
    # inp=codecs.open(path_out+'\\'+'Data_normalized.txt', 'r', 'utf-8')
    # inp=inp.readlines()

    ########### Input should be normalized Text  ############
    inp = normalizedText.split('\n')
    wsdl = 'http://185.130.78.112/preprocess/PreprocessWebService.asmx?WSDL'
    client = Client(wsdl = preprocessWSDL)



    #########################Write each Token in a line
    # y=codecs.open(path_out+'\\'+"Tokens_Test.txt",'w','utf-8')
    # gg=codecs.open(path_out+'\\'+"Test_Tokens_With_Index.txt",'w','utf-8')
    # z=codecs.open(path_out+'\\'+"Sentence_Test.txt",'w','utf-8')
    y=[]
    gg=[]
    z=[]
    temp = ''
    for i in range(len(inp)):
        inp[i] = inp[i].strip('\n')
        inp[i] = inp[i].strip('\r')
        inp[i] = inp[i].replace('  ', ' ')
        # z.append(inp[i])
        z.append(inp[i] + '\n')
        # inp[i] = inp[i].split(' ')
        inp[i] = client.service.Tokenize(inp[i])
        cou=0
        if inp[i] is not None:
            for j in range(len(inp[i])):
                temp = ''
                cou=cou+1
                nnn=str(cou)
                if len(inp[i][j])>0:
                    temp += nnn+'\t'+inp[i][j]
                else:
                    temp += inp[i][j]
                gg.append(temp + '\n')
                temp = ''
                y.append(inp[i][j])
                # y.append('\n')
    # y.close()
    # z.close()
    # gg.close()
    ###################################ِ100_POS_Bijankhan
    # subprocess.call(['TestTagger.exe','-tag',path_out+'\\'+'Tokens_Test.txt',path_out+'\\'+'Test_POS_100.txt','model-100-new'])
    wsdl = 'http://http://185.130.78.112/pos/Tagger_WebService.asmx?WSDL'
    client = Client(wsdl = taggerWSDL)
    input_type = client.get_type('ns0:ArrayOfString')
    inputObj = input_type(y)
    tags = client.service.GetTagsAdvancedByArray(inputObj, modelname='model-100-new')

    ############################################
    # w=codecs.open(path_out+'\\'+'Test_POS_100.txt','r','utf-8')
    # w=w.readlines()
    w = tags
    # M=codecs.open(path_out+'\\'+'Test_Tafkik_POS_100.txt','w','utf-8')
    M = []
    temp = ''
    for j in range(len(w)):
        # w[j]=w[j].strip('\n')
        # w[j]=w[j].strip('\r')
        # w[j]=w[j].split('\t')
        if len(w[j])>0:
            tmp_nn=w[j].split('-')
            temp += tmp_nn[0]+'\t'+w[j]+'\t'
            for k in range(1,len(tmp_nn)):
                if k!=len(tmp_nn)-1:
                    temp += tmp_nn[k]+'_'
                else:
                    temp += tmp_nn[k]
            if len(tmp_nn)==1:
               temp+=tmp_nn[0]
            M.append(temp+'\n')
            temp = ''

        else:
            M.append(temp+'\n')
            temp = ''
    # M.close()

    # M=codecs.open(path_out+'\\'+'Test_Tafkik_POS_100.txt','r','utf-8')
    # z=codecs.open(path_out+'\\'+'Test_Tokens_With_Index.txt','r','utf-8')
    # H=codecs.open(path_out+'\\'+'Test_File_For_Malt_Parser.txt','w','utf-8')
    # z=z.readlines()
    # M=M.readlines()
    z = gg
    # T = codecs.open('outDir\\Test_File_for_MaltParser.txt', 'w', 'utf-8')
    H = []
    temp = ''
    for i in range(len(z)):
        z[i]=z[i].strip('\n')
        z[i] = z[i].strip('\r')
        z[i]=z[i].split('\t')
        M[i]=M[i].strip('\n')
        M[i]=M[i].strip('\r')
        M[i]=M[i].split('\t')
        if len(z[i])>1:
            temp = z[i][0]+'\t'+z[i][1]+'\t'+'_'+'\t'+M[i][0]+'\t'+M[i][1]+'\t'+M[i][2]+'\t'+'_'+'\t'+'_'+'\t'+'_'+'\t'+'_'
            H.append(temp)
            # T.write(temp+'\n')
            temp = ''
        else:
            H.append('')
            # T.write('\n')
    # T.close()
    # H.close()
    # subprocess.call(['java','-jar','maltparser-1.9.0.jar','-c','Dadegan_Malt_Parser_Model.mco','-i',path_out+'\\'+'Test_File_For_Malt_Parser.txt','-o',path_out+'\\'+'Test_Output_Parser.txt','-m','parse'])
    wsdl = 'http://185.130.78.112/depparser/DependencyParser_WS.asmx?WSDL'
    client = Client(wsdl = depWSDL)
    input_type = client.get_type('ns0:ArrayOfString')
    inputObj = input_type(H)
    out_maltParser = client.service.DoParseAdvancedByArray(inputObj, modelKey='SRL')

 ##############################Boundary_Extraction_From_Dependency_Parser
    # x=codecs.open(path_out+'\\'+'Test_Output_Parser.txt','r','utf-8')
    # x=x.readlines()
    x=[]
    for i in range(len(out_maltParser)):
        if out_maltParser[i] is None:
            x.append('\n')
        else:
            x.append(out_maltParser[i]+'\n')

    # ppp=codecs.open(path_out+'\\'+'Chunks'+'\\'+Boundary_Sentences,'w','utf-8')
    ppp = []

    Li=[]
    Li.append(-1)
    for i in range(len(x)):
        x[i] = x[i].strip('\n')
        x[i] = x[i].strip('\r')
        x[i] = x[i].replace('\ufeff', '')
        x[i] = x[i].split('\t')
        if len(x[i])<2:
            Li.append(i)

    temp = ''
    for j in range(len(Li)-1):
        A=Li[j]+1
        B=Li[j+1]
        if x[A][7]=='SBJ' and x[A][3]!='N':
            Token=[]
            DEP_PRE=[]
            Token.append(x[A][0])
            DEP_PRE.append(x[A][0])
            Control = 1
            while Control == 1:
                       EMP = []
                       for tt in range(len(Token)):
                           for ii in range(A, B):
                               if x[ii][6] == Token[tt] and x[ii][3]!='V' and x[ii][7]!='NVE':
                                   if x[ii][0] not in DEP_PRE:
                                       DEP_PRE.append(x[ii][0])
                                       EMP.append(x[ii][0])
                       if len(EMP) > 0:
                          Control = 1
                          Token = EMP
                       else:
                           Control = 0
            counter=0
            Mat = []
            for kk in range(A, B):
                XXX = x[kk][0]
                for h in range(len(DEP_PRE)):
                    if XXX == DEP_PRE[h]:
                        counter=counter+1
                        Mat.append(kk)

            for aa in range(len(Mat)):
                GH = Mat[aa]
                SH = x[GH][0]
                for ff in range(A, B):
                    if x[ff][0] == SH and x[ff][3]!='P' and x[ff][3]!='DELM' and x[ff][7]!='NVE' and x[ff][1]!=u'که':
                        temp += x[ff][1] + ' '
            temp += '\t'+'NP_SBJ'+'\t'+str(Mat[0])
            ppp.append(temp+'\n')
            temp = ''
        for k in range(A,B):
            if x[k][7]=='SBJ':
                Token=[]
                DEP_PRE=[]
                Token.append(x[k][0])
                DEP_PRE.append(x[k][0])
                Control = 1
                if x[k][3]=='CON':
                   Token=[]
                   Token.append(x[k+1][0])
                   DEP_PRE=[]
                   DEP_PRE.append(x[k+1][0])
                while Control == 1:
                       EMP = []
                       for tt in range(len(Token)):
                           for ii in range(A, B):
                               if x[ii][6] == Token[tt] and x[ii][3]!='V' and x[ii][7]!='NVE':
                                   if x[ii][0] not in DEP_PRE:
                                       DEP_PRE.append(x[ii][0])
                                       EMP.append(x[ii][0])
                       if len(EMP) > 0:
                          Control = 1
                          Token = EMP
                       else:
                           Control = 0
                counter=0
                Mat = []
                for kk in range(A, B):
                      XXX = x[kk][0]
                      for h in range(len(DEP_PRE)):
                          if XXX == DEP_PRE[h]:
                             counter=counter+1
                             Mat.append(kk)

                if len(Mat)>1:
                    for aa in range(len(Mat)):
                        GH = Mat[aa]
                        SH = x[GH][0]
                        for ff in range(A, B):
                            if x[ff][0] == SH and x[ff][3]!='P' and x[ff][3]!='DELM' and x[ff][7]!='NVE' and x[ff][1]!=u'که':
                                temp += x[ff][1] + ' '
                    temp += '\t'+'NP_SBJ'+'\t'+str(Mat[0])
                    ppp.append(temp+'\n')
                    temp = ''

            if x[k][7]=='OBJ':
                Token=[]
                DEP_PRE=[]
                Token.append(x[k][0])
                DEP_PRE.append(x[k][0])
                if x[k][3]=='CON':
                   Token=[]
                   Token.append(x[k+1][0])
                   DEP_PRE=[]
                   DEP_PRE.append(x[k+1][0])
                Control = 1
                while Control == 1:
                       EMP = []
                       for tt in range(len(Token)):
                           for ii in range(A, B):
                               if x[ii][6] == Token[tt] and x[ii][3]!='V' and x[ii][7]!='NVE':
                                   if x[ii][0] not in DEP_PRE:
                                       DEP_PRE.append(x[ii][0])
                                       EMP.append(x[ii][0])
                       if len(EMP) > 0:
                          Control = 1
                          Token = EMP
                       else:
                           Control = 0
                counter=0
                Mat = []
                for kk in range(A, B):
                      XXX = x[kk][0]
                      for h in range(len(DEP_PRE)):
                          if XXX == DEP_PRE[h]:
                             counter=counter+1
                             Mat.append(kk)
                if len(Mat)>1:
                    for aa in range(len(Mat)):
                        GH = Mat[aa]
                        SH = x[GH][0]
                        for ff in range(A, B):
                            if x[ff][0] == SH and x[ff][3]!='P' and x[ff][3]!='V' and x[ff][3]!='DELM' and x[ff][7]!='NVE'  and x[ff][0]!=u'که':
                                temp += x[ff][1] + ' '
                    temp += '\t'+'NP_OBJ'+'\t'+str(Mat[0])
                    ppp.append(temp+'\n')
                    temp = ''

            if x[k][7]=='NPP' or x[k][7]=='MOZ' and x[k][3]!='AJ':
                Token=[]
                DEP_PRE=[]
                Token.append(x[k][0])
                DEP_PRE.append(x[k][0])
                if x[k][3]=='CON':
                   Token=[]
                   Token.append(x[k+1][0])
                   DEP_PRE=[]
                   DEP_PRE.append(x[k+1][0])
                Control = 1
                while Control == 1:
                       EMP = []
                       for tt in range(len(Token)):
                           for ii in range(A, B):
                               if x[ii][6] == Token[tt] and x[ii][3]!='V' and x[ii][7]!='NVE':
                                   if x[ii][0] not in DEP_PRE:
                                       DEP_PRE.append(x[ii][0])
                                       EMP.append(x[ii][0])
                       if len(EMP) > 0:
                          Control = 1
                          Token = EMP
                       else:
                           Control = 0
                counter=0
                Mat = []
                for kk in range(A, B):
                      XXX = x[kk][0]
                      for h in range(len(DEP_PRE)):
                          if XXX == DEP_PRE[h]:
                             counter=counter+1
                             Mat.append(kk)
                if len(Mat)>1:
                    for aa in range(len(Mat)):
                        GH = Mat[aa]
                        SH = x[GH][0]
                        for ff in range(A, B):
                            if x[ff][0] == SH and x[ff][3]!='P' and x[ff][3]!='V' and x[ff][3]!='DELM' and x[ff][7]!='NVE'  and x[ff][0]!=u'که':
                                temp += x[ff][1] + ' '
                    temp += '\t'+'NP'+'\t'+str(Mat[0])
                    ppp.append(temp+'\n')
                    temp = ''

            if x[k][7]=='ROOT' and x[k][3]=='N':
                Token=[]
                DEP_PRE=[]
                Token.append(x[k][0])
                DEP_PRE.append(x[k][0])
                Control = 1

                while Control == 1:
                       EMP = []
                       for tt in range(len(Token)):
                           for ii in range(A, B):
                               if x[ii][6] == Token[tt] and x[ii][3]!='V' and x[ii][7]!='NVE':
                                   if x[ii][0] not in DEP_PRE:
                                       DEP_PRE.append(x[ii][0])
                                       EMP.append(x[ii][0])
                       if len(EMP) > 0:
                          Control = 1
                          Token = EMP
                       else:
                           Control = 0
                counter=0
                Mat = []
                for kk in range(A, B):
                      XXX = x[kk][0]
                      for h in range(len(DEP_PRE)):
                          if XXX == DEP_PRE[h]:
                             counter=counter+1
                             Mat.append(kk)
                if len(Mat)>1:
                    for aa in range(len(Mat)):
                        GH = Mat[aa]
                        SH = x[GH][0]
                        for ff in range(A, B):
                            if x[ff][0] == SH and x[ff][3]!='P' and x[ff][3]!='V' and x[ff][3]!='DELM' and x[ff][7]!='NVE'  and x[ff][0]!=u'که':
                                temp += x[ff][1] + ' '
                    temp += '\t'+'NP'+'\t'+str(Mat[0])
                    ppp.append(temp + '\n')
                    temp = ''


            if x[k][7]=='ADV':
                Token=[]
                DEP_PRE=[]
                Token.append(x[k][0])
                DEP_PRE.append(x[k][0])
                if x[k][3]=='CON':
                   Token=[]
                   Token.append(x[k+1][0])
                   DEP_PRE=[]
                   DEP_PRE.append(x[k+1][0])
                Control = 1
                while Control == 1:
                       EMP = []
                       for tt in range(len(Token)):
                           for ii in range(A, B):
                               if x[ii][6] == Token[tt] and x[ii][3]!='V' and x[ii][7]!='NVE':
                                   if x[ii][0] not in DEP_PRE:
                                       DEP_PRE.append(x[ii][0])
                                       EMP.append(x[ii][0])
                       if len(EMP) > 0:
                          Control = 1
                          Token = EMP
                       else:
                           Control = 0
                counter=0
                Mat = []
                for kk in range(A, B):
                      XXX = x[kk][0]
                      for h in range(len(DEP_PRE)):
                          if XXX == DEP_PRE[h]:
                             counter=counter+1
                             Mat.append(kk)
                hhh=Mat[0]
                if len(Mat)>1 and x[hhh][3]!='P':
                    for aa in range(len(Mat)):
                        GH = Mat[aa]
                        SH = x[GH][0]
                        for ff in range(A, B):
                            if x[ff][0] == SH and x[ff][3]!='V' and x[ff][3]!='DELM' and x[ff][7]!='NVE'  and x[ff][0]!=u'که':
                                temp += x[ff][1] + ' '
                    temp += '\t'+'NP'+'\t'+str(Mat[0])
                    ppp.append(temp + '\n')
                    temp = ''
        ppp.append(temp + '\n')
    # ppp.close()
    return ppp




