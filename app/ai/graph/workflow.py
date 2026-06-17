from langgraph.graph import START, END, StateGraph
from app.ai.graph.state import ArticleState
from app.ai.graph.nodes import (
    research_node,
    writer_node,
    editor_node,
    publisher_node
)

builder = StateGraph(ArticleState)

builder.add_node("research", research_node)
builder.add_node("writer", writer_node)
builder.add_node("editor", editor_node)
builder.add_node("publisher", publisher_node)

builder.add_edge(START, "research")
builder.add_edge("research", "writer")
builder.add_edge("writer", "editor")
builder.add_edge("editor", "publisher")
builder.add_edge("publisher", END)

graph = builder.compile()