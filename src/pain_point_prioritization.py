"""
pain_point_prioritization.py
Ranks and summarizes pain points by frequency and engagement.
"""

import pandas as pd

def prioritize_pain_points(pain_df):
    """
    Returns a DataFrame ranking pain points by frequency, upvotes, and comments.
    """
    # Explode matched_keywords for grouping
    exploded = pain_df.explode('matched_keywords')
    grouped = exploded.groupby('matched_keywords').agg(
        num_posts=('title', 'count'),
        total_upvotes=('upvotes', 'sum'),
        avg_upvotes=('upvotes', 'mean'),
        total_comments=('num_comments', 'sum'),
        avg_comments=('num_comments', 'mean')
    ).reset_index()
    # Sort by number of posts, then total upvotes
    grouped = grouped.sort_values(['num_posts', 'total_upvotes'], ascending=False)
    return grouped

def top_posts_for_keyword(pain_df, keyword, n=5):
    """
    Returns the top n posts for a given pain point keyword, sorted by upvotes.
    """
    mask = pain_df['matched_keywords'].apply(lambda kws: keyword in kws)
    return pain_df[mask].sort_values('upvotes', ascending=False).head(n)

# Example usage (uncomment to run directly)
# if __name__ == "__main__":
#     pain_df = pd.read_csv('pain_point_posts_YYYYMMDD_HHMMSS.csv', converters={'matched_keywords': eval})
#     summary = prioritize_pain_points(pain_df)
#     summary.to_csv('pain_point_priority_summary.csv', index=False)
#     print(summary)