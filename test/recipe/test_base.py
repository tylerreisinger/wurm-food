from wurm_food.knowledge import KnowledgeBase


class TestBase(object):
    @classmethod
    def setup_class(cls):
        cls._kb = KnowledgeBase.load_from_json('../data/knowledge')