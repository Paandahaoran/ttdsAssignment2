import  re
def qrels_input():
    file = open('systems/qrels.txt','r+')
    qrels=[]
    for item in file.readlines():
        line = []
        for i in item.strip().split():
            line.append(re.findall('\d+',i))
        qrels.append(line)
    return qrels

def results_input(filename):
    file = open('systems/'+filename,'r+')
    results = []
    results_each = []
    prev_id = '1'
    for item in file.readlines():
        query_number = item.strip().split()[0]
        doc_number = item.strip().split()[2]
        rank_of_doc = item.strip().split()[3]
        score = item.strip().split()[4]
        result = [query_number,doc_number,rank_of_doc,score]
        if  query_number != prev_id:
            results.append(results_each)
            results_each = []
            results_each.append(result)
        else:
            results_each.append(result)
        prev_id = query_number
    results.append(results_each)
    return results

#qrels_input()
#print(results_input('S1.results')[9])
