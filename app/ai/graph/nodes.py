from app.ai.agent import llm
from app.ai.graph.prompts import WRITER_PROMPT, EDITOR_PROMPT
from app.ai.graph.state import ArticleState
from app.ai.tools import (
    search_news,
    create_article,
)
from app.schemas.article import ReviewResponse


async def research_node(state: ArticleState):
    news = await search_news.ainvoke(
        {"query": state["topic"]}
    )
    return {
        "news": news
    }

async def writer_node(state: ArticleState):

    prompt = WRITER_PROMPT.format(
        news=state["news"]
    )
    response = await llm.ainvoke(prompt)

    return {
        "content": response.content
    }

async def editor_node(state: ArticleState):
    prompt = EDITOR_PROMPT.format(
        content=state["content"]
    )

    response = await llm.ainvoke(prompt)

    return {
        "content": response.content
    }

async def title_generator_node(state: ArticleState):
    response = await llm.ainvoke(
        f"""
        Generate a concise news headline (max 10 words)
        for the following article.

        {state["content"]}
        """
    )

    return {
        "title": response.content.strip()
    }

async def publisher_node(state: ArticleState):
    print("STATE IN PUBLISHER:")
    print(state)

    article = await create_article.ainvoke({
        "title": state["title"],
        "content": state["content"],
        "summary": state["summary"]
        }
    )
    return {
        "article_id": article["id"]
    }

async def reviewer_node(state: ArticleState):
    response = await llm.with_structured_output(
        ReviewResponse
    ).ainvoke(
        f"""
        Review the article and rate its quality from 1 to 10.

        Consider:
        - clarity
        - grammar
        - structure
        - factual consistency

        Article:
        {state["content"]}
        """
    )

    return {
        "quality_score": response.score
    }

async def summarizer_node(state: ArticleState):
    response = await llm.ainvoke(
        f"""
        Summarize the following news article in 2-3 sentences.

        Article:
        {state["content"]}
        """
    )

    return {
        "summary": response.content.strip()
    }