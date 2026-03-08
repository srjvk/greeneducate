from modules.llm_client import generate 
import json
SYSTEM_PROMPT = """
You are an expert educational analyst. Analyze the student's quiz responses and return a JSON object with:
    Strengths: list of topics the student understands well
    weakness: list of topics needing imporvement
    summary: 2-sentence plain-language explanation for the student
    recommended_focus: the single most important topic to study next
RESPOND ONLY WITH VALID JSON. Nothing extra.
"""

def analyze_quiz(questions: list[dict], subject: str="general") -> dict:
    quiz_text = "\n".join([
        f"Q{i+1}: {q['question']}\n"
        f"  Correct: {q['correct_answer']}\n"
        f"  Student: {q['student_answer']}"
        for i, q in enumerate(questions)
    ])

    raw = generate(
        prompt=f"Analyze this quiz:\n\n{quiz_text}",
        subject=subject,
        system=SYSTEM_PROMPT,
    )

    clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(clean)

