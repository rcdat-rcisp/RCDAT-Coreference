__author__ = 'RCDAT'
#____________________ imports!_______________________
import codecs
import os
import  subprocess
import  timeit

####-------------------------places------------------

folderNum='1'
inputCorpus='finalCorpus\\p'+folderNum
outPutFiles='featureFiles'
main_dict='Final_dict.txt' ### old dictionary with many many words
#main_dict='Final_dict.txt' # new dictionary, just train words
theOutPut='train-withoutWords_SVM'+folderNum+'.txt'
theOutPut_1='withWord'+folderNum+'.txt'

#______________kharabkari_____________________________
def kharbKari(inputCorpus,file):
    o=openFile_and_read(inputCorpus,file)
    out=codecs.open(inputCorpus+'\\'+file,'w','utf-8')
    for i in range(len(o)):
        if o[i][1]=='' or o[i][1]=='-' or o[i][1]=='*)':
                o[i][1]=o[i-1][1]
        for j in range(len(o[i])-1):
                    out.write(o[i][j]+'\t')
        out.write(o[i][-1])
        out.write('\n')
    out.write(o[-2][0]+'\t'+o[-2][1]+'\t'+'.	PUNC	O	.	.	-	-	-	-	-	O	DELM'+'\n')
    out.close()

    return
#________________readAndWrite_________________________
def openFile_and_read(inputCorpus,file):
    open_File=codecs.open(inputCorpus+'\\'+file,'r','utf-8')
    one_File=open_File.readlines()
    for i in range(len(one_File)):
        one_File[i]=one_File[i].strip('\r\n')
        one_File[i]=one_File[i].split('\t')

    return one_File
#

def Write_results_on_file(x,ooniKeBayadNevesht):
    x.write('"'+ooniKeBayadNevesht[0]+'"'+';'+'"'+ooniKeBayadNevesht[1]+'"'+';')
    for i in range(2,len(ooniKeBayadNevesht)-1):
            x.write(str(ooniKeBayadNevesht[i])+';')
    x.write("'"+ooniKeBayadNevesht[-1]+"'")
    x.write('\n')

    return
def Write_svm_results_on_file(x,ooniKeBayadNevesht):

    ooniKeBayadNevesht[-1].strip('\r\n')
    if ooniKeBayadNevesht[-1]=='N':
        x.write('-1 ')
    if ooniKeBayadNevesht[-1]=='P':
        x.write('1 ')
    if ooniKeBayadNevesht[2]>=2:
        x.write('2:1 ')
    else:
        x.write('2:2 ')
    for i in range(3,len(ooniKeBayadNevesht)-3):
        if ooniKeBayadNevesht[i]==1:
            x.write(str(i+100)+':2 ')
        else:
             x.write(str(i+100)+':1 ')
    x.write('\n')
    return
def Write_svm_results_on_file_2(x,ooniKeBayadNevesht):
    ooniKeBayadNevesht[-1].strip('\r\n')
    ooniKeBayadNevesht[0]=ooniKeBayadNevesht[0].split(' ')
    ooniKeBayadNevesht[1]=ooniKeBayadNevesht[1].split(' ')
    for i in range(len(ooniKeBayadNevesht[0])):
        ooniKeBayadNevesht[0][i]=int(float(ooniKeBayadNevesht[0][i]))
    for i in range(len(ooniKeBayadNevesht[1])):
        ooniKeBayadNevesht[1][i]=int(float(ooniKeBayadNevesht[1][i]))

    ooniKeBayadNevesht[0].sort()
    ooniKeBayadNevesht[1].sort()
    if ooniKeBayadNevesht[-1]=="'N'":
        x.write('-1 ')
    if ooniKeBayadNevesht[-1]=="'P'":
        x.write('1 ')
    if int(ooniKeBayadNevesht[2])>=2:
        x.write('2:1 ')
    else:
        x.write('2:2 ')
    for i in range(3,len(ooniKeBayadNevesht)-3):
        if ooniKeBayadNevesht[i]=='1':
            x.write(str(i+100)+':2 ')
        else:
             x.write(str(i+100)+':1 ')
    z=ooniKeBayadNevesht[0]+ooniKeBayadNevesht[1]
    word=list(set(z))
    word.sort()
    for i in range(len(word)):
        if word[i]>0:
            x.write(str(word[i]+200)+':1 ')
    x.write('\n')
    return
