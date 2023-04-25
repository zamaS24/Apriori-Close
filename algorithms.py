from itertools import combinations
import pandas as pd
import numpy as np


class Algorithm: 
    

    def load_data(file_path):
        data = []
        with open(file_path, 'r') as f:
            for line in f:
                transaction = line.strip().split(',')
                data.append(set(transaction))
        return data #return a list of sets of transactions

    # This function counts the number of times each item appears in the dataset:
    def get_item_counts(data):
        item_counts = {}    
        for transaction in data:
            for item in transaction:
                if item in item_counts:
                    item_counts[item] += 1
                else:
                    item_counts[item] = 1
        return item_counts  # returns dictionnary containing the count of each item in the dataset.

    # This function generates all frequent itemsets in the dataset that have a support greater than 
    # or equal to the specified minimum support:
    def get_frequent_itemsets(data, min_support):
        item_counts = Algorithm.get_item_counts(data)
        num_transactions = len(data)
        min_support_count = num_transactions * min_support

        # Creer l'ensemble de 1-Frequent Itemsets
        frequent_itemsets = [frozenset({item}) for item, count in item_counts.items() if count >= min_support_count]
        
        k = 2
        while frequent_itemsets:
            itemsets = set()
            for i, itemset1 in enumerate(frequent_itemsets):
                for itemset2 in frequent_itemsets[i+1:]:
                    new_itemset = itemset1.union(itemset2)
                    if len(new_itemset) == k:
                        itemsets.add(new_itemset)
            frequent_itemsets_k = set()
            for itemset in itemsets:
                itemset_count = sum(1 for transaction in data if itemset.issubset(transaction))
                if itemset_count >= min_support_count:
                    frequent_itemsets_k.add(itemset)
            if not frequent_itemsets_k:
                break
            frequent_itemsets.extend(frequent_itemsets_k)
            k += 1
            # The loop continues until there are no more frequent itemsets left to generate. 
            # print('the list of frequent itemsets is: ', frequent_itemsets)
        return frequent_itemsets

    # This function generates all association rules with a confidence greater than or equal to the specified minimum confidence:
    def get_association_rules(frequent_itemsets, min_confidence, data):
        num_transactions = len(data)
        association_rules = []
        for itemset in frequent_itemsets:
            if len(itemset) < 2:
                continue
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent

                    antecedent_support = sum(1 for transaction in data if antecedent.issubset(transaction)) / num_transactions
                    consequent_support = sum(1 for transaction in data if consequent.issubset(transaction)) / num_transactions

                    itemset_support = sum(1 for transaction in data if itemset.issubset(transaction)) / num_transactions

                    confidence = itemset_support / antecedent_support
                    lift = confidence / consequent_support
                    
                    if confidence >= min_confidence:
                        association_rules.append((antecedent, consequent, confidence, lift))
        return association_rules

    def get_closed_itemsets(data, min_support):
        # Generate frequent itemsets
        frequent_itemsets = Algorithm.get_frequent_itemsets(data, min_support)
        
        # Initialize dictionary to keep track of support counts for each itemset
        itemset_support_counts = {}
        for transaction in data:
            for itemset in frequent_itemsets:
                if itemset.issubset(transaction):
                    if itemset not in itemset_support_counts:
                        itemset_support_counts[itemset] = 1
                    else:
                        itemset_support_counts[itemset] += 1
        
        # Initialize list to store closed itemsets
        closed_itemsets = []
        
        # Iterate over frequent itemsets
        for itemset1 in frequent_itemsets:
            # Flag to indicate whether itemset1 is closed
            is_closed = True
            
            # a closed itemset is a subset of items that appears frequently in a dataset, 
            # and no superset of this itemset has the same support
            
            # Iterate over remaining frequent itemsets
            for itemset2 in frequent_itemsets:
                # Check if itemset2 is a superset of itemset1
                if itemset1.issubset(itemset2):
                    # Check if itemset1 and itemset2 have the same support count
                    if itemset_support_counts[itemset1] == itemset_support_counts[itemset2]:
                        # If itemset2 is not the same as itemset1, itemset1 is not closed
                        if itemset1 != itemset2:
                            is_closed = False
                            break
            
            # If itemset1 is closed, add it to the list of closed itemsets
            if is_closed:
                closed_itemsets.append(itemset1)
        
        return closed_itemsets

    def Apriori(data, minsup, min_confidence, contribution=False, closed=False): 
        
        min_support = minsup
        frequent_itemsets = Algorithm.get_frequent_itemsets(data, min_support)
        
        if closed:
            frequent_itemsets = Algorithm.get_closed_itemsets(data, min_support)
        association_rules = Algorithm.get_association_rules(frequent_itemsets, min_confidence, data)

        if (contribution):
            min_support = 0.10
            frequent_itemsets = Algorithm.get_frequent_itemsets(data, min_support)
            while (len(frequent_itemsets)>len(Algorithm.get_item_counts(data).items())/2):
                min_support += 0.05

                frequent_itemsets = Algorithm.get_frequent_itemsets(data, min_support)
                if closed:
                    frequent_itemsets = Algorithm.get_closed_itemsets(data, min_support)
                
                association_rules = Algorithm.get_association_rules(frequent_itemsets, min_confidence, data)
        return association_rules, frequent_itemsets




