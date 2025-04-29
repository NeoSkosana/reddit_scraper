"""
Combined Reddit Scraper and Data Cleaner
- Scrapes Reddit posts from specified subreddits using keywords.
- Cleans and preprocesses the scraped data.
- Outputs a cleaned CSV file.
"""

import os
import re
from datetime import datetime
from dotenv import load_dotenv
import praw
import pandas as pd

# ========== CONFIGURATION ==========

# Load environment variables
load_dotenv()

auth = {
    'client_id': os.getenv('REDDIT_CLIENT_ID'),
    'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
    'user_agent': os.getenv('REDDIT_USER_AGENT')
}

SUBREDDITS = [
    'healthcare', 'HealthIT', 'medicine', 'medical', 'nursing', 'digitalhealth', 'HealthTech',
    'Construction', 'ConstructionIndustry', 'ConstructionManagement', 'civilengineering', 'architecture', 'skilledtrades',
    'education', 'Teachers', 'EdTech', 'teaching', 'OnlineLearning', 'homeschool',
    'personalfinance', 'Finance', 'FinancialPlanning', 'FinTech', 'investing', 'accounting',
    'ecommerce', 'retail', 'Entrepreneur', 'smallbusiness', 'Shopify', 'AmazonFBA'
]

KEYWORDS = [
    'pain point', 'problem', 'struggle', 'challenge', 'frustration', 'issue', 'difficult', 'hard',
    'need help', 'solution', 'feature request', 'wish', 'improve', 'broken', 'bug', 'limitation', 'missing'
]

MIN_UPVOTES = 1
MIN_COMMENTS = 0

# ========== SCRAPER FUNCTION ==========

def scrape_reddit(auth, subreddits, keywords, limit=100):
    reddit = praw.Reddit(**auth)
    results = []
    for subreddit in subreddits:
        print(f"Scraping r/{subreddit}...")
        try:
            for submission in reddit.subreddit(subreddit).hot(limit=limit):
                if any(kw.lower() in submission.title.lower() or kw.lower() in submission.selftext.lower() for kw in keywords):
                    results.append({
                        'subreddit': subreddit,
                        'title': submission.title,
                        'body': submission.selftext,
                        'author': str(submission.author),
                        'created_utc': datetime.fromtimestamp(submission.created_utc),
                        'upvotes': submission.score,
                        'url': submission.url,
                        'num_comments': submission.num_comments
                    })
        except Exception as e:
            print(f"Error scraping r/{subreddit}: {str(e)}")
            continue
    print(f"✓ Scraping complete. {len(results)} posts found.")
    return pd.DataFrame(results)

# ========== DATA CLEANING FUNCTION ==========

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

# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    # Scrape
    raw_df = scrape_reddit(auth, SUBREDDITS, KEYWORDS, limit=100)

    # Clean
    cleaned_df = clean_reddit_data(raw_df, min_upvotes=MIN_UPVOTES, min_comments=MIN_COMMENTS)

    # Save cleaned data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_csv = f'reddit_scrape_cleaned_{timestamp}.csv'
    cleaned_df.to_csv(output_csv, index=False)
    print(f"✓ Cleaned data saved to {output_csv}")