#___________________split Groups______________________
def split_g(one):
    grouped=[]
    www=[]
    for i in range(len(one)):
        grouped.append([])
    for i in range(len(one)):
        grouped[i].append(one[i])
    for i in range(len(one)):
        if len(one[i])>1:
            if one[i][-3].find('(*')!=-1:
                place=i
                www.append(place)
                grouped[place].append(i)
                i+=1
                while one[i][-3].find('*')!=-1 or one[i][-3].find('*)')!=-1:
                        grouped[place].append(one[i][2]+'*'+one[i][3])
                        i+=1
            elif one[i][-3].find('-') == -1 and one[i][-3].find('*)') == -1 and one[i][-3].find('*') == -1:
                one[i][2]=one[i][2]+' '
                place=i
                www.append(place)
                grouped[place].append(i)
                i+=1

    x=grouped.count([''])
    for i in range(x):
        grouped.remove([''])
    tmp=[]
    m=2
    for i in range(len(grouped)):
        if len(grouped[i])>m: ### 12 toole yek line dar yek file  boode ke alan shode 14!!!
            tmp=[]
            for j in range(len(grouped[i])-m):
                tmp.append(' '+str(grouped[i][m+j]))
        ####
            grouped[i][0][2]=grouped[i][0][2]+'*'+grouped[i][0][3]
        for k in range(len(tmp)):
            if len(grouped[i])>m:
                grouped[i][0][2]= grouped[i][0][2]+tmp[k]
        if len(grouped[i])>m:
            head,word=head_detector(grouped[i])
            grouped[i][0].append(head)
            grouped[i][0][2]=word

    return grouped
#___________________split Groups + chunks______________________
def split_groups_withChunks_oldChunker(one):
    grouped=[]
    www=[]
    q=0
    n=12 # olace of Chunk
    g_type=[]
    chunks_split=[]
    for i in range(len(one)):
        grouped.append([])
        g_type.append('O')
        chunks_split.append('')
    for i in range(len(one)):
        if len(one[i])>=1:
            chunks_split[i]=(one[i][0][n].split('-'))
            if chunks_split[i][0]=='O':
                chunks_split[i].append('O')


    for i in range(len(one)):
        if len(one[i][0])>= 1:
            if chunks_split[i][0]=='B':
                place=i
                www.append(place)
                grouped[place].append(one[i][0])
                grouped[place].append(i)
                q+=1
                if chunks_split[i][0]!='O':
                    g_type[place]=chunks_split[i][1]

                i+=1

                while (chunks_split[i][1]==g_type[place] and chunks_split[i][0]=='I'):
                        grouped[place].append(one[i][0][2]+'*'+one[i][0][3])
                        grouped[i]=['']
                        i+=1

            elif chunks_split[i][0]=='O':
                place=i
                grouped[place].append(one[i][0])
                grouped[place].append(i)
                q+=1
                i+=1

    x=grouped.count([''])
    for i in range(x):
        grouped.remove([''])
    tmp=[]
    m=2
    for i in range(len(grouped)):
        if len(grouped[i])>m: ### m  toole yek line dar yek file
            tmp=[]
            for j in range(len(grouped[i])-m):
                tmp.append(' '+str(grouped[i][m+j]))
            grouped[i][0][2]=grouped[i][0][2]+'*'+grouped[i][0][3]
        for k in range(len(tmp)):
            if len(grouped[i])>m:
                grouped[i][0][2]= grouped[i][0][2]+tmp[k]
        if len(grouped[i])>m:
            head,word=head_detector(grouped[i])
            grouped[i][0].append(head)
            grouped[i][0][2]=word

    return grouped
#### __ headDetect
def head_detector(oneF):
    one=oneF[0][2]
    www=[]
    one=one.split(' ')
    for j in range(len(one)):
        one[j]=one[j].split('*')
    word=''
    for i in range(len(one)):
            word=word+' '+one[i][0]
    for i in range(len(one)):
            if one[i][1]=='N' or one[i][1]=='N-SING-COM' or one[i][1]=='N-SING-PR' or one[i][1]=='N-PL-PR'or one[i][1]=='N-PL-COM' :
                head=one[i][0]
                break
            else:
                head=one[0][0]
    word=word.strip(' ')
    return head,word

