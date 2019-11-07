import doc_process
import numpy as np
from collections import defaultdict
from decimal import Decimal


'''
calculate Precision with standard input
'''
def Precision(TP,FP,FN):
    if FP == 0:
        return 0
    return float(TP)/float(FP)

'''
calculate Recall with standard input
'''
def Recall(TP,FP,FN):
    if FN == 0:
        return 0
    return float(TP)/float(FN)


'''
input sysID,queryID and specific rank@ required
return precision and recall
'''
def precision_recall_atrank(sysID,rank,queryID):
    Precisions = []
    Recalls = []
    qrels = doc_process.qrels_input()
    results = doc_process.results_input('S'+str(sysID)+'.results')
    #FN = qrels[i][1:]
    #extract relevant docIDs from query as FN
    FN = [item[0] for item in qrels[queryID][1:]]
    #FP = results[i][0:10]
    #extract retrieved docIDs for specifc query as FP
    FP = [item[1] for item in results[queryID][0:rank]]
    TP = set(FN) & set(FP)
    Pres = Precision(len(TP),len(FP),len(FN))
    recall = Recall(len(TP),len(FP),len(FN))
    return Pres,recall


'''
Temporary execution function
'''
def exe_Pat10_Rat50():
    precisions = []
    recalls = []
    precision = []
    recall = []
    for i in range(1,7):
        for j in range(0,10):
            precision.append(precision_recall_atrank(i,10,j)[0])
            recall.append(precision_recall_atrank(i,50,j)[1])
        precisions.append(precision)
        recalls.append(recall)
        precision = []
        recall = []
    return precisions,recalls



'''
return r_Precision of the system ,input with sysID
'''
def r_Precision(sysID):
    qrels = doc_process.qrels_input()
    r_Precision = []
    r_Precisions = []
    for i,item in enumerate(qrels):
        #Call precision_recall_atrank function with rank input = len(item)-1 : delete the first queryID element
        r_Precisions.append(precision_recall_atrank(sysID,len(item)-1,i)[0])
    return r_Precisions


'''
return AP of the system for specifc query
'''
def AP(sysID,queryID):
    #data inputs
    qrels = doc_process.qrels_input()
    results = doc_process.results_input('S'+str(sysID)+'.results')
    Precisions = []
    #FN = qrels[i][1:]
    FN = [item[0] for item in qrels[queryID][1:]]
    #FP = results[i][0:10]
    FP_all = [item[1] for item in results[queryID]]
    index_of_rank = [i for i, x in enumerate(FP_all) if x in FN]
    #index in FP_all from zero
    #
    for i,index in enumerate(index_of_rank):
        Pres = float(i+1)/(index+1)
        Precisions.append(Pres)
    if Precisions == []:
        return 0
    else:
        return sum(Precisions)/len(FN)

'''
return MAP of specific ststem,input with S-number
'''
def MAP(sysID):
    APs = []
    for i in range(0,10):
        APs.append(AP(sysID,i))
    return sum(APs)/len(APs)



def DG(index,value):
    if index == 1:
        return value
    else:
        return float(value)/(np.log2(index))

#calculate to find DCG
def DCG(sysID,queryID,rank):
    DCG = 0.0#iniatialize
    #input qrels and results from documents
    qrels = doc_process.qrels_input()
    results = doc_process.results_input('S'+str(sysID)+'.results')
    #sepreate value and docID from qrels
    FN = [item[0] for item in qrels[queryID][1:]]
    IR_values = [item[1] for item in qrels[queryID][1:]]
    #extract docID from retrieved documents
    FP_all = [item[1] for item in results[queryID]]
    '''trying to get the relvant docID and its value from retrieved system documents
        store the index of docID and value of docID together in the list:  indexandValue_of_rank,
        for the calculation of DG
    '''
    for i,x in enumerate(FP_all):
        #care '=' causer i start with 0 and rank start with 1
        if i >= rank:
            break
        if x in FN:
             #[0] in indexandValue_of_rank means the rank in retrieved system, index start at 0
             #[1] in indexandValue_of_rank means the value of the docID in [0] position

             #then calculate the DG with the rank[0] and value[1],this list just for understanding the
             #process easily, not necessary

            #indexandValue_of_rank.append([i,IR_values[FN.index(x)]])

            #calculation of DG ,the index should start with 1
            DCG += float(DG(i+1,IR_values[FN.index(x)]))
    return(DCG)




