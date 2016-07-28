from collections import defaultdict, namedtuple



def find_frequent_item(db,min_supprot):
    items = defaultdict(lambda: 0)
    for sequence in db:
        flattened  = [val for sublist in sequence for val in sublist]
        for item in set(flattened):
            items[item]+=1
    items = dict((item, support) for item, support in list(items.items())
        if support >= min_supprot)
    for sequence in db:
        for itemset in sequence:
            for item in itemset:
                if item not in items:
                    itemset.remove(item)
    return db

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

