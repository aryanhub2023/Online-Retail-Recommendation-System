from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import webbrowser
import threading

# Load trained models and data
print("Loading trained models...")
with open("C:/Users/Lenovo/Desktop/Project For Data Science/Plasmid/backend/trained_models.pkl", "rb") as file:
    models = pickle.load(file)

vectorizer = models["vectorizer"]
knn_model = models["knn_model"]
nmf_model = models["nmf_model"]
user_factors = models["user_factors"]
item_factors = models["item_factors"]
pivot_table = models["pivot_table"]
data = models["data"]

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Content-based Recommendation Function
def get_content_recommendations(product_id, top_n=5):
    try:
        product_index = data[data['StockCode'] == product_id].index[0]
        product_vector = vectorizer.transform([data.iloc[product_index]['Description']])
        distances, indices = knn_model.kneighbors(product_vector, n_neighbors=top_n)
        recommendations = [data.iloc[idx]['Description'] for idx in indices[0]]
        return recommendations
    except IndexError:
        return ["Product not found"]

# Collaborative Filtering Recommendation Function
def get_collab_recommendations(user_id, top_n=5):
    try:
        user_index = pivot_table.index.get_loc(user_id)
        user_scores = user_factors[user_index].dot(item_factors)
        top_indices = user_scores.argsort()[::-1][:top_n]
        recommended_items = pivot_table.columns[top_indices]
        return [data[data['StockCode'] == item]['Description'].iloc[0] for item in recommended_items if item in data['StockCode'].values]
    except KeyError:
        return ["User not found"]

# Hybrid Recommendation Function
def hybrid_recommend_products(customer_id, product_id, top_n=5):
    collab_recs = get_collab_recommendations(customer_id, top_n)
    content_recs = get_content_recommendations(product_id, top_n)
    hybrid_recs = list(set(collab_recs + content_recs))[:top_n]
    return hybrid_recs

# API Endpoints
@app.route('/recommend/content', methods=['GET'])
def recommend_content():
    product_id = request.args.get('product_id')
    recommendations = get_content_recommendations(product_id)
    return jsonify({"product_id": product_id, "recommendations": recommendations})

@app.route('/recommend/collab', methods=['GET'])
def recommend_collab():
    user_id = request.args.get('user_id')
    recommendations = get_collab_recommendations(user_id)
    return jsonify({"user_id": user_id, "recommendations": recommendations})

@app.route('/recommend/hybrid', methods=['GET'])
def recommend_hybrid():
    user_id = request.args.get('user_id')
    product_id = request.args.get('product_id')
    recommendations = hybrid_recommend_products(user_id, product_id)
    return jsonify({"user_id": user_id, "product_id": product_id, "recommendations": recommendations})

# Automatically open the frontend
def open_frontend():
    frontend_path = "file:///C:/Users/Lenovo/Desktop/Project For Data Science/Plasmid/frontend/index.html"
    print(f"Opening frontend: {frontend_path}")
    webbrowser.open(frontend_path)

if __name__ == '__main__':
    # Start a thread to open the frontend
    threading.Timer(1.0, open_frontend).start()
    app.run(debug=True)
