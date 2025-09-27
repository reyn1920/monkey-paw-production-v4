import re
from typing import Dict

def readability_fkgl(text: str) -> float:
    # Simple Flesch-Kincaid grade level approximation
    sentences = max(1, len(re.findall(r'[.!?]+', text)))
    words = max(1, len(re.findall(r'\b\w+\b', text)))
    syllables = max(1, sum(len(re.findall(r'[aeiouyAEIOUY]+', w)) for w in re.findall(r'\b\w+\b', text)))
    return 0.39*(words/sentences) + 11.8*(syllables/words) - 15.59

def seo_score(text: str) -> Dict[str, float]:
    wc = len(re.findall(r'\b\w+\b', text))
    avg_sent_len = wc / max(1, len(re.findall(r'[.!?]+', text)))
    return {"word_count": wc, "avg_sentence_len": avg_sent_len, "score": max(0, min(100, 100 - abs(20-avg_sent_len)*5))}
