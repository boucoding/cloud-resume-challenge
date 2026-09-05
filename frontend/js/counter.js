/**
 * Cloud Resume Challenge - Visitor Counter
 * Deduplication logic: Uses sessionStorage to prevent inflating the count on rapid refreshes.
 * - If not visited during the current session: Sends ?action=increment (or default) to increment count.
 * - If already visited during this session: Sends ?action=get for a read-only fetch.
 */

// Live API Gateway HTTP API v2 visitor counter endpoint
const API_URL = window.__API_URL__ || "https://zegbzy1j8g.execute-api.eu-north-1.amazonaws.com/visitors";

async function updateVisitorCount() {
  const counterElement = document.getElementById("visitor-count");
  if (!counterElement) return;

  try {
    const hasVisitedThisSession = sessionStorage.getItem("cloud_resume_visited");
    const queryParam = hasVisitedThisSession ? "?action=get" : "?action=increment";

    // If local or placeholder hasn't been set yet, show an indicator
    if (API_URL.includes("REPLACE_WITH_API_GATEWAY_URL")) {
      counterElement.textContent = "1 (Local)";
      return;
    }

    const response = await fetch(`${API_URL}${queryParam}`, {
      method: "GET",
      headers: {
        "Accept": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`API responded with status: ${response.status}`);
    }

    const data = await response.json();
    const count = data.count;

    // Smoothly animate count or display formatted number
    counterElement.textContent = Number(count).toLocaleString();

    // Mark session as visited
    if (!hasVisitedThisSession) {
      sessionStorage.setItem("cloud_resume_visited", "true");
    }
  } catch (error) {
    console.warn("Visitor counter request failed, fallback applied:", error);
    // Graceful fallback for offline viewing
    counterElement.textContent = "--";
    counterElement.title = "Live counter unreachable";
  }
}

document.addEventListener("DOMContentLoaded", updateVisitorCount);
