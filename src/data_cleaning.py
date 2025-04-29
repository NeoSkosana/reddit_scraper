"""
data_cleaning.py
Module for cleaning and preprocessing Reddit scrape data.
"""

import pandas as pd
import re

def clean_reddit_data(input_csv, output_csv=None, min_upvotes=1, min_comments=0):
    """
    Cleans and preprocesses Reddit data.
    - Removes duplicates
    - Drops rows with missing titles or bodies
    - Standardizes text (lowercase, removes special characters)
    - Filters by minimum upvotes and comments

    Args:
        input_csv (str): Path to the raw scraped CSV file.
        output_csv (str, optional): Path to save the cleaned CSV. If None, does not save.
        min_upvotes (int): Minimum upvotes to keep a post.
        min_comments (int): Minimum comments to keep a post.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = pd.read_csv(input_csv)

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

    # Save cleaned data if output path is provided
    if output_csv:
        df.to_csv(output_csv, index=False)
        print(f"✓ Cleaned data saved to {output_csv}")

    print(f"✓ Data cleaned. {len(df)} posts remaining after cleaning.")
    return df

# Example usage (uncomment to run directly)
# if __name__ == "__main__":
#     clean_reddit_data(
#         input_csv='../reddit_scrape_results_20250429_154526.csv',
#         output_csv='../reddit_scrape_results_cleaned.csv'
#     )