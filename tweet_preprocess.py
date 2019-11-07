import string
import re
from collections import defaultdict


def genre_trans(line):
    genre = line[-1]
    if genre == 'vehicles':
        line = line[:-2]
        line.append(1)
    if genre == 'comedy':
        line = line[:-1]
        line.append(2)
    if genre == 'education':
        line = line[:-1]
        line.append(3)
    if genre == 'entertainment':
        line = line[:-1]
        line.append(4)
    if genre == 'animation':
        line = line[:-2]
        line.append(5)
    if genre == 'gaming':
        line = line[:-1]
        line.append(6)
    if genre == 'style':
        line = line[:-2]
        line.append(7)
    if genre == 'music':
        line = line[:-1]
        line.append(8)
    if genre == 'politics':
        line = line[:-2]
        line.append(9)
    if genre == 'activism':
        line = line[:-2]
        line.append(10)
    if genre == 'animals':
        line = line[:-2]
        line.append(11)
    if genre == 'technology':
        line = line[:-2]
        line.append(12)
    if genre == 'sports':
        line = line[:-1]
        line.append(13)
    if genre == 'events':
        line = line[:-1]
        line.append(14)
    return line

tweet_test_file = open('tweetsclassification/Tweets.14cat.test',encoding="utf-8",errors='ignore',mode='r+')
tweet_train_file = open('tweetsclassification/Tweets.14cat.train',encoding="utf-8",errors='ignore',mode='r+')
tweet_test = tweet_test_file.readlines()
tweet_train = tweet_train_file.readlines()


feats = set()
#feats_train for part b
feats_train = []
feats_test = []

'''
train part to generate feats_dic for the model and dict of train datas for further analyse

'''
for index, item in enumerate(tweet_train):
    line = item.split()
    if line == None:
        continue
    line = [i for i in line if  'http' not in i]
    line = [i for i in line if  'RT' not in i]
    line = [i.lower() for i in line]
    id = line[0]
    line = ' '.join(line)
    line = re.split(r'[^0-9a-zA-Z@#]\s*',line)
    #r'[;,&%-:=.$\[\]\(\)\'\/"?!\s]\s*'
    line = [i for i in line if i !='']
    line = line[1:]
    feats_train.append([id,genre_trans(line)])
    feats.update(set(line))


'''
test part to generate feats_dic for the model and dict of train datas for further analyse

'''
for index, item in enumerate(tweet_test):
    line = item.split()
    if line == None:
        continue
    line = [i for i in line if  'http' not in i]
    line = [i for i in line if  'RT' not in i]
    line = [i.lower() for i in line]
    id = line[0]
    line = ' '.join(line)
    line = re.split(r'[^0-9a-zA-Z@#]\s*',line)
    #r'[;,&%-:=.$\[\]\(\)\'\/"?!\s]\s*'
    line = [i for i in line if i !='']
    line = line[1:]
    feats_test.append([id,genre_trans(line)])


'''
output part for feats_dic
'''
feats_dic = defaultdict(int)
feats_dic_file = open('tweetsclassification/feats_dic','w+')
for i ,item in enumerate(feats):
    feats_dic[item] = i+1
    feats_dic_file.write(str(i+1)+'\t'+item+'\n')

'''
feats_train part:
output
'''

feats_train_file = open('tweetsclassification/feats_train','w+')
for item in feats_train:
    feats_train_file.write(str(item[1][-1])+'\t')
    id = item[0]
    orderlist=[]
    item[1] = item[1][:-1]
    for feat in item[1]:
        feat_id = feats_dic[feat]
        orderlist.append(feat_id)
    for item in sorted(orderlist):
        feats_train_file.write('\t'+str(item)+':1\t')
    orderlist = []
    feats_train_file.write('#'+str(id)+'\n')

'''
feats_test part:
output
'''

feats_train_file = open('tweetsclassification/feats_test','w+')
for item in feats_test:
    feats_train_file.write(str(item[1][-1])+'\t')
    id = item[0]
    orderlist=[]
    item[1] = item[1][:-1]
    for feat in item[1]:
        feat_id = feats_dic[feat]
        if feat_id == 0:
            continue
        orderlist.append(feat_id)
    for item in sorted(orderlist):
        feats_train_file.write('\t'+str(item)+':1\t')
    orderlist = []
    feats_train_file.write('#'+str(id)+'\n')
