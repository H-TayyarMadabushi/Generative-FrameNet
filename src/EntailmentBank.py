import re
import os
import csv
import json
from tqdm import tqdm
from rake_nltk import Rake




class EntailmentBank :
    def __init__( self, data_location='data', task='task_2', k=30 ) :
        self.train_data = self._load( os.path.join( data_location, task, 'train.jsonl' ) )
        self.dev_data   = self._load( os.path.join( data_location, task, 'dev.jsonl' ) )
        self.test_data  = self._load( os.path.join( data_location, task, 'test.jsonl' ) )
        self.split_to_data = {
            'train' : self.train_data,
            'test'  : self.test_data ,
            'dev'   : self.dev_data,
            }
        self.get_all_facts()
        self.k = k
        return

    def _load( self, file_path ) :
        data = list()
        with open( file_path ) as fh :
            for elem in fh :
                elem = json.loads( elem ) 
                elem['context'] = [ i.rstrip().lstrip() for i in re.split( r'sent\d+:\s*', elem['context'] ) if i != '' ]
                data.append( elem )
        return data

    def get_all_facts( self ) :
        self.facts = set()
        for datasplit in [ self.train_data, self.dev_data, self.test_data ] :
            for elem in datasplit :
                self.facts = self.facts.union( set( elem[ 'context'] ) )
                
    def get_data_facts( self, data ) :
        self.data_facts = set()
        for elem in data :
            self.data_facts = self.data_facts.union( set( elem[ 'context'] ) )
        return 

    def filter_data( self, data, min_inferences=6, max_inferences=20 ) :
        y = [ (i, len( data[i]['context'] )) for i in range( len( data ) ) ]
        y.sort( key=lambda x:x[1] )
        y.reverse()

        from collections import defaultdict
        counter = defaultdict( int )
        for elem in y :
            counter[ elem[1] ] += 1

        print( "Limiting data by min and max inferences steps" )
        y = [ i for i in y if i[1] >= min_inferences and i[1] <= max_inferences  ] 
        new_data = list()
        for elem in y[:30] : 
            new_data.append( data[elem[0]] )
        return [ new_data, 'min_{}_max_{}'.format( min_inferences, max_inferences ) ]

    def get_search_terms_rake( self, question ) :
        rake = Rake()
        rake.extract_keywords_from_text( question )
        keywords = rake.get_ranked_phrases()
        return keywords[:10]

    def search_facts( self, keywords ) :
        retrieved_facts = list()
        for keyword in keywords :
            this_keyword_facts = 0
            for factoid in self.data_facts :
                if keyword.lower() in factoid.lower() :
                    retrieved_facts.append( factoid )
                    this_keyword_facts += 1
                    if this_keyword_facts > round( self.k / len( keywords ) ) :
                        break

        uniq_facts      = list()
        for fact in retrieved_facts :
            if not fact in uniq_facts :
                uniq_facts.append( fact )
        retrieved_facts = uniq_facts
                    
        return retrieved_facts

    def onerecallatk( self, retrieved_facts, gold_facts ) :
        # Recall@k = (# of recommended items @k that are relevant) / (total # of relevant items)
        gold_facts = [ i.lower().lstrip().rstrip() for i in gold_facts ]
        if self.k < len( retrieved_facts ) : 
            retrieved_facts = retrieved_facts[:self.k]
        num_relevant = 0
        for retrieved_fact in retrieved_facts :
            if retrieved_fact.lower().lstrip().rstrip() in gold_facts :
                num_relevant += 1
        return num_relevant / len( gold_facts )
    
    def oneprecisionatk( self, retrieved_facts, gold_facts ) :
        #Precision@k = (# of recommended items @k that are relevant) / (# of recommended items @k)
        gold_facts = [ i.lower().lstrip().rstrip() for i in gold_facts ]
        if self.k < len( retrieved_facts ) : 
            retrieved_facts = retrieved_facts[:self.k]
        num_relevant = 0
        for retrieved_fact in retrieved_facts :
            if retrieved_fact.lower().lstrip().rstrip() in gold_facts :
                num_relevant += 1
        return num_relevant / self.k

    def verify_search( self, split ) :
        data = split
        if type( split ) == str :
            data = self.split_to_data[ split ]
        else :
            split = "Custom Split"
        for question in tqdm( data, desc='Verifying search' ) :
            for fact in question['context']  :
                assert fact in self.facts
        print( "Verified that all facts in {} are in the corpus.".format( split ) )
        

    def calculate_baseline( self, split, verify=False ) :
        data = split
        if type( split ) == str :
            data =  self.split_to_data[ split ]
        self.get_data_facts( data )
        if verify  :
            self.verify_search( data )
        recall_total    = 0
        precision_total = 0 
        for question in data :
            search_terms    = self.get_search_terms_rake( question['question'] )
            retrieved_facts = self.search_facts( search_terms )
            recall_total   += self.onerecallatk   ( retrieved_facts, question['context'] )
            precision_total+= self.oneprecisionatk( retrieved_facts, question['context'] )
        recall = float( recall_total / len( data ) )
        # print( "Baseline Recall@{}".format( self.k )   , recall )
        # print( "Baseline Precision@{}".format( self.k ), precision_total / len( data ) )
        return recall

        
if __name__ == '__main__' :
    for k in [ 30, 100, 1000, 10000 ] : 
        entailmentbank = EntailmentBank( task='task_1', k=k)
        import pdb; pdb.set_trace()
        entailmentbank.calculate_baseline( 'train' ) 
