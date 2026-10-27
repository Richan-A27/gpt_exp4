function getProfilePayload(feedbackText = null) {
  return {
    name: document.getElementById("user_name").value.trim(),
    age: document.getElementById("user_age").value.trim() || 20,
    field: document.getElementById("user_field").value.trim() || "Computer science",
    interests: document.getElementById("user_interests").value.trim() || "AI",
    skill_level: document.getElementById("skill_level").value,
    preferred_type: document.getElementById("preferred_type").value,
    goal: document.getElementById("learning_goal").value.trim() || "learn AI",
    feedback: feedbackText
  };
}

function renderRecommendations(items) {
  const container = document.getElementById("recommendations-list");
  container.innerHTML = "";

  items.forEach((item, index) => {
    const div = document.createElement("div");
    div.className = "rec-item";
    div.innerHTML = `
      <div class="rec-title-row">
        <span class="rec-title">${index + 1}. ${item.title}</span>
      </div>
      <div class="rec-explanation">${item.explanation}</div>
      <div class="rec-score-row">
        Match Score: <span class="score-badge">${item.match_score}%</span>
      </div>
    `;
    container.appendChild(div);
  });

  document.getElementById("recs-section").style.display = "block";
  document.getElementById("feedback-section").style.display = "block";
}

async function fetchRecommendations() {
  const payload = getProfilePayload();
  const btn = document.getElementById("btn-generate-recs");
  btn.innerHTML = "Processing recommendations...";
  btn.disabled = true;

  try {
    const res = await fetch("/get_recommendations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      renderRecommendations(data.recommendations);
      document.getElementById("recs-section").scrollIntoView({ behavior: "smooth" });
    }
  } catch (err) {
    console.error(err);
    alert("Failed to generate recommendations.");
  } finally {
    btn.innerHTML = "✨ Generate Recommendations";
    btn.disabled = false;
  }
}

async function updateWithFeedback() {
  const feedback = document.getElementById("feedback_text").value.trim();
  if (!feedback) {
    alert("Please enter feedback to refine recommendations.");
    return;
  }

  const payload = getProfilePayload(feedback);
  const btn = document.getElementById("btn-update-recs");
  btn.innerHTML = "Updating...";
  btn.disabled = true;

  try {
    const res = await fetch("/get_recommendations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      renderRecommendations(data.recommendations);
      document.getElementById("recs-section").scrollIntoView({ behavior: "smooth" });
    }
  } catch (err) {
    console.error(err);
    alert("Feedback refinement failed.");
  } finally {
    btn.innerHTML = "🔀 Update Recommendations";
    btn.disabled = false;
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("demo") === "1" || params.get("autoload") === "1") {
    fetchRecommendations();
    document.getElementById("feedback_text").value = "I am more interested in Java than Web Development";
  }
});
