import pandas as pd
import re

def clean_reddit_data(df, min_upvotes=1, min_comments=0):
    # Remove duplicates based on title and body
    df = df.drop_duplicates(subset=['title', 'body'])
    # Drop rows with missing title or body
    df = df.dropna(subset=['title', 'body'])
    # Standardize text: lowercase, remove special characters
    def clean_text(text):
        text = str(text).lower()
        text = re.sub(r'[^a-z0-9\\s]', '', text)
        return text.strip()
    df['title_clean'] = df['title'].apply(clean_text)
    df['body_clean'] = df['body'].apply(clean_text)
    # Filter by upvotes and comments
    df = df[(df['upvotes'] >= min_upvotes) & (df['num_comments'] >= min_comments)]
    # Reset index
    df = df.reset_index(drop=True)
    print(f"✓ Data cleaned. {len(df)} posts remaining after cleaning.")
    return df