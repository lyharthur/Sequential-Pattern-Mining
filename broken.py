from collections import defaultdict, namedtuple

def find_frequent_item(db,min_supprot,seq_pattern):
    prefix = defaultdict(lambda: 0)
    prefix_list = []
    last = seq_pattern[-1:]
    
    #print(db,'start')
    db_new = []
    prefix_out = ''
    
    for sequence in db: #calculate prefix 
        seq_new = []
        seq_done = defaultdict(lambda: 0)
        for itemset in sequence:           
            itemset_new = itemset[:]
            itemset_tmp = []
            set_l = len(itemset)
            has_ = 0
            for item in itemset:
                if item == '_':
                    has_ = 1
                for item1 in itemset:
                    itemnew = item + ')'
                    #print( item ,item1 ,last)
                    if ([item1] == last or item1 == '_' ) and prefix[itemnew] < min_supprot and seq_done[itemnew] == 0 and [item] != last:
                        prefix[itemnew]+=1
                        seq_done[itemnew] = 1
                        if prefix[itemnew] >= min_supprot:
                            prefix_list.append(itemnew)
                    elif seq_done[item] == 0 and has_ == 0 and prefix[item] < min_supprot:
                        prefix[item]+=1
                        seq_done[item] = 1
                        if prefix[item] >= min_supprot:
                            prefix_list.append(item)

    if '_' in prefix_list:
        prefix_list.remove('_')

    if '_)' in prefix_list:
        prefix_list.remove('_)')


#if prefix_list != []:
#       print(prefix_list,'plist')


    for prefix in prefix_list:  #create object_DB
        db_object= []
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
                db_object.append(seq_new)
                    #print(db_object)
        #print(seq_pattern ,'out')
        if db_object !=[]:
            find_frequent_item(db_object,min_supprot,seq_pattern)

        writeTXT(str(seq_pattern)+'\n')

        seq_pattern.pop()
        
        
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
