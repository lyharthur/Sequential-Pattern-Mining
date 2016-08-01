from collections import defaultdict, namedtuple



def find_frequent_item(db,min_supprot,prefix_object):
    prefix = defaultdict(lambda: 0)
    db_new = []
    prefix_out = ''
    #print(prefix_object)
    for sequence in db:
        flattened  = [val for sublist in sequence for val in sublist]
        for item in set(flattened):
            if item != '_':
                prefix[item]+=1
    prefix = dict((item, support) for item, support in list(prefix.items())
        if support >= min_supprot)
    #print(prefix)
    for sequence in db:
        for itemset in sequence:
            for item in itemset:
                if item not in prefix:
                    itemset.remove(item)
        db_new.append(list(filter(None, sequence)))
        
    for prefix_item in prefix:    
        db_object= []
        prefix_out =  prefix_object + prefix_item

        for seq in db_new:
            seq_new = []
            a=0
            for itemset in seq:    
                itemset_n = itemset[:]
                if a==0:
                    for item in itemset:
                        if item == prefix_item:
                            itemset_n[itemset_n.index(item)] = '_'
                            a=1
                            break
                        else :
                            itemset_n.remove(item)
                seq_new.append(itemset_n)
                seq_new = list(filter(None, seq_new))
            #print(seq_new)
            if seq_new != [] and seq_new != [['_']]:
                db_object.append(seq_new)
                #print(seq_new)
        print(db_object)
        
        if db_object !=[]: 
            find_frequent_item(db_object,min_supprot,prefix_out)
        print(prefix_out)
    return 0


def writeTXT(t):
    f = open('out.txt','w')
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

