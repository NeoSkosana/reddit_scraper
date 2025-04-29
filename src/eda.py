import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

KEYWORDS = [
    'pain point', 'problem', 'struggle', 'challenge', 'frustration', 'issue', 'difficult', 'hard',
    'need help', 'solution', 'feature request', 'wish', 'improve', 'broken', 'bug', 'limitation', 'missing'
]

def show_summary_statistics(df):
    print("=== Data Overview ===")
    print(df.info())
    print(df.head())
    print("\n=== Basic Statistics ===")
    print(df.describe(include='all'))
    print("\n=== Posts per Subreddit ===")
    print(df['subreddit'].value_counts())

def plot_posts_per_subreddit(df):
    plt.figure(figsize=(12, 6))
    df['subreddit'].value_counts().plot(kind='bar')
    plt.title('Number of Posts per Subreddit')
    plt.xlabel('Subreddit')
    plt.ylabel('Number of Posts')
    plt.tight_layout()
    plt.show()

def plot_upvotes_comments_distribution(df):
    plt.figure(figsize=(10, 4))
    plt.hist(df['upvotes'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Upvotes')
    plt.xlabel('Upvotes')
    plt.ylabel('Number of Posts')
    plt.tight_layout()
    plt.show()
    plt.figure(figsize=(10, 4))
    plt.hist(df['num_comments'], bins=30, color='salmon', edgecolor='black')
    plt.title('Distribution of Number of Comments')
    plt.xlabel('Number of Comments')
    plt.ylabel('Number of Posts')
    plt.tight_layout()
    plt.show()

def get_top_words(series, n=20):
    words = []
    for text in series.dropna():
        words += re.findall(r'\b\w+\b', str(text).lower())
    return Counter(words).most_common(n)

def list_common_keywords(df):
    print("\n=== Top 20 Words in Titles ===")
    print(get_top_words(df['title_clean']))
    print("\n=== Top 20 Words in Bodies ===")
    print(get_top_words(df['body_clean']))
    print("\n=== Keyword Frequency in Titles ===")
    print(keyword_counts(df['title_clean'], KEYWORDS))
    print("\n=== Keyword Frequency in Bodies ===")
    print(keyword_counts(df['body_clean'], KEYWORDS))

def keyword_counts(series, keywords):
    counts = {kw: 0 for kw in keywords}
    for text in series.dropna():
        for kw in keywords:
            if kw in text:
                counts[kw] += 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)