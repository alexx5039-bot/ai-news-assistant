WRITER_PROMPT = """
Write a news article in 50 words
based on the following news.
{news}
"""

EDITOR_PROMPT = """
Review and improve the article.

Fix:
- grammar
- clarity
- readability
- professional tone

Return ONLY the final improved article.

Do not:
- explain your changes
- provide bullet points
- provide comments
- ask questions

Article:

{content}
"""