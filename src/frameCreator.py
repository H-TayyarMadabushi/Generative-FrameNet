import re
import os
import csv
import sys
import json
import copy
import time
import torch
import openai
import pickle
import numpy as np

from tqdm                   import tqdm
from pprint                 import pprint
from datasets               import load_dataset
from collections            import defaultdict
from nltk.corpus            import framenet as fn
from TestTemplates          import TestTemplates
from EntailmentBank         import EntailmentBank
from sklearn.metrics        import classification_report
from sentence_transformers  import SentenceTransformer, util

sys.stdout.flush()

class FrameCreator :
 
    def __init__( self, data, data_version, model_used, output_location, openai_completion_style, template_style, question_column='question', cot_column='cot', verbose=True, allow_cache=True, force_framenet=False, entailmentbank=None ) : 

        self.model                   = model_used
        self.data_version            = data_version
        self.output_location         = output_location
        self.openai_completion_style = openai_completion_style
        self.template_style          = template_style
        self.question_column         = question_column
        self.allow_cache             = allow_cache
        self.cot_column              = cot_column
        self.verbose                 = verbose
        self.data                    = data
        self.force_framenet          = force_framenet
        self.entailmentbank          = entailmentbank
        
        self._load_openai_key()

        self.sentence_transformer_model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

        self.custom_frames_file = 'CustomFrames.pk'
        self.frames = set()
        if self.force_framenet : 
            x = fn.frames()
            y = [ i['name'] for i in x ]
            y.sort()
            self.frames = y
        else :
            ## Load the frames we've constructed
            if self.verbose :
                print( "Loading Frames we've created so far ... " )
                if os.path.exists( self.custom_frames_file ) :
                    with open( self.custom_frames_file, 'rb' ) as fh :
                        self.frames = pickle.load( fh ) 
                    
        tt = TestTemplates()
        self.test_templates = tt.test_templates
        
        return 

    def _save_frames( self ) :
        with open( self.custom_frames_file, 'wb' ) as fh :
            pickle.dump( self.frames, fh )
        return 

    def _get_cache_path( self, content_type ) :
        if not content_type is None:
            print( "WARNING: OLD CACHE STYLE" ) 
            return os.path.join( self.output_location, self.model, self.template_style, content_type )
        else :
            return os.path.join( self.output_location, self.model, self.template_style )

    
    def _load_openai_key( self ) :
        with open( '.key' ) as fh :
            data = fh.readlines()
            self.org_key, self.user_key = data[0].split( ',' )
        openai.organization = self.org_key
        openai.api_key = self.user_key
        return

    def _cached_get( self, content_type, example_id, prompt ) :
        cache_path      =  self._get_cache_path(None)
        # cache_file      =  '{}.pk3'.format( example_id )
        cache_file = 'combined_cache.pk'
        cache_file_path = os.path.join( cache_path, cache_file )
        cache_data = dict()
        if os.path.exists( cache_file_path ) and self.allow_cache :
            with open( cache_file_path, 'rb' ) as fh :
                cache_data = pickle.load( fh )
                if prompt in cache_data.keys() :
                    if self.verbose :
                        print( "Cache Get GPT" ) 
                    return cache_data[ prompt ]
        if not os.path.exists( cache_path ) :
            os.makedirs( cache_path )

        if self.verbose : 
            print( "GPT hit" )
        if self.openai_completion_style == 'ChatCompletion' :
            error = True
            tries = 5
            while error and tries >= 0 :
                try : 
                    chat_completion = openai.ChatCompletion.create(
                        model=self.model,
                        temperature=0,
                        messages=[{"role": "user", "content": prompt}]
                    )
                except :
                    if self.verbose :
                        print( "OpenAI Error - will sleep and try again" )
                    time.sleep( 5 * ( 5 - tries ) )
                    tries -= 1
                    continue
                error = False
                break
            response = chat_completion[ 'choices' ][0].to_dict_recursive()
            response[ 'prompt' ] = prompt
            response[ 'answer' ] = response['message']['content']
        elif self.openai_completion_style == 'Completion' :
            completion = openai.Completion.create(
                model=self.model,
                temperature=0,
                prompt=prompt,
            )
            response = completion[ 'choices' ][0].to_dict_recursive()
            response[ 'prompt' ] = prompt
            response[ 'answer' ] = response['text']


        cache_data[ prompt ] = response
        with open( cache_file_path, 'wb' ) as fh :
            pickle.dump( cache_data, fh )
            
        return response

    
    def _generate_prompt( self, content, content_type, other_content=None, other_content2=None ) :
        template  = self.test_templates[ self.template_style ][ content_type ]
        prompt    = template[ 'prompt']
        to_use    = template[ 'fields']
        sources   = [ ', '.join( self.frames ), content, other_content, other_content2 ]
        data_list = list()
        for i in range( len( sources ) ) :
            use_this = None
            try :
                use_this = int( to_use[ i ] ) 
            except IndexError :
                pass
            if not use_this is None and use_this == 1 :
                data_list.append( sources[ i ] )

        prompt   = prompt.format( *data_list )
        
        return prompt
        
    def _clean_response_json( self, response ) :
        content    = response['message']['content']
        content    = content.replace( '```json', '' )
        content    = content.replace( '```', '' )
        return content
    
    def _clean_response_list( self, response ) :
        content    = [ i.rstrip().lstrip() for i in response['message']['content'].lstrip().rstrip().split( ',' ) if i != '' ] 
        return content

    
    def _get_sentencebert_frames( self, gen_frames ) :
        relevant_frames = list()
        if len( self.frames ) == 0 :
            return [[] for _ in gen_frames]
        for gen_frame in gen_frames :
            this_rel_frames   = list()
            frame_list        = list( self.frames ) 
            query_embedding   = self.sentence_transformer_model.encode( gen_frame )
            passage_embedding = self.sentence_transformer_model.encode( [ i.replace( '_', ' ' ) for i in frame_list ] )

            sims    = util.dot_score(query_embedding, passage_embedding)
            pick    = 5 if len( self.frames ) > 5 else len( self.frames )
            indices = torch.topk( sims, pick ).indices.tolist()[0]
            for i in indices : 
                this_rel_frames.append( frame_list[ i ] )
            this_rel_frames = list( set( this_rel_frames ) )
            relevant_frames.append( this_rel_frames )
        return relevant_frames
        
    
    def generate_frames( self, limit=None ) :
        cache_string = "{}_{}_{}_{}_{}.pk3".format( self.data_version, self.model, str( limit ), self.template_style, str( self.force_framenet ) )
        cache_path = self._get_cache_path( cache_string ) 

        self.framed_questions = list()
        if os.path.exists( cache_path ) and self.allow_cache :
            with open( cache_path, 'rb' ) as fh :
                self.framed_questions = pickle.load( fh )
            if self.verbose :
                print( "Loaded from cache" ) 
            return 

        for example_id, elem in enumerate( self.data ) :
            if not limit is None and example_id > limit :
                break
            # ['id', 'ref_id', 'question', 'type', 'choices', 'context', 'cot', 'answer', 'generated_cot', 'feedback']
            question = elem[ self.question_column]
            cot      = elem[ self.cot_column     ]
            one_question = {
                'question' : { 'text' : question, 'frames' : None }, 
                'cot' : list()
            }

            if self.verbose : 
                print( "*" * 100) 
                print( "Question: ", question )
                print( "*" * 100) 
                print( "CoT:\n", "\n".join( cot ) )
                print( "*" * 100) 
                print( "*" * 100)
                

            question_prompt = self._generate_prompt( question, 'explore'  )
            response        = self._cached_get( 'explore', example_id, question_prompt )
            frames          = self._clean_response_list( response ) 

            relevant_frames = self._get_sentencebert_frames( frames )
            relevant_frames = relevant_frames[0]
            use_new_frames  = True
            if len( relevant_frames ) > 0 :
                relevant_frames.sort()
                check_prompt    = self._generate_prompt( question, 'frame_check_question', frames[0], ', '.join( relevant_frames ) )
                response        = self._cached_get( 'frame_check_question', example_id, check_prompt )
                response        = response['message']['content']
                if response == 'True' :
                    use_new_frames = True
                elif response == 'False' :
                    use_new_frames = False
                else :
                    raise Exception( "WARNING: Error with GPT response" )

            original_frames = frames
            if use_new_frames : 
                self.frames = self.frames.union( frames )
                self._save_frames()
            else :
                frames = [ relevant_frames[0] ]
                
            one_question[ 'question' ][ 'frames' ] = frames

            if self.verbose : 
                print( one_question )

            if self.verbose : 
                print( "*" * 100) 
                print( "Question: ", question )
                print( "Frames:", original_frames )
                print( "Use New:", use_new_frames )
                print_frames = ", ".join( frames ) 
                print( "Frames: ", print_frames )
                print( "*" * 100)
                
            
            for cot_no, one_cot in enumerate( cot ) :
                one_cot_details = {
                    'fact'   : one_cot,
                    'frames' : None
                }
                cot_prompt = self._generate_prompt( one_cot, 'explore_fact', question  )
                number     = str( example_id ) + str( cot_no )
                response   = self._cached_get( 'explore_fact', number, cot_prompt )

                frames          = self._clean_response_list( response ) 
                relevant_frames = self._get_sentencebert_frames( frames )

                picked_frames   = list()
                for i, relevant_frame_set in enumerate( relevant_frames ) :
                    relevant_frame_set.sort()
                    check_prompt    = self._generate_prompt( question, 'frame_check_fact', frames[0], ', '.join( relevant_frame_set ) )
                    response        = self._cached_get( 'frame_check_fact', example_id, check_prompt )
                    response        = response['message']['content']
                    use_new_frames  = None
                    if response == 'True' :
                        use_new_frames = True
                    elif response == 'False' :
                        use_new_frames = False
                    else :
                        raise Exception( "WARNING: Error with GPT response" )
                    
                    if use_new_frames : 
                        self.frames = self.frames.union( [ frames[i] ] )
                        self._save_frames()
                        picked_frames += [ frames[i] ]
                    else :
                        picked_frames += relevant_frame_set[:2]
                        
                one_cot_details[ 'frames' ] = picked_frames
                if self.verbose : 
                    print( "*" * 100) 
                    print( "CoT:", one_cot )
                    print( "*" * 100)
                    print_frames = frames
                    if type( print_frames[0] ) == dict :
                        print_frames = [ i['frame'] for i in frames ]
                    print( "Frames: ", print_frames  )
                    print( "Picked: ", picked_frames ) 
                    print( "*" * 100)
                one_question[ 'cot' ].append( one_cot_details )

            ## End of for cot
            self.framed_questions.append( one_question )
            

        ## End of question loop
        with open( cache_path, 'wb' ) as fh :
            pickle.dump( self.framed_questions, fh )
            if self.verbose:
                print( "Written to cache" ) 
        return

    def index_frames( self ) :
        self.frame_index = defaultdict( list )
        for question_data in self.framed_questions :
            for cot in question_data[ 'cot' ] :
                for frame in cot['frames'] :
                    self.frame_index[ frame ].append( cot['fact'] )
        return

    def frame_based_retrive( self, frames ) :
        all_frames = list()
        for frame_set in frames :
            all_frames += frame_set
        all_frames = list( set( all_frames ) ) 
        retrieved_facts = list()
        for frame in all_frames :
            retrieved_facts += list( set( self.frame_index[ frame ] ) )
        uniq_facts      = list()
        for fact in retrieved_facts :
            if not fact in uniq_facts :
                uniq_facts.append( fact )
        retrieved_facts = uniq_facts

        return retrieved_facts

    
    def search_rag( self )  :
        recall_total = 0
        for question_data in self.framed_questions :
            gold_facts       = [ i['fact'] for i in question_data['cot'] ]
            search_prompt    = self._generate_prompt( question_data['question']['text'], 'search_terms'  )
            response         = self._cached_get( 'search_terms', 0, search_prompt )
            search_terms     = self._clean_response_list( response )

            retrieved_facts  = self.entailmentbank.search_facts( search_terms )
            
            this_recall      = self.entailmentbank.onerecallatk   ( retrieved_facts, gold_facts )
            recall_total    += this_recall
            
        recall = float( recall_total / len( self.framed_questions ) )
        return recall

    
    def extended_rag_test( self )  :
        recall_total = 0
        count = 0
        for question_data in tqdm( self.framed_questions ) :
            ## pprint (question_data)
            question_frames = question_data['question']['frames']
            cot_frames      = list()
            for cot in question_data['cot'] :
                cot_frames += cot['frames']
                
            cot_frames = list( set( cot_frames ) )
            cot_frames.sort()
            assert len( question_frames ) == 1
            question_frame = question_frames[0]

            inference_prompt = self._generate_prompt( question_data['question']['text'], 'frame_relations', question_frame  )
            response         = self._cached_get( 'frame_relations', 0, inference_prompt )
            frames           = self._clean_response_list( response )

            # print( inference_prompt )
            # print( frames )

            relevant_frames  = self._get_sentencebert_frames( frames )
            relevant_frames  = [ question_frames ] + relevant_frames

            uniq_frames      = list()
            updated_frames   = list()
            for frame_set in relevant_frames :
                this_frames = list()
                for elem in frame_set :
                    if not elem in uniq_frames :
                        this_frames.append( elem )
                updated_frames.append( this_frames ) 

            relevant_frames = updated_frames
            retrieved_facts = self.frame_based_retrive( relevant_frames )
            gold_facts      = [ i['fact'] for i in question_data['cot'] ]
            
            this_recall     = self.entailmentbank.onerecallatk   ( retrieved_facts, gold_facts )
            recall_total   += this_recall
            count += 1
            print( this_recall, float(recall_total/count) )

            if self.verbose and False:
                print( "*" * 60 ) 
                print( "Question: {}".format( question_data['question'] ) )
                print( "Question Frames: {}".format( question_frame ) )
                print( "Rel Actal: {}".format( ', '.join( cot_frames ) ) )

                print( "GOT: ", frames )
                print( "GOT RelFrames", relevant_frames )

                print( this_recall, flush=True )
                print( "*" * 60 ) 


            
        recall = float( recall_total / len( self.framed_questions ) )
        return recall
            
            
    def inference_rag_test( self ) :
        ## This is single step -- simply based on the frames associated the question (and semantic similarity).
        ## Not used in paper
        recall_total = 0 
        for question_data in self.framed_questions :
            gold_facts      = [ i['fact'] for i in question_data['cot'] ]
            relevant_frames = self._get_sentencebert_frames( question_data['question']['frames'] )
            retrieved_facts = self.frame_based_retrive( relevant_frames )
            recall_total   += self.entailmentbank.onerecallatk   ( retrieved_facts, gold_facts )
        inf_recall = float( recall_total / len( self.framed_questions ) )
        if self.verbose : 
            print( "Inference RAG Recall@{}:   ".format( self.entailmentbank.k ), inf_recall, flush=True )
        return inf_recall
            
    
    def basic_rag_test( self ) :
        recall_total    = 0
        precision_total = 0 
        for question_data in self.framed_questions :
            gold_facts      = [ i['fact'] for i in question_data['cot'] ]
            retrieved_facts = list()
            for frame in question_data['question']['frames'] :
                retrieved_facts += list( set( self.frame_index[ frame ] ) ) 
            precision_total+= self.entailmentbank.oneprecisionatk( retrieved_facts, gold_facts )
            recall_total   += self.entailmentbank.onerecallatk   ( retrieved_facts, gold_facts )
        rag_recall = float( recall_total / len( self.framed_questions ) )
        if self.verbose : 
            print( "Basic RAG Recall@{}:   ".format( self.entailmentbank.k ), rag_recall  )
            print( "Basic RAG Precision@{}:".format( self.entailmentbank.k ), precision_total / len( self.framed_questions ) )
        return rag_recall
    
    def writeout( self ) :
        output = list()
        for question_data in self.framed_questions :
            output.append( [ 'Question', question_data['question'][ 'text' ] ] + [ i for i in question_data['question']['frames'] ] )
            for cot in question_data[ 'cot' ] :
                output.append( [ 'COT', cot['fact'] ] + [ i for i in cot['frames'] ] )
        with open( 'frames.csv', 'w' ) as fh :
            csvwriter = csv.writer( fh )
            csvwriter.writerows( output ) 
                                                          

    
