from langgraph.graph import START, END, StateGraph
from app.ai.graph.state import ArticleState
from app.ai.graph.routers import review_router
from app.ai.graph.nodes import (
    research_node,
    writer_node,
    editor_node,
    publisher_node,
    title_generator_node,
    reviewer_node,
    summarizer_node
)

builder = StateGraph(ArticleState)

builder.add_node("research", research_node)
builder.add_node("writer", writer_node)
builder.add_node("editor", editor_node)
builder.add_node("publisher", publisher_node)
builder.add_node("title_generator", title_generator_node)
builder.add_node("reviewer", reviewer_node)
builder.add_node("summarizer", summarizer_node)


builder.add_edge(START, "research")
builder.add_edge("research", "writer")
builder.add_edge("writer", "editor")
builder.add_edge("editor", "title_generator")
builder.add_edge("title_generator", "reviewer")
builder.add_conditional_edges(
    "reviewer",
    review_router,
    {
        "summarizer": "summarizer",
        "writer": "writer",
    }
)

builder.add_edge("summarizer", "publisher")
builder.add_edge("publisher", END)

graph = builder.compile()