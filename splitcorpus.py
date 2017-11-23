corpus = open('corpuslimpio.txt','r',encoding='utf8')
pos = open('pos.txt','w',encoding='utf8')
neg = open('neg.txt','w',encoding='utf8')


for line in corpus.readlines():
    if line[0] == 'P':
        pos.write(line[2:])
    elif line[0] == 'N':
        neg.write(line[2:])

corpus.close()
pos.close()
neg.close()