x=open('train-2.txt','r')
x=x.readlines()
for i in range(len(x)):
    x[i]=x[i].strip('\r\n')
    x[i]=x[i].split(' ')
o=open('train-1.txt','w')
t=[]
for i in range(len(x)):
    if x[i][0]=='-1':
        x[i][0]='1'
    else:
        x[i][0]='-1'
for i in range(len(x)):
    for j in range(len(x[i])):
        o.write(x[i][j]+' ')
    o.write('\n')

