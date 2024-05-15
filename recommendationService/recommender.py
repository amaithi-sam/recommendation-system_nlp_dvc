import pandas as pd
import joblib




def get_recommendations(idx):
    
    df = pd.read_csv('recommendationService/recommend.csv')
    
    cosine_sim = joblib.load('recommendationService/cosine_sim.joblib')
    
    # indices = pd.Series(df['index'], index=df['product'])

    # idx = indices[title]
    idx = int(idx)

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    _indices = [i[0] for i in sim_scores]

    return df[['product', 'rating', 'sale_price', 'market_price']].iloc[_indices] 