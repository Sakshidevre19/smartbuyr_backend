import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product


def get_recommendations(product_id, top_n=5):
    # Fetch limited dataset for performance
    products = Product.objects.all()[:2000]

    df = pd.DataFrame(list(products.values(
        'product_id', 'title', 'description', 'bullet_points'
    )))

    if df.empty:
        raise ValueError("No products available")

    if product_id not in df['product_id'].values:
        raise ValueError("Product not found in sample")

    df['text'] = (
        df['title'].fillna('') + ' ' +
        df['description'].fillna('') + ' ' +
        df['bullet_points'].fillna('')
    )

    tfidf = TfidfVectorizer(stop_words='english', max_features=3000)
    matrix = tfidf.fit_transform(df['text'])

    similarity = cosine_similarity(matrix)

    idx = df.index[df['product_id'] == product_id][0]

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]

    recommended_indices = [i[0] for i in scores]

    return df.iloc[recommended_indices][['product_id', 'title']]
