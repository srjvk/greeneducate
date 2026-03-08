import os, json, requests
from modules.llm_client import generate
import re

SERPAPI_KEY = "613c4a55e295e17081785cbc05d1acce4d08e8a557e188c46d21fe72ba145917"
SERPAPI_URL = "https://serpapi.com/search"

TRUSTED_DOMAINS = ["khanacademy.org","youtube.com","youtu.be"]

def serpapi_search(query: str, num: int = 10) -> list[dict]:
    params = {
        "q":      query,
        "api_key": SERPAPI_KEY,
        "num":    num,
        "engine": "google",
    }
    resp = requests.get(SERPAPI_URL, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("organic_results", [])

def filter_trusted(results: list[dict]) -> list[dict]:
    filtered = []
    for r in results:
        link = r.get("link", "")
        if any(domain in link for domain in TRUSTED_DOMAINS):
            filtered.append({"title": r.get("title"), "link": link, "snippet": r.get("snippet")})
    return filtered

def llm_rank_resources(topic: str, resources: list[dict]) -> list[dict]:
    if not resources:
        return []

    resource_text = "\n".join([
        f"{i+1}. {r['title']} — {r['link']}\n   {r.get('snippet','')}"
        for i, r in enumerate(resources)
    ])

    system = (
        "You are an educational resource curator. "
        "Given a topic and a list of links, return a JSON array where each item has: "
        "'title', 'link', 'relevance_score' (0-10), 'why_useful' (one sentence). "
        "Sort by relevance_score descending. Return ONLY a valid JSON array. "
        "No explanation, no markdown, no extra text. Start with [ and end with ]."
    )

    raw = generate(
        prompt=f"Topic: {topic}\n\nResources:\n{resource_text}",
        subject="general",
        system=system,
    )

    # Extract just the JSON array using regex
    match = re.search(r'\[.*\]', raw, re.DOTALL)
    if not match:
        # If LLM returns nothing useful, build basic list from trusted results
        return [
            {"title": r["title"], "link": r["link"], "relevance_score": 8, "why_useful": "Trusted educational source."}
            for r in resources
        ]

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        # Fallback: return raw trusted results without LLM ranking
        return [
            {"title": r["title"], "link": r["link"], "relevance_score": 8, "why_useful": "Trusted educational source."}
            for r in resources
        ]

def fetch_resources(topic: str) -> list[dict]:
    query   = f"{topic} tutorial site:khanacademy.org OR site:youtube.com"
    results = serpapi_search(query)
    trusted = filter_trusted(results)
    ranked  = llm_rank_resources(topic, trusted)
    return ranked