#______________________combine 2 splits _________________
#________________ Mention Detection ------------------
def Is_NEOR_chunk(one,n): # n=4 ne , n=12 chunk
    chosen=[]
    grouped=[]
    q=0
    # n=4 # place of NER
    g_type=[]
    chunks_split=[]
    for i in range(len(one)):
        grouped.append([])
        g_type.append('O')
        chunks_split.append('')
    for i in range(len(one)):
        if len(one[i])>=1:
            chunks_split[i]=(one[i][n].split('-'))
            if chunks_split[i][0]=='O':
                chunks_split[i].append('O')

    for i in range(len(one)):
        if len(one[i])>= 1:
            if chunks_split[i][0]=='B':
                place=i
                chosen.append(place)
                grouped[place].append(one[i])
                grouped[place].append(i)
                q+=1
                if chunks_split[i][0]!='O':
                    g_type[place]=chunks_split[i][1]

                i+=1

                while (chunks_split[i][1]==g_type[place] and chunks_split[i][0]=='I'):
                        grouped[place].append(one[i][2])
                        grouped[i]=['']
                        i+=1

            elif chunks_split[i][0]=='O':
                place=i
                grouped[place].append(one[i])
                grouped[place].append(i)
                q+=1
                i+=1

    x=grouped.count([''])
    for i in range(x):
        grouped.remove([''])
    tmp=[]
    m=2

    #print(len(grouped[1]))
    for i in range(len(grouped)):
        if len(grouped[i])>m: ### m  toole yek line dar yek file
            tmp=[]

            for j in range(len(grouped[i])-m):
                tmp.append(' '+str(grouped[i][m+j]))
        for k in range(len(tmp)):
            if len(grouped[i])>m:
                grouped[i][0][2]= grouped[i][0][2]+tmp[k]

    print('----------------------------')
    return grouped,chosen
#______________________________________
def combine_2_chunkers(one):
    two=split_g(one)
    spaSe=' '
    tmp=[]
    x=two.count([['']])
    #print(x)
    for i in range(x):
        two.remove([['']])
    for i in range(len(two)):
        tmp.append(two[i][0][2]) ### negah darande meghdar token
        if len(two[i])>1:
            if spaSe in two[i][0][2]:
                two[i][0][2]=''
                two[i][0][12]='XX-XXX'
    four=[]
    three=split_groups_withChunks_oldChunker(two)
    for i in range(len(three)):
        if len(three[i])>1:
            if three[i][0][-3]=='B-NP':
                four.append(three[i])
    whole_test=[]
    for i in range(len(four)+len(two)):
        whole_test.append([])
    for i in range(len(two)):
            if len(two[i])>1:
                two[i][0][2]=tmp[i]
                whole_test[i].append(two[i][0])
                whole_test[i].append(two[i][1])
    l=len(two)
    for i in range(l,len(whole_test)):
        if len(three[i-l])>=2:
            whole_test[i].append(four[i-l][0])
            whole_test[i].append(four[i-l][1])
    x=whole_test.count([])
    for i in range(x):
        whole_test.remove([])

    whole_test=sorted(whole_test,key=lambda tup: tup[1])


    return whole_test
#__________________ make Pairs _______________________

def paired_data(oneFile):

    pairs=[]
    x=1
    # i token - j token - i - j - PNN (pro-ne-np) i - PNN j - ner i - ner j - animacy i - animacy j - pos16 i - pos16 j -
    # stem i - stem j - sentence i - sentence j - number i - number j -gender i - gender j - proper i - proper j
    for i in range(len(oneFile)):
        for j in range(1,len(oneFile)-i):
            if len(oneFile[i]) >1 and len(oneFile[i+j])>1:
                x=(oneFile[i][2]+'\t'+oneFile[i+j][2]+'\t'+str(i)+'\t'+str(i+j)+'\t'+ oneFile[i][10]+'\t' + oneFile[i+j][10] +'\t' + oneFile[i][7]+'\t'+oneFile[i+j][7] + '\t'+
                   oneFile[i][11] + '\t' + oneFile[i+j][11] + '\t' +oneFile[i][3] + '\t' + oneFile[i+j][3] + '\t'+ oneFile[i][5] + '\t' + oneFile[i+j][5]+ '\t'
                   + oneFile[i][1]+ '\t' + oneFile[i+j][1]+'\t'+ oneFile[i][13]+ '\t' + oneFile[i+j][13])

                pairs.append(x)
    print(pairs[0])

    return pairs
