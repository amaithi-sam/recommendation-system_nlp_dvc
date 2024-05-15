

import streamlit as st
import pandas as pd
from recommender import get_recommendations


products_df = pd.read_csv('recommendationService/recommend.csv')

# Function to search for products based on a query
def search_products(query):
    return products_df[products_df["product"].str.lower().str.contains(query.lower(), na=False)]


def format_func(option):
    return products_df[option]

 


# Streamlit app
def main():
    st.title("Big Basket Product Recommendation")

    # Search bar
    search_query = st.text_input("Search for products:")


    # Display products based on search
    if search_query:
        
        search_results = search_products(search_query)
        if search_results.empty:
            st.warning("No products found.")
        else:
            st.subheader("Search Results:")
            
            selected_product_index = st.selectbox("Select a product to view details:", options= search_results.index, format_func = lambda x : search_results.loc[x, 'product'] ) #, format_func=lambda x:search_results.product) 
            
            selected_product = search_results.loc[selected_product_index]
            
            st.subheader("Product Details:")
            st.write(f"**{selected_product['product']}** - {selected_product['brand']}")
            st.write(f"Description: {selected_product['description']}")
            
            
            # ---------------------RECOMMENDATION SYSTEM--------------------
            
            st.subheader("Recommended Products:")
            
            df = get_recommendations(selected_product['index'])
           
            for index, row in df.iterrows():
                
                discount_percentage = (float(row['market_price']) - float(row['sale_price'])) / (row['market_price']) * 100
                
                st.write(f"**{row['product']}**  - Offer : {int(discount_percentage)}%  - Rating : {row['rating']}")
                
                
            # ----------------------------------------------------------------
            
            
            
    else:
        # Display all(30) products if no search query
        st.subheader("Our Products:")
        # for _, product in products_df.iloc[:30].iterrows():
        for _, product in products_df.sample(n=30).iterrows():

            st.write(f"**{product['product']}** - {product['brand']}")

if __name__ == "__main__":
    main()
