from modules.llm_client import generate
from langdetect import detect as langdetect_detect
from langdetect.lang_detect_exception import LangDetectException
import json

SUPPORTED_LANGUAGES = [
    "English", "French", "Spanish", "Tamil",
    "Hindi",   "Mandarin", "Portuguese", "Italian"
]

LANG_CODES = {
    "fr": "French", "es": "Spanish", "en": "English",
    "ar": "Arabic", "hi": "Hindi", "zh-cn": "Mandarin",
    "pt": "Portuguese", "sw": "Swahili", "de": "German"
}

def detect_language(text: str) -> str:
    try:
        code = langdetect_detect(text)
        return LANG_CODES.get(code, code)
    except LangDetectException:
        return "Unknown"


def translate(text: str, target: str) -> str:
    if not text or text.strip().lstrip('-').replace('.','').isdigit() or len(text.strip()) <= 2:
        return text

    system = (
    f"You are a translator. Translate this text to {target}. "
    f"Keep it as a question if it is a question. "
    f"Return ONLY the translated text. No answers, no explanations."
)
    return generate(prompt=text, subject="default", system=system).strip()

def translate_quiz(questions: list[dict], target: str) -> list[dict]:
    translated = []
    for i in questions:
        translated.append({
            "question":       translate(i["question"], target),
            "correct_answer": translate(i["correct_answer"], target),
            "options":        [translate(opt, target) for opt in i.get("options", [])],
        })
    return translated