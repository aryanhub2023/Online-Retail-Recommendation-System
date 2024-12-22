# Online-Retail-Recommendation-System

This project implements a Retail Recommendation System that provides product recommendations based on customer behavior and product descriptions. The system leverages both content-based and collaborative filtering techniques, with an option to combine them into a hybrid recommendation model.

Project Structure

backend
   |-- backend_server.py       # Flask backend server for recommendation APIs
   |-- model_training.py       # Script for training recommendation models
   |-- trained_models.pkl      # Serialized trained models and data
frontend
   |-- index.html              # Frontend interface for user interaction
data
   |-- OnlineRetail.xlsx       # Dataset containing retail transaction data

Features

Recommendation Types:

Content-Based: Recommends products based on their descriptions.

Collaborative Filtering: Suggests products based on user purchase history.

Hybrid: Combines both content-based and collaborative filtering recommendations.

API Endpoints:

/recommend/content: Provides content-based recommendations.

/recommend/collab: Provides collaborative filtering recommendations.

/recommend/hybrid: Provides hybrid recommendations.

Frontend:

Simple and intuitive web interface to interact with the recommendation system.

Installation and Setup

Prerequisites

Python 3.11 or higher

Flask

Pandas

Scikit-learn

Numpy

Steps

Clone the repository:

git clone https://github.com/aryanhub2023/Online-Retail-Recommendation-System.git
cd Online-Retail-Recommendation-System

Install the required Python packages:

pip install flask pandas scikit-learn numpy

Place the dataset (OnlineRetail.xlsx) in the data directory.

Train the models:

python backend/model_training.py

This script will preprocess the data, train the models, and save them to backend/trained_models.pkl.

Start the backend server:

python backend/backend_server.py

Open the frontend:

The server will automatically open the index.html file in your default browser.

Alternatively, you can manually open frontend/index.html in your browser.

Usage

Enter a User ID and Product ID in the provided input fields.

Click the "Get Recommendations" button.

View the recommendations displayed on the page.

Dataset

File: OnlineRetail.xlsx

Description: Contains retail transaction data, including product descriptions, stock codes, customer IDs, quantities, and unit prices.

Preprocessing:

Rows with missing Description or CustomerID are removed.

Negative quantities (e.g., returns) are excluded.

New column TotalPrice is calculated as Quantity * UnitPrice.

Technical Details

Backend

Built with Flask to handle API requests.

Models trained using Scikit-learn:

TF-IDF Vectorizer: For content-based filtering.

KNN (Nearest Neighbors): To find similar products based on descriptions.

NMF (Non-Negative Matrix Factorization): For collaborative filtering.

Frontend

Simple HTML and JavaScript-based interface.

Fetches recommendations from the backend using asynchronous API calls.

Future Enhancements

Add user authentication to personalize recommendations further.

Include more advanced recommendation algorithms (e.g., deep learning models).

Deploy the application to a cloud platform for broader accessibility.
