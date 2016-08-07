from collections import defaultdict
import time


def find_frequent_item(db,min_support,seq_pattern):

    #db2 = np.array(db)
    #print(db2)
    prefix = defaultdict(lambda: 0)
    prefix_list = []
    last = seq_pattern[-1:]
    #print(db,'start')
    prefix_out = ''
    #start1 = time.time()
    for sequence in db: #calculate prefix 
        seq_done = defaultdict(lambda: 0)
        for itemset in sequence:           
            has_ = 0
            has_last = defaultdict(lambda: 0)
            has_last['o']= 0
            check_pre = 0
            for index,item in enumerate(itemset):
                if item == '_' :
                    has_ = 1
                if item != '_' :
                    #for item1 in itemset[:index+1]:
                    itemnew = item + ')'
                    if (check_pre == 1 or has_ == 1)  and prefix[itemnew] < min_support and seq_done[itemnew] == 0:
                        prefix[itemnew]+=1  # has )
                        seq_done[itemnew] = 1
                        if prefix[itemnew] >= min_support:
                            prefix_list.append(itemnew)
                
                    if seq_done[item] == 0 and has_ == 0 and prefix[item] < min_support:
                        prefix[item]+=1
                        seq_done[item] = 1
                        if prefix[item] >= min_support:
                            prefix_list.append(item)
                
                #if prefix in itemset :
                    if check_pre == 0:
                        for pattern in reversed(seq_pattern):
                            if itemset[index] == pattern or itemset[index] == pattern[:-1]:
                                has_last['o'] = 1
                                has_last[str(pattern)] = 1
                            else:
                                has_last[str(pattern)] = 0
                        #print(pattern)
                            
                            #print('lsitfor', itemset[index]  , has_last[str(pattern)])
                            index -= index

                            if pattern[-1:] != ')' or has_last[str(pattern)] == 0 :
                                break
                        if all(i == 1 for i in has_last.values()):
                            check_pre = 1

#if prefix_list != []:
#       print(prefix_list,'plist')

##    end1 = time.time()
##    elapsed1 = end1 - start1
##    print( "FOR(1) Time taken: ", elapsed1, "seconds.")


    #start2 = time.time()
    for prefix in prefix_list:  #create probject_DB
        db_project= []
        if seq_pattern ==[]:
            new = 1
        else:
            new = 0
        seq_pattern.append(prefix)
        for seq in db:
            seq_new = []
            a=0
            for itemset in seq:    
                itemset_new = itemset[:]
                if a==0:
                    has_ = 0
                    has_pre = 0
                    for item in itemset:
                        
                        if item == '_' :
                            has_ = 1
                        if seq_pattern[-2:-1] == [item]:
                            has_pre = 1
                                #print(seq_pattern[-2:-1],[item],has_,has_pre)
                        
                        if((item == prefix[:-1] and prefix[-1:] == ')') or (item == prefix) ):
                            if prefix[-1:]==')' and(has_== 1 or has_pre == 1 or new == 1):
                                #print(item,prefix)
                                itemset_new[itemset_new.index(item)] = '_'
                                a=1
                                break
                            elif (has_== 0) :
                                itemset_new[itemset_new.index(item)] = '_'
                                a=1
                                break
                            else :
                                itemset_new.remove(item)
                        else:
                            itemset_new.remove(item)
            
                seq_new.append(itemset_new)
                seq_new = list(filter(None, seq_new))


            if seq_new != [] and seq_new != [['_']]:
                db_project.append(seq_new)
        #print(db_project)
        #print(seq_pattern,'out')


        if db_project !=[]:
            find_frequent_item(db_project,min_support,seq_pattern)
            
            #print(seq_pattern,'out')


        #seq_pattern output
        out = seq_pattern[:]
        for index,ele in enumerate(out) :
            if ele[-1:] ==')' :
                out[index-1] = '('+ out[index-1]
                if out[index-1][-1:] ==')':
                    out[index-1] = out[index-1][1:-1]
                    
                
                
        output = ' '.join(out)
        #print(output)
        
        
        writeTXT(output+'\n')
        
        seq_pattern.pop()
##    end2 = time.time()
##    elapsed2 = end2 - start2
##    print( "FOR(2) Time taken: ", elapsed2, "seconds.")
    release_list(db)
    return 


def writeTXT(t):
    f = open('out.txt','a')
    f.write(t)
    f.close()



def make_sequence(db):
    sequence_done = []
    sequence = []
    itemset = []
    items = defaultdict(lambda: 0)
    transactions_done = []
    i = 0
    for id_list in db:
        try:
            if db[i][0] == db[i+1][0]:
                if db[i][1] == db[i+1][1]: # same set
                    if not itemset : 
                        itemset.append(db[i][2])
                        itemset.append(db[i+1][2])                
                    else:
                        itemset.append(db[i+1][2])
                else: # same sequence
                    if not itemset :
                        itemset.append(db[i][2]) 
                    sequence.append(itemset)
                    itemset = []
            else:
                if not itemset :
                    itemset.append(db[i][2]) 
                sequence.append(itemset)
                itemset = []
                sequence_done.append(sequence)
                sequence = []
           
        except IndexError:
            if not itemset :
                itemset.append(db[i][2]) 
            sequence.append(itemset)
            itemset = []
            sequence_done.append(sequence)
            sequence = []
        i += 1
        
    return sequence_done

def release_list(d):
   del d[:]
   del d


if __name__ == '__main__':
    start = time.time()
    data= []
    filename1 = 'C50S10T2.5N10000.ascii'
    filename2 = 'abc copy.txt'
    with open(filename2) as f:
        for line in f:
            line = line.replace('\n','')
            line = line.split(' ')
            while '' in line: line.remove('')
            data.append(line)


    f = open('out.txt','w')
    f.write('')
    db = make_sequence(data)
    find_frequent_item(db,2,[])


    end = time.time()
    elapsed = end - start
    print( "Time taken: ", elapsed, "seconds.")

