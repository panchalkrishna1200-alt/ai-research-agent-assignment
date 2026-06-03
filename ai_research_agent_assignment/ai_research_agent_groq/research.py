from duckduckgo_search import DDGS
import wikipedia
import time


def search_company(company_name: str) -> str:
    queries = [
        f"{company_name} company overview business",
        f"{company_name} recent news 2024 2025",
        f"{company_name} expansion plans projects",
        f"{company_name} challenges issues",
    ]
    results_text = ""
    try:
        with DDGS() as ddgs:
            for query in queries:
                try:
                    results = list(ddgs.text(query, max_results=3))
                    if results:
                        results_text += f"\n--- {query} ---\n"
                        for r in results:
                            results_text += f"• {r.get('title','')}\n  {r.get('body','')}\n\n"
                    time.sleep(0.3)
                except Exception:
                    continue
    except Exception as e:
        results_text += f"\nSearch error: {e}"
    return results_text.strip() or f"Limited results for {company_name}."


def get_wikipedia_summary(company_name: str) -> str:
    try:
        wikipedia.set_lang("en")
        results = wikipedia.search(company_name, results=3)
        for title in results:
            try:
                summary = wikipedia.summary(title, sentences=10, auto_suggest=False)
                page = wikipedia.page(title, auto_suggest=False)
                return f"Title: {page.title}\n\n{summary}"
            except wikipedia.exceptions.DisambiguationError as e:
                try:
                    summary = wikipedia.summary(e.options[0], sentences=8, auto_suggest=False)
                    return summary
                except Exception:
                    continue
            except Exception:
                continue
        return f"No Wikipedia article found for {company_name}."
    except Exception as e:
        return f"Wikipedia error: {e}"
