"""
pain_point_extraction.py
Extracts and groups pain point posts from cleaned Reddit data.
"""

import pandas as pd

PAIN_KEYWORDS = [
    'pain point', 'problem', 'struggle', 'challenge', 'frustration', 'issue', 'difficult', 'hard',
    'need help', 'solution', 'feature request', 'wish', 'improve', 'broken', 'bug', 'limitation', 'missing'
]

def extract_pain_points(df, keywords=PAIN_KEYWORDS):
    """
    Returns a DataFrame of posts containing any of the pain point keywords in title or body.
    Adds a 'matched_keywords' column listing which keywords were found in each post.
    """
    def find_keywords(text):
        return [kw for kw in keywords if kw in text]

    mask = df['title_clean'].apply(lambda x: any(kw in x for kw in keywords)) | \
           df['body_clean'].apply(lambda x: any(kw in x for kw in keywords))

    pain_df = df[mask].copy()
    pain_df['matched_keywords'] = pain_df.apply(
        lambda row: list(set(find_keywords(row['title_clean']) + find_keywords(row['body_clean']))), axis=1
    )
    print(f"✓ Extracted {len(pain_df)} pain point posts.")
    return pain_df

def group_by_keyword_and_subreddit(pain_df):
    """
    Groups pain point posts by matched keyword and subreddit.
    Returns a summary DataFrame.
    """
    rows = []
    for _, row in pain_df.iterrows():
        for kw in row['matched_keywords']:
            rows.append({'subreddit': row['subreddit'], 'keyword': kw, 'title': row['title'], 'url': row['url']})
    summary_df = pd.DataFrame(rows)
    summary = summary_df.groupby(['subreddit', 'keyword']).size().reset_index(name='count')
    summary = summary.sort_values(['count'], ascending=False)
    return summary

# Example usage (uncomment to run directly)
# if __name__ == "__main__":
#     df = pd.read_csv('reddit_scrape_cleaned_YYYYMMDD_HHMMSS.csv')
#     pain_df = extract_pain_points(df)
#     summary = group_by_keyword_and_subreddit(pain_df)
#     pain_df.to_csv('pain_point_posts.csv', index=False)
#     summary.to_csv('pain_point_summary.csv', index=False)