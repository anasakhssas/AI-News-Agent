import os
from typing import List, Dict
from groq import Groq

def generate_summary(articles: List[Dict[str, str]]) -> str:
    """Generates a summary of the provided articles using Groq API."""
    if not articles:
        return "No news articles available to summarize today."

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is missing.")

    # Initialize the Groq client
    client = Groq(api_key=api_key)

    # Format articles for the prompt
    news_text = "\n".join([f"- {a['title']} (Source: {a['source']})" for a in articles])
    
    prompt = f"You are a global intelligence analyst. Summarize the following world news headlines regarding AI, geopolitics, and global events into a concise, professional 3-sentence morning briefing:\n\n{news_text}"

    try:
        # Call the Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a highly efficient AI news curator."},
                {"role": "user", "content": prompt}
            ],
            model="openai/gpt-oss-20b", # Using Meta's Llama 3 70B model via Groq
            temperature=0.5,
            max_tokens=200
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating summary with Groq: {e}")
        return "Failed to generate AI summary today."