import datetime


class Article:
    def __init__(self, id, title, summary, content, creator_id, created_at=None, is_published=False):
        self.id = id
        self.title = title
        self.summary = summary
        self.content = content
        self.creator_id = creator_id
        self.is_published = is_published
        self.created_at = created_at or datetime.datetime.now()
