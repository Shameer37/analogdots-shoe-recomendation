import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import random
import os

# ===============================
# 1. Load Data
# ===============================
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

catalog = pd.read_csv(os.path.join(DATA_DIR, "sample_shoe_catalog.csv"))
ratings = pd.read_csv(os.path.join(DATA_DIR, "sample_user_interactions.csv"))
device_care = pd.read_csv(os.path.join(DATA_DIR, "sample_device_care_history.csv"))

# Ensure correct dtypes
ratings['rating'] = ratings['rating'].fillna(0).astype(float)

# ===============================
# 2. Content-Based Vectors
# ===============================
ohe = OneHotEncoder(sparse_output=False)
cat_feats = ohe.fit_transform(catalog[['type', 'material', 'season']])
num_feats = MinMaxScaler().fit_transform(catalog[['comfort_score']])
content_matrix = np.hstack([cat_feats, num_feats])

# Cosine similarity for content
content_sim = cosine_similarity(content_matrix)

# ===============================
# 3. Collaborative Filtering (Item-Item)
# ===============================
# Create user-item rating matrix
user_item_matrix = ratings.pivot_table(index='user_id', columns='shoe_id', values='rating').fillna(0)

# Cosine similarity between items
collab_sim = cosine_similarity(user_item_matrix.T)

# Map shoe_id to matrix index
shoe_id_to_idx = {shoe_id: idx for idx, shoe_id in enumerate(user_item_matrix.columns)}

# ===============================
# 4. Hybrid Recommendation
# ===============================
def hybrid_recommend(user_id, topn=5, alpha=0.5):
    """
    alpha = weight for content-based filtering
    (1-alpha) = weight for collaborative filtering
    """
    # Shoes the user has rated
    user_ratings = ratings[ratings.user_id == user_id]
    rated_shoes = user_ratings['shoe_id'].tolist()

    # Initialize score array
    hybrid_scores = np.zeros(len(catalog))

    for _, row in user_ratings.iterrows():
        sid = row['shoe_id']
        score = row['rating']

        if sid in shoe_id_to_idx:
            idx = shoe_id_to_idx[sid]

            # Collaborative scores
            collab_scores = collab_sim[idx]

            # Content scores
            content_idx = catalog.index[catalog.shoe_id == sid][0]
            content_scores = content_sim[content_idx]

            # Hybrid blend
            total_scores = alpha * content_scores + (1 - alpha) * collab_scores

            hybrid_scores += score * total_scores

    # Remove already rated shoes
    for sid in rated_shoes:
        idx = catalog.index[catalog.shoe_id == sid][0]
        hybrid_scores[idx] = -np.inf

    # Get top N recommendations
    top_indices = np.argsort(hybrid_scores)[::-1][:topn]
    return catalog.iloc[top_indices][['shoe_id', 'brand', 'model', 'type', 'comfort_score']]

# ===============================
# 5. Personalized Services
# ===============================
def proactive_care_notification(user_id):
    owned = ratings[(ratings.user_id == user_id) & (ratings.rating >= 4)]
    msgs = []
    for _, row in owned.iterrows():
        shoe = catalog[catalog.shoe_id == row.shoe_id].iloc[0]
        usage_score = row.rating * random.uniform(0.8, 1.2)
        if shoe.care_required != 'none' and usage_score > 3.5:
            msgs.append(f"Your {shoe.brand} {shoe.model} may need {shoe.care_required}.")
    return msgs

def replacement_suggestion(user_id):
    owned = ratings[(ratings.user_id == user_id) & (ratings.rating >= 4)]
    msgs = []
    for _, row in owned.iterrows():
        shoe = catalog[catalog.shoe_id == row.shoe_id].iloc[0]
        days_used = random.randint(200, 500)
        base_life = 400 if shoe.type == "running" else 700
        remaining = base_life - days_used
        if remaining < 100:
            alt = hybrid_recommend(user_id, topn=1).iloc[0]
            msgs.append(f"Consider replacing {shoe.brand} {shoe.model}. Suggested: {alt.brand} {alt.model}")
    return msgs

# ===============================
# 6. Main Execution
# ===============================
if __name__ == "__main__":
    user_id = int(input())

    print(f"Top Recommendations for User {user_id}:")
    recs = hybrid_recommend(user_id, topn=5, alpha=0.6)
    print(recs)

    # Save to CSV
    output_path = os.path.join(DATA_DIR, "recommendations.csv")
    recs.to_csv(output_path, index=False)
    print(f"✅ Recommendations saved to {output_path}")

    # Extra services
    print("\nProactive Care Notifications:")
    print(proactive_care_notification(user_id))

    print("\nReplacement Suggestions:")
    print(replacement_suggestion(user_id))
