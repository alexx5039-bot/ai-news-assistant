from enum import Enum

class ArticleStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"