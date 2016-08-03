from collections import defaultdict, namedtuple

def find_frequent_item(db,min_supprot,prefix_object):
    prefix = defaultdict(lambda: 0)
    prefix_list = []
    last = ''.join(prefix_object.split()[-1:])
    print(db,'start')
    db_new = []
    prefix_out = ''
    
    for sequence in db: #calculate prefix 
        seq_new = []
        seq_done = defaultdict(lambda: 0)
        
        for itemset in sequence:           
            itemset_new = itemset[:]
            itemset_tmp = []
            set_flag = 0
            has_ = 0
            has_last = 0     
            for item in itemset:
                

                                
                if item == '_' or(item[:-1] == last and  len(item) > 1)or(item == last) :
                    has_ = 1
                print(item ,last,has_ )    
                if item != '_' : #and prefix[item] < min_supprot
                    
                    if item[-1:] == ')' and has_ == 0 and seq_done[item[:-1]] == 0 :    #hasnt '_' or last ,=>no ')'
                        prefix[item[:-1]]+=1  #rm')'
                        seq_done[item[:-1]] = 1
                        if prefix[item[:-1]] >= min_supprot:
                            prefix_list.append(item[:-1])
                            
                    if seq_done[item] == 0 and has_==0:
                        prefix[item]+=1   
                        seq_done[item] = 1
                        if prefix[item] >= min_supprot:
                            prefix_list.append(item)
                                                        
                    if has_ == 1 and seq_done[item[:-1]] == 0 :    
                        prefix[item[:-1]]+=1  #rm')'
                        seq_done[item[:-1]] = 1
                        if prefix[item[:-1]] >= min_supprot:
                            prefix_list.append(item[:-1])           
                    



                    
                    
                if set_flag == 1 and item[-1:] != ')' :
                    item_new = item + ')'
                    if item in itemset_new:
                            itemset_new.remove(item)
                    itemset_tmp.append(item_new)
                if item != '_' and item != last  :
                    set_flag = 1                       
                    
                    
            for item in itemset_tmp:        
                    itemset_new.append(item)
                    
            seq_new.append(itemset_new)
        db_new.append(seq_new)   
    
    #print(db_new ,'mid')
    if prefix_list != []:
        print(prefix_list,'plist')


        
    for prefix in prefix_list:  #create object_DB
        db_object= []
        prefix_out =  prefix_object  + prefix + ' '
        for seq in db_new:
            seq_new = []
            a=0
            for itemset in seq:    
                itemset_new = itemset[:]
                if a==0:
                    for item in itemset:
                        
                        if (item[:-1]== prefix and  len(item) > 1)or(item== prefix) :
                            
                            itemset_new[itemset_new.index(item)] = '_'
                            a=1
                            break
                        else:
                            itemset_new.remove(item)
                seq_new.append(itemset_new)
                seq_new = list(filter(None, seq_new))

            if seq_new != [] and seq_new != [['_']]:
                db_object.append(seq_new)
        #print(db_object,'final')
        print(prefix_out,'output')
        if db_object !=[]:
            
            find_frequent_item(db_object,min_supprot,prefix_out)
        
        
    
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
