import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import NMF
import pickle

# Load the dataset
print("Loading dataset...")
data_path = "C:/Users/Lenovo/Desktop/Project For Data Science/Plasmid/data/OnlineRetail.xlsx"
data = pd.read_excel(data_path)

# Preprocessing
print("Preprocessing data...")
data.dropna(subset=['Description', 'CustomerID'], inplace=True)
data['CustomerID'] = data['CustomerID'].astype(str)
data['StockCode'] = data['StockCode'].astype(str)
data['Description'] = data['Description'].astype(str)
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

# Remove rows with negative quantities (e.g., product returns)
data = data[data['Quantity'] > 0]

# Content-based Filtering
print("Training content-based recommendation model...")
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = vectorizer.fit_transform(data['Description'])

# Train Nearest Neighbors model for content-based recommendations
knn_model = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute')
knn_model.fit(tfidf_matrix)

# Collaborative Filtering using NMF
print("Training collaborative filtering model...")
pivot_table = data.pivot_table(index='CustomerID', columns='StockCode', values='Quantity', fill_value=0)

# Verify non-negativity of the pivot table
if (pivot_table < 0).any().any():
    raise ValueError("Pivot table contains negative values after filtering.")

# Train NMF model
nmf_model = NMF(n_components=10, init='random', random_state=42)
user_factors = nmf_model.fit_transform(pivot_table)
item_factors = nmf_model.components_

# Save trained models
print("Saving trained models...")
output = {
    "vectorizer": vectorizer,
    "knn_model": knn_model,
    "nmf_model": nmf_model,
    "user_factors": user_factors,
    "item_factors": item_factors,
    "pivot_table": pivot_table,
    "data": data,
}

with open("C:/Users/Lenovo/Desktop/Project For Data Science/Plasmid/backend/trained_models.pkl", "wb") as file:
    pickle.dump(output, file)

print("Models saved successfully!")
