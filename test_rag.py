"""
Basic tests for HealthBridge AI RAG pipeline
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import core functions from app
import importlib.util
spec = importlib.util.spec_from_file_location("app", os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py"))

def test_knowledge_base_structure():
    """All KB entries must have title, source, data, insight keys"""
    from app import KNOWLEDGE_BASE
    required_keys = {"title", "source", "data", "insight"}
    for topic, entry in KNOWLEDGE_BASE.items():
        assert required_keys.issubset(entry.keys()), f"Missing keys in {topic}"

def test_topic_keywords_coverage():
    """Every KB topic must have corresponding keywords"""
    from app import KNOWLEDGE_BASE, TOPIC_KEYWORDS
    for topic in KNOWLEDGE_BASE:
        assert topic in TOPIC_KEYWORDS, f"No keywords for topic: {topic}"
        assert len(TOPIC_KEYWORDS[topic]) >= 3, f"Too few keywords for: {topic}"

def test_find_relevant_topics_hospital():
    from app import find_relevant_topics
    topics = find_relevant_topics("What are hospital emergency wait times?")
    assert "hospital_wait_times" in topics

def test_find_relevant_topics_rural():
    from app import find_relevant_topics
    topics = find_relevant_topics("rural healthcare access in remote areas")
    assert "rural_health" in topics

def test_find_relevant_topics_digital():
    from app import find_relevant_topics
    topics = find_relevant_topics("digital health technology and data engineering")
    assert "digital_health" in topics

def test_find_relevant_topics_fallback():
    from app import find_relevant_topics
    topics = find_relevant_topics("xyzabc unknown query with no matches zzzzzz")
    assert isinstance(topics, list)
    assert len(topics) >= 1  # Should return fallback topics

def test_build_context_returns_string():
    from app import build_context
    context = build_context(["hospital_wait_times", "chronic_disease"])
    assert isinstance(context, str)
    assert len(context) > 100
    assert "AIHW" in context

def test_suggested_questions_count():
    from app import SUGGESTED_QUESTIONS
    assert len(SUGGESTED_QUESTIONS) == 8

if __name__ == "__main__":
    test_knowledge_base_structure()
    test_topic_keywords_coverage()
    test_find_relevant_topics_hospital()
    test_find_relevant_topics_rural()
    test_find_relevant_topics_digital()
    test_find_relevant_topics_fallback()
    test_build_context_returns_string()
    test_suggested_questions_count()
    print("✅ All tests passed!")
