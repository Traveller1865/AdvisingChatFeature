# spell_checker.py

from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata
from typing import Any, Optional, Text, Dict
from spellchecker import SpellChecker

class SpellCheckerComponent(Component):
    name = "spell_checker"
    provides = ["text"]
    requires = []
    defaults = {}
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(SpellCheckerComponent, self).__init__(component_config)
        self.spell = SpellChecker()

    def process(self, message, **kwargs):
        text = message.get("text")
        corrected_text = []
        for word in text.split():
            corrected_word = self.spell.correction(word)
            corrected_text.append(corrected_word)
        message.set("text", " ".join(corrected_text), add_to_output=True)