def paired_data_version2(ones):
    oneFile=[]
    for i in range(len(ones)):
        oneFile.append(ones[i][0])
    corefS=[]
    for i in range(len(oneFile)):
        if len(oneFile[i])>1:
            if oneFile[i][9]!='-':
                corefS.append(i)
    pos_pairs=[]

    chains=[]
    neg_pairs=[]
    for i in range(len(corefS)): ### find chains
            x1=oneFile[corefS[i]][9]
            x1=x1.replace('(*','')
            x1=x1.replace('*','')
            x1=x1.replace('*0','')
            x1=x1.replace(')','')
            chains.append(x1)
    u_chains=list(set(chains))
    ch=[]
    for i in range(len(u_chains)): # make chains
        ch.append([])
    for i in range(len(corefS)):
            x1=oneFile[corefS[i]][9]
            x1=x1.replace('(*','')
            x1=x1.replace('*','')
            x1=x1.replace('*0','')
            x1=x1.replace(')','')
            for j in range(len(u_chains)):
                if u_chains[j]==x1:
                    ch[j].append(corefS[i])
    for i in range(len(ch)):
        for j in range(1,len(ch[i])):
            a=int(ch[i][j])
            b=int(ch[i][j-1])
            if len (oneFile[a])>14:
                headi=oneFile[a][14]
            else:
                headi=oneFile[a][2]
            if len (oneFile[b])>14:
                headj=oneFile[b][14]
            else:
                headj=oneFile[b][2]

            bothData=(oneFile[a][2]+'\t'+oneFile[b][2]+'\t'+str(ones[a][1])+'\t'+str(ones[b][1])+'\t'+ oneFile[a][10]+'\t' + oneFile[b][10] +'\t' + oneFile[a][7]+'\t'+oneFile[b][7] + '\t'+
                       oneFile[a][11] + '\t' + oneFile[b][11] + '\t' +oneFile[a][3] + '\t' + oneFile[b][3] + '\t'+ oneFile[a][5] + '\t' + oneFile[b][5]+ '\t'
                       + oneFile[a][1]+ '\t' + oneFile[b][1]+'\t'+oneFile[a][13]+'\t'+oneFile[b][13]+'\t'+headi+'\t'+headj+'\t'+'P')
            pos_pairs.append(bothData)
    neg_pairs1=[]
    for i in range(len(ch)): 
        for j in range(1,len(ch[i])):
            a=int(ch[i][j])
            b=int(ch[i][j-1])
            for k in range(b+1,a):
                 if len (oneFile[a])>14:
                    headi=oneFile[a][14]
                 else:
                    headi=oneFile[a][2]
                 if len (oneFile[k])>14:
                    headj=oneFile[k][14]
                 else:
                    headj=oneFile[k][2]
                 if a!=b:
                    bothData=(oneFile[a][2]+'\t'+oneFile[k][2]+'\t'+str(ones[a][1])+'\t'+str(ones[k][1])+'\t'+ oneFile[a][10]+'\t' + oneFile[k][10] +'\t' + oneFile[a][7]+'\t'+oneFile[k][7] + '\t'+
                       oneFile[a][11] + '\t' + oneFile[k][11] + '\t' +oneFile[a][3] + '\t' + oneFile[k][3] + '\t'+ oneFile[a][5] + '\t' + oneFile[k][5]+ '\t'
                       + oneFile[a][1]+ '\t' + oneFile[k][1]+'\t'+oneFile[a][13]+'\t'+oneFile[k][13]+'\t'+headi+'\t'+headj+'\t'+'N')
                    neg_pairs.append(bothData)
    pairs=[]
    for i in range(len(neg_pairs)):
        pairs.append(neg_pairs[i])
    for j in range(len(pos_pairs)):
        pairs.append(pos_pairs[j])
    return pairs
#________________________________small Functions____________________________
def Head_match(a,b):
    if a==b:
        return 1
    else:
        return 0
def chunk_match(a,b):
    if a==b:
        return 1
    else:
        return 0
def sbStr(a,b):
    if a in b:
        return 1
    else:
        return 0
def mod_match(p): # if head a == mod b or head a == head b
    kol=p[1] # mod = kole chunk j
    headB=p[19] # head j
    modJ=kol.replace(headB,'') # mod J bedoone head j
    y=0
    x=0
    a=p[18] # a = head i
    modJ=modJ.split(' ')
    if a== headB:
        y=1
    else:
        y=0
    for i in range(len(modJ)):
        if modJ[i]== a:
            x=1
            break
        else:
            x=0
    res= x or y
    return res
