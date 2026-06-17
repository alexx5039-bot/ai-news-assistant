from app.ai.graph.state import ArticleState

def review_router(state: ArticleState):

    if state["quality_score"] >= 5:

        return "publisher"

    if state["review_attempts"] >= 2:
        return "publisher"

    return "writer"