import os
import json


class LanguageManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, default_lang="en"):
        self.lang_dir = os.path.dirname(os.path.abspath(__file__))
        self.translations = {}
        self.load_language(default_lang)

    def load_language(self, lang_code):
        path = os.path.join(self.lang_dir, f"{lang_code}.json")
        with open(path, encoding="utf-8") as f:
            self.translations = json.load(f)
        self.current_lang = lang_code

    def get(self, key, **kwargs):
        text = self.translations.get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text
