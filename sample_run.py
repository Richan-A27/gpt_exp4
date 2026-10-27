"""
Sample Run / Test Script for Experiment 4
Tests Personalized Recommendation System and feedback loop.
"""

from recommendation_engine import (
    parse_profile,
    generate_recommendations,
    apply_feedback_refinement
)

def run_test():
    print("=" * 70)
    print("EXPERIMENT 4: Personalized Recommendation System using GPT-4")
    print("=" * 70)

    # 1. Profile Module
    name = "User"
    age = 20
    field = "Computer science"
    interests = "AI"
    skill_level = "Beginner"
    preferred_type = "Practical"
    goal = "learn AI"

    profile = parse_profile(name, age, field, interests, skill_level, preferred_type, goal)
    print("\n[+] 1. User Profile Input:")
    for k, v in profile.items():
        print(f"    - {k}: {v}")

    # 2. Generate Initial Recommendations (Top 5)
    recs = generate_recommendations(profile, top_k=5)
    print("\n[+] 2. Top 5 Personalized Recommendations:")
    for i, r in enumerate(recs, start=1):
        print(f"    {i}. {r['title']}")
        print(f"       {r['explanation']}")
        print(f"       Match Score: {r['match_score']}%")

    # 3. Feedback Module Test
    feedback_text = "I am more interested in Java than Web Development"
    print(f"\n[+] 3. User Feedback Applied:\n    '{feedback_text}'")
    updated_recs = apply_feedback_refinement(profile, feedback_text)
    print("\n[+] 4. Refined Recommendations After Feedback:")
    for i, r in enumerate(updated_recs, start=1):
        print(f"    {i}. {r['title']}")
        print(f"       {r['explanation']}")
        print(f"       Match Score: {r['match_score']}%")

    print("\n[✓] Experiment 4 test completed successfully!\n")

if __name__ == "__main__":
    run_test()
