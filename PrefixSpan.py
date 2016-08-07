from collections import defaultdict, namedtuple
import time

def find_frequent_item(db,min_supprot,prefix_object):
    prefix = defaultdict(lambda: 0)
    
    suff = ''.join(prefix_object.split()[-1:])
    
    db_new = []
    prefix_out = ''
    #print(prefix_object)     #calculate prefix 
    for sequence in db:
        seq_new = []
        a=0
        for itemset in sequence:
            itemset_new = itemset[:]
            itemset_tmp = []
            if ('_' in itemset or suff in itemset) and a == 0: #a :one seq only one change
                a=1
                for index,item in enumerate(reversed(itemset)):
                    item_new = str()
                    if item != '_' and item != suff and item[-1:] != ')'and itemset[index+1] == suff :
                        item_new = item + ')'
                        if item in itemset_new:
                                itemset_new.remove(item)
                        itemset_tmp.append(item_new)
                         
                    else:
                        break
                for item in reversed(itemset_tmp):        
                    itemset_new.append(item)
            seq_new.append(itemset_new)
        
        db_new.append(seq_new)
       
        flattened  = [val for sublist in seq_new for val in sublist]                
        for item in set(flattened):
            if item != '_':
                prefix[item]+=1
    prefix = dict((item, support) for item, support in list(prefix.items())
        if support >= min_supprot)
    print(prefix)
    release_list(db)
    
    db_new2 = []
    for sequence in db_new: #remove item <minsupport
        seq_new = []
        for itemset in sequence:
            itemset_new = itemset[:]
            for item in itemset:
                if item not in prefix:  
                    itemset_new.remove(item)      
                    #itemset[:]=(value for value in itemset if value != item)
            seq_new.append(itemset_new)
        db_new2.append(list(filter(None, seq_new)))
    
    release_list(db_new)
    for prefix_item in prefix:  #create object_DB
        #print('prefix_item',prefix_item)
        db_object= []
        prefix_out =  prefix_object  + prefix_item + ' '
        for seq in db_new2:
            seq_new = []
            a=0
            for itemset in seq:    
                itemset_new = itemset[:]
                if a==0:
                    for item in itemset:
                        if item == prefix_item:
                            itemset_new[itemset_new.index(item)] = '_'
                            a=1
                            break
                        else :
                            itemset_new.remove(item)
                seq_new.append(itemset_new)
                seq_new = list(filter(None, seq_new))
            #print(seq_new)
            if seq_new != [] and seq_new != [['_']]:
                db_object.append(seq_new)
                #print(seq_new)
        
        print(db_object)

        if db_object !=[]:
            find_frequent_item(db_object,min_supprot,prefix_out)
        
        
        
        #print(prefix_out)


        writeTXT(str(prefix_out)+'\n')
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
    filename2 = 'abc.txt'
    with open(filename2) as f:
        for line in f:
            line = line.replace('\n','')
            line = line.split(' ')
            while '' in line: line.remove('')
            data.append(line)


    f = open('out.txt','w')
    f.write('')
    db = make_sequence(data)
    find_frequent_item(db,2,'')
    
    
    end = time.time()
    elapsed = end - start
    print( "Time taken: ", elapsed, "seconds.")