def iDCG(sysID,queryID,rank):
    iDCG = 0.0#iniatialize
    #data input
    qrels = doc_process.qrels_input()
    results = doc_process.results_input('S'+str(sysID)+'.results')
    iDCG_values = sorted([item[1] for item in qrels[queryID][1:]],reverse=True)
    for i,item in enumerate(iDCG_values):
        if i >= rank:
            break
        iDCG += DG(i+1,int(item))
    return iDCG




def nDCG(sysID,queryID,rank):
    return DCG(sysID,queryID,rank)/iDCG(sysID,queryID,rank)



'''
execution function to generate output to the format required , all number was forced to be 3 demical points
output files will show in the path:   /system/...
intermidiar variables:
means = {list} with all value for each systems
means_all{list} with all mean values of each systems
'''
def execution():
    means_all = defaultdict(list)
    for i in range(1,7):
        means = defaultdict(list)
        file = open('systems/S'+str(i)+'.eval','w+')
        file.write('\t'+ 'P@10\t' + 'R@50\t' + "r_Precision\t" + 'AP\t' + 'nDCG@10\t' + 'nDCG@20\n')
        for j in range(0,10):
            p10 = Decimal(precision_recall_atrank(i,10,j)[0]).quantize(Decimal('0.000'))
            means['p10'].append(p10)
            r50 = Decimal(precision_recall_atrank(i,50,j)[1]).quantize(Decimal('0.000'))
            means['r50'].append(r50)
            r_pre = Decimal(r_Precision(i)[j]).quantize(Decimal('0.000'))
            means['r_pre'].append(r_pre)
            ap = Decimal(AP(i,j)).quantize(Decimal('0.000'))
            means['ap'].append(ap)
            nDCG10 = Decimal(nDCG(i,j,10)).quantize(Decimal('0.000'))
            means['nDCG10'].append(nDCG10)
            nDCG50 = round(nDCG(i,j,50),3)
            means['nDCG50'].append(nDCG50)
            file.write(str(j+1)+'\t'+str(p10)+'\t'+str(r50)+'\t'+ str(r_pre)+'\t'+ str(ap) +'\t'+str(nDCG10) + '\t'+str(nDCG50))
            file.write('\n')
            Decimal(AP(i,j)).quantize(Decimal('0.000'))
        p10_m = str(Decimal(float(sum(means['p10']))/len(means['p10'])).quantize(Decimal('0.000')))
        r50_m = str(Decimal(float(sum(means['r50']))/len(means['r50'])).quantize(Decimal('0.000')))
        r_pre_m = str(Decimal(float(sum(means['r_pre']))/len(means['r_pre'])).quantize(Decimal('0.000')))
        ap_m = str(Decimal(float(sum(means['ap']))/len(means['ap'])).quantize(Decimal('0.000')))
        nDCG10_m = str(Decimal(float(sum(means['nDCG10']))/len(means['nDCG10'])).quantize(Decimal('0.000')))
        nDCG50_m = str(Decimal(float(sum(means['nDCG50']))/len(means['nDCG50'])).quantize(Decimal('0.000')))
        means_all[i] = [p10_m,r50_m,r_pre_m,ap_m,nDCG10_m,nDCG50_m]
        file.write('mean\t'+p10_m+'\t'+r50_m+'\t'+ r_pre_m+'\t'+ ap_m +'\t'+nDCG10_m + '\t'+nDCG50_m)
    file_all = open('systems/ALL.eval','w+')
    file_all.write('\t'+ 'P@10\t' + 'R@50\t' + "r_Precision\t" + 'AP\t' + 'nDCG@10\t' + 'nDCG@20\n')
    for no in range(1,7):
        file_all.write('S'+str(no)+'\t'+means_all[no][0]+'\t'+means_all[no][1]+'\t'+means_all[no][2]+'\t'+means_all[no][3]+'\t'+means_all[no][4]+'\t'+means_all[no][5]+'\n')
execution()
