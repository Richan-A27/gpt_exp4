"""
Experiment 4: Personalized Recommendation System
Module Architecture:
1. Input Module
2. Profile Module
3. Preference Module
4. Prompt Module (supports GPT-4 / Ollama / deterministic credit-free engine)
5. Recommendation Module
6. Ranking Module (computes match scores and returns top 5)
7. Explanation Module (generates pedagogical explanation for suitability)
8. Feedback Module (recalibrates recommendations based on user feedback)
9. Intent Module
10. Save Module
11. Main Module (Flask Web Application)
"""

import os
import json
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVED_DIR = os.path.join(BASE_DIR, "saved_recommendations")
SAVED_FILE = os.path.join(SAVED_DIR, "recommendations_log.json")


# Knowledge base of curated learning items
LEARNING_CATALOG = [
    {
        "id": "ai_fund",
        "title": "Artificial Intelligence Fundamentals",
        "topics": ["ai", "artificial intelligence", "algorithms", "problem solving"],
        "level": "Beginner",
        "type": "Theoretical",
        "base_explanation": "Matches your interest in Artificial Intelligence.",
        "base_score": 95
    },
    {
        "id": "ml_basics",
        "title": "Machine Learning Basics",
        "topics": ["ai", "machine learning", "ml", "data", "python", "scikit-learn"],
        "level": "Beginner",
        "type": "Practical",
        "base_explanation": "Provides a foundation for learning AI.",
        "base_score": 92
    },
    {
        "id": "gen_ai",
        "title": "Generative AI",
        "topics": ["ai", "generative ai", "llm", "prompt engineering", "gpt"],
        "level": "Intermediate",
        "type": "Both",
        "base_explanation": "Introduces modern AI and language-model concepts.",
        "base_score": 90
    },
    {
        "id": "dl_fund",
        "title": "Deep Learning Fundamentals",
        "topics": ["ai", "deep learning", "neural networks", "pytorch", "tensorflow"],
        "level": "Intermediate",
        "type": "Practical",
        "base_explanation": "Provides a natural progression after Machine Learning.",
        "base_score": 87
    },
    {
        "id": "cv_apps",
        "title": "Computer Vision",
        "topics": ["ai", "computer vision", "opencv", "images", "visual ai"],
        "level": "Intermediate",
        "type": "Practical",
        "base_explanation": "Introduces practical AI applications using images.",
        "base_score": 84
    },
    {
        "id": "nlp_apps",
        "title": "Natural Language Processing (NLP)",
        "topics": ["ai", "nlp", "text mining", "linguistics", "transformers"],
        "level": "Intermediate",
        "type": "Both",
        "base_explanation": "Enables machines to understand and process human language.",
        "base_score": 82
    },
    {
        "id": "java_core",
        "title": "Core Java Masterclass & OOP Principles",
        "topics": ["java", "oop", "backend", "software engineering"],
        "level": "Beginner",
        "type": "Practical",
        "base_explanation": "Master object-oriented programming with strong Java fundamentals.",
        "base_score": 94
    },
    {
        "id": "spring_boot",
        "title": "Spring Boot & Microservices Development",
        "topics": ["java", "spring boot", "microservices", "rest api"],
        "level": "Intermediate",
        "type": "Practical",
        "base_explanation": "Build enterprise-grade REST APIs and cloud-ready backend microservices.",
        "base_score": 89
    },
    {
        "id": "web_dev",
        "title": "Full-Stack Web Development Bootcamp",
        "topics": ["web", "web development", "javascript", "react", "html", "css"],
        "level": "Beginner",
        "type": "Practical",
        "base_explanation": "Hands-on project-based roadmap covering frontend and backend web development.",
        "base_score": 88
    },
    {
        "id": "python_data",
        "title": "Python for Data Science and Analysis",
        "topics": ["python", "pandas", "data science", "numpy", "matplotlib"],
        "level": "Beginner",
        "type": "Practical",
        "base_explanation": "Essential hands-on Python skills for data manipulation and visualization.",
        "base_score": 91
    }
]


