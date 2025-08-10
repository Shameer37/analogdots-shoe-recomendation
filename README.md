# analogdots-shoe-recomendation

Shoe Recommendation System — Hybrid Filtering Approach

Project Overview
This project builds an intelligent shoe recommendation system that combines content-based filtering and collaborative filtering into a hybrid model.

It not only recommends shoes but also provides personalized services such as:

Proactive Care Notifications (when your shoes might need maintenance)

Replacement Suggestions (when shoes are nearing end-of-life)

The project works entirely from CSV files and optionally supports PostgreSQL via schema.sql.

Tech Stack

Python 3

Pandas, NumPy, scikit-learn

Cosine Similarity (content & collaborative)

PostgreSQL (optional, schema provided)

Project Structure
analogdots-shoe-recommendation/
├── data/
│ ├── sample_shoe_catalog.csv
│ ├── sample_user_interactions.csv
│ ├── sample_device_care_history.csv
│ └── generate_synthetic.py
├── recommendation_system/
│ └── hybrid_recommender.py
├── schema.sql
└── README.md

Why Hybrid Filtering?
We considered three main approaches:

Collaborative Filtering

Pros: Learns from similar users' behaviors.

Cons: Fails for new users or new items (cold start problem).

Content-Based Filtering

Pros: Can recommend new/unrated items based on attributes.

Cons: Limited to known attributes, may not capture hidden preferences.

Hybrid Filtering (Chosen Approach)

Combines collaborative and content-based scores.

Overcomes cold start by still recommending based on content when no rating history exists.

Improves personalization by leveraging both user behavior patterns and item characteristics.

More robust against sparse data issues.

Example:
If a user has rated a “Running Shoe” highly, the hybrid model recommends:

Other running shoes (content-based)

Shoes that similar users liked (collaborative)
The blend increases accuracy and diversity.

How to Run

Install Dependencies
pip install pandas numpy scikit-learn

Run the Recommendation Script
python recommendation_system/hybrid_recommender.py

Output

Prints top 5 recommendations for a sample user (input user_id)

Saves them to: data/recommendations.csv

Prints Proactive Care Notifications and Replacement Suggestions

Optional: Using PostgreSQL

Start PostgreSQL and create a database:
CREATE DATABASE shoe_recommendations;

Run the schema:
psql -U username -d shoe_recommendations -f schema.sql

Insert CSV data into the database.

License
This project is for educational purposes as part of the AnalogDots Machine Learning Engineer / Data Scientist Competency Assessment.

