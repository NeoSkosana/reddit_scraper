import os
from dotenv import load_dotenv
import praw
import pandas as pd
from datetime import datetime
from data_cleaning import clean_reddit_data

# Load environment variables
load_dotenv()

auth = {
    'client_id': os.getenv('REDDIT_CLIENT_ID'),
    'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
    'user_agent': os.getenv('REDDIT_USER_AGENT')
}

if not all(auth.values()):
    raise ValueError("Missing Reddit API credentials. Please check your .env file.")

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

def scrape_reddit():
    try:
        reddit = praw.Reddit(**auth)
        results = []
        for subreddit in SUBREDDITS:
            print(f"Scraping r/{subreddit}...")
            try:
                for submission in reddit.subreddit(subreddit).hot(limit=100):
                    if any(kw.lower() in submission.title.lower() or kw.lower() in submission.selftext.lower() for kw in KEYWORDS):
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
        if results:
            df = pd.DataFrame(results)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'reddit_scrape_results_{timestamp}.csv'
            df.to_csv(filename, index=False)
            print(f"✓ Saved {len(df)} posts to {filename}")
            print("\nScraping Summary:")
            print(f"Total posts found: {len(df)}")
            print("\nPosts per subreddit:")
            print(df['subreddit'].value_counts())
        else:
            print("No matching posts found.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    scrape_reddit()