def same_Sentence(x,y):
    if x==y:
        return 1
    else:
        return 0

def str_cmpr(a,b):
    res=0
    if a == b :
        res=1
    return res
def distance(x,y):
    dist = abs(x-y)
    return dist
def what_gender(a):
    femaleList=[]
    maleList=[]
    gender='N'#neutral
    if a in femaleList:
        gender='F'
    elif a in maleList:
        gender='M'
    else:
        gender='N'
    return gender
def ij_pronount(x):
    if x=='PRO':
        return 1
    else:
        return 0

def number_Match(a,b):
        if a.find('PL') ==1 and b.find('PL')==1:
            return 1
        elif a.find('SING') ==1 and b.find('SING')==1:
            return 1
        else:
            return 0
def is_ner(a,b):
    if a.find('Entity')!=-1 and b.find('Entity')!=-1:
        return 1
    else:
        return 0
def ner_type(a,b):
    if a.find('Person')!=-1 and b.find('Person')!=-1:
        return 1
    elif a.find('Location')!=-1 and b.find('Location')!=-1:
        return 1
    elif  a.find('Organization')!=-1 and b.find('Organization')!=-1:
        return 1
    else:
        return 0

def animacy_match(a,b):
    if a=='YES' or a =='YES(*' or a == 'YES*)' or a=='YES*':
        a='Y'
    if b=='YES' or b =='YES(*' or b == 'YES*)' or b=='YES*':
        b='Y'
    if a=='NO' or a =='NO(*' or a == 'NO*)' or a=='NO*':
        a='N'
    if b=='NO' or b =='NO(*' or b == 'NO*)' or b=='NO*':
        b='N'

    if a=='Y' and b == 'Y':
        return 1
    elif a=='N' and b=='N':
        return 1
    else:
        return 0
def gender_match(a,b):
    if what_gender(a)!='N' and what_gender(b)!='N':
        if what_gender(a)==what_gender(b):
            return 1 # sameGen
        else:
            return 0 #notMatch
    elif what_gender(a)=='N' or what_gender(b)=='N':
        return -1 # notApplicable
def demonstrative(x):
    x=x.replace('ي','ی')
    x=x.split(' ')
    demon_List=['این','آن','همین','همان','چنین','چنان','همچنین','همچنان']
    if x[0] in demon_List:
        return 1
    else:
            return 0
def exclude_STOP_words(pair):
     STOP_List=['.',',','،','!','?','؟','از','با','به','در','تا','و','بر',':','»','«','(',')','[',']','/','%','*','@','-','_',';','؛']
     if pair[0] in STOP_List or pair[1] in STOP_List:
         for i in range(len(pair)):
             pair[i]=''
     return pair
def remove_null(p):
    cnt=0
    for i in range(len(p)):
        if p[i][0]=='':
            cnt+=1
            p[i]=''
    for i in range((cnt)):
        p.remove('')
    return p
def sortByFirstValue(p):

    p=sorted(p,key=lambda tup: tup[3])
    return p
#_____________________ SVM___________________
def SVM(numberWordFile):
    input=outPutFiles+'\\'+numberWordFile
    tmp=numberWordFile.strip('.dat')
    outPut=outPutFiles+'\\'+'model_'+tmp
    subprocess.call([outPutFiles+'\\'+'svm_learn.exe',input,outPut])
    print('model is in: ', outPut)
    return
#___________________ make pairs more like features ___________
def Features(p):

    # ajzaye p :
    # print(p)
    # 0,1 chunk i,j
    # 2,3 i,j
    # 4,5 Pro i,j  (pro,entity, other)
    # 6,7 NE type i,j
    # 8,9 animacy i,j
    # 10,11 POS-16 i,j
    # 12,13 stem i,j
    # 14,15 sentence number i,j
    # 16,17 POS 100 i,j
    # 18,19 head i,j
    out_P=[]
    out_P.append(p[0]) # token i
    out_P.append(p[1]) # token j
    out_P.append(distance(  int(p[14]),int(p[15]) )) # distance (if in the same sentence res=0 if 1 sentence apart res=1 , ... )
    out_P.append(same_Sentence(int(p[14]),int(p[15]))) # sameSentence
    out_P.append(ij_pronount(p[4])) # i_pronoun
    out_P.append(ij_pronount(p[5])) # j_pronoun
    out_P.append(str_cmpr(p[0],p[1])) # str Match
    out_P.append(Head_match(p[19],p[18])) # head match
    out_P.append(sbStr(p[19],p[18])) # head sub str dovomi too avali hast???
    out_P.append(mod_match(p)) # mod Match
    out_P.append(chunk_match(p[0],p[1])) # chunk match
    out_P.append(demonstrative(p[1])) #demonstrative NP j (با این و آن همین و همان شروع بش
    #print(demonstrative(p[1]))# ه)
    # demonstrative boodan baraye dovomin ozv mohem ast
    out_P.append(number_Match(p[16],p[17])  ) # number match
    ####
    # print(p)
    out_P.append(animacy_match(p[8],p[9])) # animacy match
    ########## NER
    out_P.append(is_ner(p[4],p[5]))
    out_P.append(ner_type(p[6],p[7]))
    ################## bara clustering!!!
    out_P.append(p[2])
    out_P.append(p[3])
    ### my features
    # this should be the last thing in a list
    out_P.append(p[-1]) ## class P or N


    return out_P
