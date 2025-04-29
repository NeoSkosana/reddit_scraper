import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from reddit_scraper import scrape_reddit
from data_cleaning import clean_reddit_data
import eda
import pain_point_extraction
import pain_point_prioritization

# Load environment variables
load_dotenv()

auth = {
    'client_id': os.getenv('REDDIT_CLIENT_ID'),
    'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
    'user_agent': os.getenv('REDDIT_USER_AGENT')
}

# 1. Scrape Reddit
df_raw = scrape_reddit(auth)

# 2. Clean Data
df_clean = clean_reddit_data(df_raw)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_csv = f'reddit_scrape_cleaned_{timestamp}.csv'
df_clean.to_csv(output_csv, index=False)
print(f"\n✓ Cleaned data saved to {output_csv}\n")

# 3. EDA
# eda.show_summary_statistics(df_clean)
# eda.plot_posts_per_subreddit(df_clean)
# eda.plot_upvotes_comments_distribution(df_clean)
# eda.list_common_keywords(df_clean)

# 4. Pain Point Extraction
pain_df = pain_point_extraction.extract_pain_points(df_clean)
summary = pain_point_extraction.group_by_keyword_and_subreddit(pain_df)

# Save results
pain_df.to_csv(f'pain_point_posts_{timestamp}.csv', index=False)
summary.to_csv(f'pain_point_summary_{timestamp}.csv', index=False)
print(f"\n✓ Pain point posts and summary saved for review.\n")

# 5. Prioritize Pain Points
priority_summary = pain_point_prioritization.prioritize_pain_points(pain_df)
priority_summary.to_csv(f'pain_point_priority_summary_{timestamp}.csv', index=False)
print("\n=== Pain Point Priority Summary ===")
print(priority_summary.head(10))  # Show top 10 pain points

# (Optional) Export top posts for the top 3 pain points
for kw in priority_summary['matched_keywords'].head(3):
    top_posts = pain_point_prioritization.top_posts_for_keyword(pain_df, kw)
    top_posts.to_csv(f'top_posts_{kw}_{timestamp}.csv', index=False)
    print(f"Top posts for '{kw}' exported.")