# ==========================================
# 1 & 2. Input & Profile Module
# ==========================================
def parse_profile(name, age, field, interests, skill_level, preferred_type, goal):
    """Structures and validates the user profile."""
    return {
        "name": (name or "Student").strip(),
        "age": int(age) if str(age).isdigit() else 20,
        "field": (field or "Computer Science").strip(),
        "interests": (interests or "AI").strip(),
        "skill_level": skill_level if skill_level in ["Beginner", "Intermediate", "Advanced"] else "Beginner",
        "preferred_type": preferred_type if preferred_type in ["Practical", "Theoretical", "Both"] else "Practical",
        "goal": (goal or "learn AI").strip()
    }


# ==========================================
# 3 & 9. Preference & Intent Module
# ==========================================
def extract_learning_intent(interests, goal):
    """Extracts thematic intent keywords."""
    combined = f"{interests} {goal}".lower()
    intent_tags = set()
    for token in combined.replace(",", " ").replace(";", " ").split():
        clean = token.strip()
        if len(clean) > 1:
            intent_tags.add(clean)
    return list(intent_tags)


# ==========================================
# 4, 5, 6, 7. Recommendation, Ranking & Explanation Modules
# ==========================================
def generate_recommendations(profile, feedback=None, top_k=5):
    """
    Ranks items according to match score against user profile,
    taking into account dynamic feedback refinement.
    """
    intent_keywords = extract_learning_intent(profile["interests"], profile["goal"])
    
    # Check feedback adjustment
    boost_keywords = []
    penalize_keywords = []
    if feedback:
        fb_lower = feedback.lower()
        # Look for "more interested in X than Y"
        if "more interested in" in fb_lower:
            parts = fb_lower.split("more interested in")
            after = parts[1]
            if "than" in after:
                preferred, disliked = after.split("than", 1)
                boost_keywords.extend([w.strip() for w in preferred.split() if len(w.strip()) > 1])
                penalize_keywords.extend([w.strip() for w in disliked.split() if len(w.strip()) > 1])
            else:
                boost_keywords.extend([w.strip() for w in after.split() if len(w.strip()) > 1])
        else:
            boost_keywords.extend([w.strip() for w in fb_lower.split() if len(w.strip()) > 2])

    scored_items = []

    for item in LEARNING_CATALOG:
        score = item["base_score"]

        # Relevance to primary interests
        topic_match = any(t in intent_keywords for t in item["topics"])
        if topic_match:
            score += 4
        else:
            score -= 10

        # Skill Level matching
        if item["level"] == profile["skill_level"]:
            score += 3
        elif profile["skill_level"] == "Beginner" and item["level"] == "Advanced":
            score -= 8

        # Learning type matching
        if profile["preferred_type"] == "Both" or item["type"] == profile["preferred_type"] or item["type"] == "Both":
            score += 2

        # Apply user feedback adjustments
        if boost_keywords and any(bk in item["topics"] or bk in item["title"].lower() for bk in boost_keywords):
            score += 15
        if penalize_keywords and any(pk in item["topics"] or pk in item["title"].lower() for pk in penalize_keywords):
            score -= 20

        # Dynamic explanation adaptation
        explanation = item["base_explanation"]
        if boost_keywords and any(bk in item["topics"] for bk in boost_keywords):
            explanation = f"Prioritized based on your feedback preference for {', '.join(boost_keywords)}."

        # Clamp between 60% and 98%
        final_score = max(60, min(98, score))

        scored_items.append({
            "title": item["title"],
            "explanation": explanation,
            "match_score": final_score,
            "level": item["level"],
            "type": item["type"]
        })

    # Sort descending by match_score
    scored_items.sort(key=lambda x: x["match_score"], reverse=True)
    return scored_items[:top_k]


# ==========================================
# 8. Feedback Module
# ==========================================
def apply_feedback_refinement(profile, feedback_text):
    """Processes user feedback and produces updated recommendations."""
    return generate_recommendations(profile, feedback=feedback_text, top_k=5)


# ==========================================
# 10. Save Module
# ==========================================
def save_recommendation_history(profile, recommendations, feedback=None):
    """Logs recommendations to disk."""
    os.makedirs(SAVED_DIR, exist_ok=True)
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "profile": profile,
        "feedback": feedback,
        "recommendations": recommendations
    }
    history = []
    if os.path.exists(SAVED_FILE):
        try:
            with open(SAVED_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
    history.append(entry)
    with open(SAVED_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
