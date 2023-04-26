from itertools import combinations

class Algorithm: 
    

    def load_data(file_path):
        data = []
        with open(file_path, 'r') as f:
            for line in f:
                transaction = line.strip().split(',')
                data.append(set(transaction))
        # retourner la liste des transactions. et une transaction est un ensemble d'items
        return data 

    def get_item_counts(data):
        item_counts = {}    
        for transaction in data:
            for item in transaction:
                if item in item_counts:
                    item_counts[item] += 1
                else:
                    item_counts[item] = 1
        #retourner un dictionnaire contenant le compte de tous les items
        return item_counts  

    #Fonction pour implementer Apriori
    def get_frequent_itemsets(data, min_support):
        item_counts = Algorithm.get_item_counts(data)
        num_transactions = len(data)
        min_support_count = num_transactions * min_support

        # Creer l'ensemble des 1-itemsets Frequents
        frequent_itemsets = [frozenset({item}) for item, count in item_counts.items() if count >= min_support_count]


        # Creer les K itemsets frequents k=2...
        k = 2
        while frequent_itemsets:

            #creer d'abord les K itemsets
            itemsets = set()
            for i, itemset1 in enumerate(frequent_itemsets):
                for itemset2 in frequent_itemsets[i+1:]:
                    new_itemset = itemset1.union(itemset2)
                    if len(new_itemset) == k:
                        itemsets.add(new_itemset)

            # creer les K itemsets frequents seulement
            frequent_itemsets_k = set()
            for itemset in itemsets:
                itemset_count = sum(1 for transaction in data if itemset.issubset(transaction))
                if itemset_count >= min_support_count:
                    frequent_itemsets_k.add(itemset)
            
            # Si il y a pas de K itemsets frequents alors on sort de la boucle
            if not frequent_itemsets_k:
                break

            # Ajouter la liste des K_itemsets à la liste globale des Itemsets frequents
            frequent_itemsets.extend(frequent_itemsets_k)
            k += 1
            

        # Retourner la liste finale des itemsets frequents   
        return frequent_itemsets
    
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
 
    def Apriori(data, minsup, min_confidence, contribution=False): 
        
        min_support = minsup
        frequent_itemsets = Algorithm.get_frequent_itemsets(data, min_support)
        
        
        association_rules = Algorithm.get_association_rules(frequent_itemsets, min_confidence, data)

        if (contribution):
            min_support = 0.10
            frequent_itemsets = Algorithm.get_frequent_itemsets(data, min_support)
            while (len(frequent_itemsets)>len(Algorithm.get_item_counts(data).items())/2):
                min_support += 0.05

                frequent_itemsets = Algorithm.get_frequent_itemsets(data, min_support)       
                association_rules = Algorithm.get_association_rules(frequent_itemsets, min_confidence, data)
        return association_rules, frequent_itemsets

    # Fonction pour implementer Close
    def get_closed_itemsets(data, min_support):
        frequent_closed_itemsets = []

        item_counts = Algorithm.get_item_counts(data)
        num_transactions = len(data)
        min_support_count = num_transactions * min_support

        # Creer l'ensemble des 1-itemsets Frequents
        frequent_itemsets = [frozenset({item}) for item, count in item_counts.items() if count >= min_support_count]

        # generer la fermeture pour les 1 itemsets
        for itemset in frequent_itemsets: 
            #initialiser la fermeture de l'itemset à tous les items
            close=set()   
            for item ,count in item_counts.items():                      
                close.add(item)
            
            #Enlever les items qui ne figure pas dans une certaine transaction avec l'itemset
            for transaction in data: 
                for item2 in close.copy(): 
                    if itemset.issubset(transaction) and not {item2}.issubset(transaction):   
                        if item2 in close:
                            close.remove(item2)
                                    
            frequent_closed_itemsets.append((itemset, close))



        # Creer les K itemsets frequents k=2...
        k = 2
        while frequent_itemsets:

            #creer d'abord les K itemsets
            itemsets = set()
            for i, itemset1 in enumerate(frequent_itemsets):
                for itemset2 in frequent_itemsets[i+1:]:
                    new_itemset = itemset1.union(itemset2)
                    if len(new_itemset) == k:
                        itemsets.add(new_itemset)

            # creer les K itemsets frequents seulement
            frequent_itemsets_k = set()
            for itemset in itemsets:
                itemset_count = sum(1 for transaction in data if itemset.issubset(transaction))
                if itemset_count >= min_support_count:
                    frequent_itemsets_k.add(itemset)
            
            # Si il y a pas de K itemsets frequents alors on sort de la boucle
            if not frequent_itemsets_k:
                break
            else:
                #generer la fermuture de chaque K_itemset et l'ajouter à la liste
                for itemset in frequent_itemsets_k: 
                    close=set()   
                    for item ,count in item_counts.items():                      
                        close.add(item)
                    
                    for transaction in data: 
                        for item2 in close.copy(): 
                            if itemset.issubset(transaction) and not {item2}.issubset(transaction):   
                                if item2 in close:
                                    close.remove(item2)
                                            
                    frequent_closed_itemsets.append((itemset, close))


            # Ajouter la liste des K_itemsets à la liste globale des Itemsets frequents
            frequent_itemsets.extend(frequent_itemsets_k)
            k += 1
            

        # Retourner la liste finale des itemsets frequents   
        return frequent_closed_itemsets
 
    def get_closed_association_rules(frequent_closed_itemsets, min_confidence, data):
        num_transactions = len(data)
        association_rules = []
        for itemset, closer in frequent_closed_itemsets:
            if set(itemset) == closer: 
                continue

            antecedent = set(itemset)
            consequent = closer - antecedent

            antecedent_support = sum(1 for transaction in data if antecedent.issubset(transaction)) / num_transactions
            consequent_support = sum(1 for transaction in data if consequent.issubset(transaction)) / num_transactions

            full_itemset = set(itemset).union(closer)
            itemset_support = sum(1 for transaction in data if full_itemset.issubset(transaction)) / num_transactions

            confidence = itemset_support / antecedent_support
            lift = confidence / consequent_support
            
            if confidence >= min_confidence:
                association_rules.append((antecedent, consequent, confidence, lift))
        return association_rules

    def Close(data, min_support):
        item_closed = Algorithm.get_closed_itemsets(data,min_support)
        association_rules = Algorithm.get_closed_association_rules(item_closed, 0.5, data)

        return association_rules, item_closed