#_____________________ word to number function_______________
def search_and_replace(word,dicts):
    word=word.split(' ')
    number=''

    for j in range(len(word)):
        if word[j].isdigit():
            number=str(float(word[j]))
        elif word[j] in dicts:
                t=dicts.index(word[j])
                number=number+' '+str(t+1)
        else:
                number=number+' '+'-99999999'
    number=number.strip(' ')
    return number

def wordToNumber(dict,fileToChange):
    ### read Dict file
    open_File=codecs.open(dict,'r','utf-8')
    d_File=open_File.readlines()
    for i in range(len(d_File)):
        d_File[i]=d_File[i].strip('\r\n')
        d_File[i]=d_File[i].replace('ي','ی')

    open_File=codecs.open(outPutFiles+'\\'+fileToChange,'r','utf-8')
    file_to_change=open_File.readlines()
    for i in range(len(file_to_change)):
        file_to_change[i]=file_to_change[i].strip('\r\n')
        file_to_change[i]=file_to_change[i].split(';')
        # remove Y arabi and '
        file_to_change[i][0]=file_to_change[i][0].replace('ي','ی')
        file_to_change[i][0]=file_to_change[i][0].strip('"')
        file_to_change[i][0]=file_to_change[i][0].strip(' ')

        file_to_change[i][1]=file_to_change[i][1].replace('ي','ی')
        file_to_change[i][1]=file_to_change[i][1].strip('"')
        file_to_change[i][1]=file_to_change[i][1].strip(' ')
        ## search
        file_to_change[i][0]=search_and_replace(file_to_change[i][0],d_File)
        file_to_change[i][1]=search_and_replace(file_to_change[i][1],d_File)
        Write_svm_results_on_file_2(write_on_numberi,file_to_change[i])

    return file_to_change
files=os.listdir(inputCorpus)
for file in files:
    kharbKari(inputCorpus,file)
write_on=codecs.open(outPutFiles+'\\'+theOutPut,'a+b','utf-8') # svm without Words(or numbers instead of words)
write_on_1=codecs.open(outPutFiles+'\\'+theOutPut_1,'a+b','utf-8') # outPut that contains WORDS not numbers
write_on_numberi=codecs.open(outPutFiles+'\\'+'train-numbersAsWordsSVM'+folderNum+'.dat','a+b','utf-8') # SVM type with words (numbers instead of words)
first=timeit.default_timer()
print('START!!!!')
y=0
d=0
for file in files:
    print(file)
    one=openFile_and_read(inputCorpus,file)
    grouped=combine_2_chunkers(one)
    pairs=paired_data_version2(grouped)
    for i in range(len(pairs)):
         pairs[i]=pairs[i].split('\t')
    pairs=sortByFirstValue(pairs)
    for i in range(len(pairs)):
         pairs[i]=exclude_STOP_words (pairs[i])
    pairs=remove_null(pairs)
    for i in range(len(pairs)):
        khorooj=Features(pairs[i])
        Write_results_on_file(write_on_1,khorooj)####
        Write_svm_results_on_file(write_on,khorooj)####

second=timeit.default_timer()
print('feature File Made')
print('Make Feature File time: ',second-first)
print('searching in that HUGE! dictionary')
write_on.close() ############number saz
write_on_1.close()
o=wordToNumber(main_dict,theOutPut_1)
last=timeit.default_timer()
forSVM='train-numbersAsWordsSVM'+folderNum+'.dat'
SVM(forSVM)
print('Total Time: ',last-first)

