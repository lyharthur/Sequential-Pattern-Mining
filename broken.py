from collections import defaultdict, namedtuple
import time

def find_frequent_item(db,min_support,seq_pattern):
    
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
            has_last = 0
            for index,item in enumerate(itemset):
                if [item] == last:
                    has_last =1
                if item == '_':
                    has_ = 1          
                elif item != '_' :
                    #for item1 in itemset[:index+1]:
                    itemnew = item + ')'
                    #print('lsitfor', item  ,last , index)
                    if (has_last == 1 or has_ == 1 ) and prefix[itemnew] < min_support and seq_done[itemnew] == 0 and [item] != last:
                        prefix[itemnew]+=1  # has )
                        seq_done[itemnew] = 1
                        if prefix[itemnew] >= min_support:
                            prefix_list.append(itemnew)
                    elif seq_done[item] == 0 and has_ == 0 and prefix[item] < min_support:
                        prefix[item]+=1
                        seq_done[item] = 1
                        if prefix[item] >= min_support:
                            prefix_list.append(item)



    #if prefix_list != []:
    #    print(prefix_list,'plist')

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
                        if prefix[-1:]==')':
                            #print(item,prefix)
                            if item == '_' :
                                has_ = 1
                            if seq_pattern[-2:-1] == [item]:
                                has_pre = 1
                            #print(has_,has_pre)
                            
                            if ((item == prefix[:-1] )or(item == prefix) ) and (has_== 1 or has_pre == 1 or new == 1):
                                itemset_new[itemset_new.index(item)] = '_'                           
                                a=1
                                break
                            else :
                                itemset_new.remove(item)
                                
                        else:
                            #print(item,prefix)
                            if item == '_' :
                                has_ = 1
                            if seq_pattern[-2:-1] == [item]:
                                has_pre = 1
                            #print(has_,has_pre)
                            if ((item == prefix[:-1] )or(item == prefix)) and (has_== 0) :
                                itemset_new[itemset_new.index(item)] = '_'
                                
                                a=1
                                break
                            else :
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
        writeTXT(str(seq_pattern)+'\n')
        
        seq_pattern.pop()
##    end2 = time.time()
##    elapsed2 = end2 - start2
##    print( "FOR(2) Time taken: ", elapsed2, "seconds.")
        
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
