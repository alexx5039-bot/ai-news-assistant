from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI

from app.ai.prompts import SYSTEM_PROMPT
from app.core.config import settings
from app.ai.tools import (get_articles,
                          get_article,
                          update_article,
                          update_article_status,
                          delete_article,
                          create_article,
                          search_news
                          )



llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=settings.mistral_api_key
)

agent = create_agent(
    model=llm,
    tools=[
        get_article,
        get_articles,
        update_article,
        update_article_status,
        delete_article,
        create_article,
        search_news
    ],
    system_prompt=SYSTEM_PROMPT
)
