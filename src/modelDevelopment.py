import os 
import pandas as pd
import argparse
from getData import get_dataframe, read_params
import joblib
from pathlib import Path

def model_development(config_path):
    
    print("-------------------- MODEL DEVELOPMENT INITIATED------------------", end='\n\n')
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    config = read_params(config_path)
    processed_data_path = config['data_source']['preprocessed_data_source']
    model_path = config['recommendation']['cosine_model_path']
    recommend_data_path = config['recommendation']['recommend_data']
    
    
    model_path = os.path.join(model_path, 'cosine_sim.joblib')
    
    df = pd.read_csv(processed_data_path)
    
    # TFIDF MODEL & COSINE SIMILIARITY(METRIC) MODEL
    
    Tfidf = TfidfVectorizer(stop_words='english')
    
    count_matrix = Tfidf.fit_transform(df['product_classification_features'])
    
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
    joblib.dump(cosine_sim, model_path)
    

    df.drop(['product_classification_features', 'sub_category', 'type'], inplace=True, axis=1)

    df.to_csv(recommend_data_path)

    print("-------------------- COMPLETED ------------------", end='\n\n')



if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default='params.yaml')
    parsed_args = args.parse_args()
    model_development(parsed_args.config)