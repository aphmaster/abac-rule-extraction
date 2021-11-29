
import numpy as np
from collections import Counter


def get_entries_freqs(entries):
    #entries is a list of dataset entries
    #Returns a list of collcounters: attidx_to_collcounter #TODO: como es la mejor forma de explicarlo
    
    num_atts = len(entries[0])
    attidx_to_collcounter = []
    entries_np = np.array(entries)
    
    for attidx in range(num_atts):
        attidx_to_collcounter.append(Counter(entries_np[:,attidx]))
    
    return attidx_to_collcounter


def to_tuple_format(entries):
    #Transforms each entry in entries to a list of tuples (att_idx, att_val)
    
    t_list = []
    num_atts = len(entries[0])
    
    for entry in entries:
        t = []
        for att_idx in range(num_atts):
            att_val = entry[att_idx]
            t.append((att_idx,att_val))
        t_list.append(tuple(t))
        
    return t_list
        

def get_pattern_indexes(entries, f_pattern_dict):

    indexes = set()
    
    for e_idx,entry in enumerate(entries):
        flag = True

        for att_idx,vals in f_pattern_dict.items():
            if not entry[att_idx] in vals:
                flag = False

        if flag: indexes.add(e_idx)

    return indexes


def get_false_neg(pos_entries, policy):
    #TODO revisar
    false_negs = []
    
    for entry in pos_entries:
        
        #Check access for each rule
        denies_count = 0
        
        for rule in policy:
            
            res = True
            for att_idx in rule.keys():

                if not entry[att_idx] in rule[att_idx]:
                    res = False
                    break
            
            if res == False:
                denies_count += 1
                
        if denies_count == len(policy):
            false_negs.append(entry)
            
    return false_negs


def evaluate_policy(policy, pos_entries, neg_entries=None):
    #TODO revisar
    false_negs = get_false_neg(pos_entries, policy)
    FN = len(false_negs)
    TP = len(pos_entries) - FN
    #false_pos = get_false_pos(neg_entries, policy)
    #FP = len(false_pos)
    FP = 0
    #TN = len(neg_entries) - FP
    TN = 0
    
    precision = TP / (TP + FP)
    
    recall = TP / (TP + FN)
    
    fscore = 2*(precision*recall)/(precision+recall)
    
    return false_negs,None,precision,recall,fscore
    
    
def compute_wsc(policy):
    wsc = 0
    for rule in policy:
        for lst_vals in rule.values():
            wsc += len(lst_vals)

    return wsc