def tests() :
    
    limit          = None
    datasplit      = 'test'
    frequent_only  = False
    min_inferences = 6
    for k in [ 25, 30, 35, 40 ] : 
        entailmentbank = EntailmentBank( task='task_1', k=k )
        params = { 
            'openai_completion_style' : 'ChatCompletion',
            'template_style'          : 'template_6', 
            'model_used'              : 'gpt-4-turbo-2024-04-09', #'gpt-3.5-turbo', # 
            # 'model_used'              : 'gpt-3.5-turbo', 
            'force_framenet'          : False,
            'question_column'         : 'question',
            'cot_column'              : 'context',
            'allow_cache'             : True,
            'entailmentbank'          : entailmentbank,
        }
    
        params[ 'output_location' ]   = params[ 'model_used' ] + '-' + params[ 'template_style' ] + '-' + datasplit + '.output'
        params[ 'data_version'    ]   = datasplit
        params[ 'data'            ]   = entailmentbank.split_to_data[ datasplit ]

        ## Get frequent only
        if frequent_only : 
            ( data, data_version )  = entailmentbank.filter_data( params[ 'data' ], min_inferences=min_inferences )
            data_version = "{}_{}".format( datasplit, data_version )
            params[ 'data_version'    ]   = data_version
            params[ 'data'            ]   = data


        baseline_recalls = list()
        for _ in range( 1 ) : 
            if limit is None :
                baseline_recalls.append( entailmentbank.calculate_baseline( params[ 'data' ] ) )
            else : 
                baseline_recalls.append( entailmentbank.calculate_baseline( params[ 'data' ][ : limit ] ) )

        tester = FrameCreator( **params )
        tester.generate_frames( limit=limit )
        tester.index_frames()
        rag_recall    = tester.basic_rag_test()
        search_recall = tester.search_rag()
        inf_recall    = tester.inference_rag_test()
        ext_recall    = tester.extended_rag_test()
        
        print( """
Datasplit: {}, Limit: {}, Frequent Only: {}, Min Inferences: {}, K: {}:
Baseline: {}, RAG Recall: {}, Inference Recall: {}, Frame Inference Recall: {}, Search Rag: {}

""".format(
            datasplit, limit, frequent_only, min_inferences, k, np.average( baseline_recalls ), rag_recall, inf_recall, ext_recall, search_recall
        ) )
        tester.writeout()



if __name__ == '__main__' :
    for _ in range( 1 ) :
        tests()
