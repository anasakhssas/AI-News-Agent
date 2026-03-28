from dotenv import load_dotenv
from src.news_fetcher import fetch_top_news
from src.summarizer import generate_summary
from src.mailer import send_newsletter

def main():
    print("Starting Daily AI News Agent...")
    
    load_dotenv()

    print("Fetching news...")
    articles = fetch_top_news(limit=5)
    
    if not articles:
        print("No articles fetched. Exiting.")
        return

    print("Generating AI summary with Groq...")
    summary = generate_summary(articles)

    print("Sending email newsletter...")
    try:
        send_newsletter(summary, articles)
        print("Process completed successfully.")
    except Exception as e:
        print(f"Process failed while sending email: {e}")

if __name__ == "__main__":
    main()
