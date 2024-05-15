import argparse 
import os 
import pandas as pd 
import re

from getData import get_dataframe, read_params 


def data_preparation(config_path):
    
    print("-------------------- DATA PREPARATION INITIATED------------------", end='\n\n')
    config = read_params(config_path)
    processed_data_path = config['data_source']['preprocessed_data_source']
    
    df = get_dataframe(config_path)
    

    
    #----------------- DATA CLEANING -----------------
    
    df.drop_duplicates(inplace=True)
    
    remove_space = lambda x:x.strip()
    
    get_list = lambda x: list(map(remove_space, re.split('& |, |\*', x)))
    
    for col in ['category', 'sub_category', 'type']:
        df[col+'_'] = df[col].apply(get_list)
        
    def cleaner(x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        
        else:
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''
            
    df['brand_'] = df.loc[:, 'brand']
            
    for col in ['category_', 'sub_category_', 'type_', 'brand_']:
        df[col] = df[col].apply(cleaner)
        
    def couple(x):
        
        return ' '.join(x['category_']) + ' ' + ' '.join(x['sub_category_']) + ' '+x['brand_']+ ' '  + ' '.join(x['type_'])
        # return ' '.join(x['category_']) + ' ' + ' '.join(x['sub_category_']) + ' '+x['brand']+ ' '  + ' '.join(x['type_'])

        # return ' '.join(x['category']) + ' ' + ' '.join(x['sub_category']) + ' '+x['brand']+' ' +' '.join( x['type'])

    
    
    
    df['product_classification_features'] = df.apply(couple, axis=1)
    
    
    df.drop(['category_', 'sub_category_', 'type_', 'brand_'], axis=1, inplace=True)
    

    df.reset_index(inplace=True, drop=True)
    
    df.to_csv(processed_data_path, index_label='index')

    print("-------------------- COMPLETED------------------", end='\n\n')



if __name__ == "__main__":
    
    args = argparse.ArgumentParser()
    args.add_argument("--config", default='params.yaml')
    parsed_args = args.parse_args()
    data_preparation(parsed_args.config)
    
