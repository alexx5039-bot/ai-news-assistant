from app.ai.agent import llm
from app.ai.graph.prompts import WRITER_PROMPT, EDITOR_PROMPT
from app.ai.graph.state import ArticleState
from app.ai.tools import (
    search_news,
    create_article,
    get_article,
    update_article,
)

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

async def publisher_node(state: ArticleState):
    article = await create_article.ainvoke({
        "title": state["title"],
        "content": state["content"]
        }
    )
    return {
        "article_id": article["id"]
    }
