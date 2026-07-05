from dataclasses import dataclass
from typing import Optional
from abc import ABC, abstractmethod


@dataclass
class TranslationResult:
    text: str
    iast: str
    translation: Optional[str] = None


class Translator(ABC):
    @abstractmethod
    def translate(self, text: str) -> TranslationResult:
        ...


class DummyTranslator(Translator):
    def translate(self, text: str) -> TranslationResult:
        return TranslationResult(
            text=text,
            iast="",
            translation="[Translation pending]",
        )
