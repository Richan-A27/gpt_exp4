"""
Ex. No.: 4 - Personalized Recommendation System
Backend: Flask Application
"""

import os
from flask import Flask, render_template, request, jsonify
from recommendation_engine import (
    parse_profile,
    generate_recommendations,
    apply_feedback_refinement,
    save_recommendation_history
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_recommendations", methods=["POST"])
def handle_recommendations():
    data = request.get_json() or {}
    name = data.get("name", "")
    age = data.get("age", 20)
    field = data.get("field", "Computer science")
    interests = data.get("interests", "AI")
    skill_level = data.get("skill_level", "Beginner")
    preferred_type = data.get("preferred_type", "Practical")
    goal = data.get("goal", "learn AI")
    feedback = data.get("feedback", None)

    profile = parse_profile(name, age, field, interests, skill_level, preferred_type, goal)
    
    if feedback:
        recommendations = apply_feedback_refinement(profile, feedback)
    else:
        recommendations = generate_recommendations(profile)

    save_recommendation_history(profile, recommendations, feedback)

    return jsonify({
        "success": True,
        "profile": profile,
        "recommendations": recommendations,
        "feedback_applied": bool(feedback)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    print(f"[*] Starting Personalized Recommendation System on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
