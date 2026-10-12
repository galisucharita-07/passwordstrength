
const form = document.getElementById("passwordForm");
const passwordInput = document.getElementById("password");
const toggleButton = document.getElementById("togglePassword");

const report = document.getElementById("report");
const scoreValue = document.getElementById("scoreValue");
const strengthText = document.getElementById("strength");
const meterFill = document.getElementById("meterFill");

const checksList = document.getElementById("checksList");
const issuesList = document.getElementById("issuesList");
const suggestionsList = document.getElementById("suggestions");

const searchSpace = document.getElementById("searchSpace");
const errorMessage = document.getElementById("errorMessage");

toggleButton.addEventListener("click", function () {
    const showing = passwordInput.type === "password";

    passwordInput.type = showing ? "text" : "password";
    toggleButton.textContent = showing ? "Hide" : "Show";
});

function addListItem(list, text) {
    const item = document.createElement("li");
    item.textContent = text;
    list.appendChild(item);
}

function renderList(list, values, emptyMessage) {
    list.replaceChildren();

    if (!values || values.length === 0) {
        addListItem(list, emptyMessage);
        return;
    }

    values.forEach(function (value) {
        addListItem(list, value);
    });
}

function getScoreColor(score) {
    if (score < 30) return "#ef4444";
    if (score < 55) return "#f59e0b";
    if (score < 75) return "#22c55e";
    return "#06b6d4";
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    errorMessage.textContent = "";
    report.hidden = true;

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                password: passwordInput.value
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Analysis failed.");
        }

        const score = Math.max(
            0,
            Math.min(100, Number(result.score) || 0)
        );

        scoreValue.textContent = score;
        strengthText.textContent = result.strength;
        meterFill.style.width = score + "%";
        meterFill.style.backgroundColor = getScoreColor(score);

        const checks = Object.entries(result.checks || {}).map(
            function ([name, value]) {
                return name.replaceAll("_", " ") + ": " + value;
            }
        );

        renderList(
            checksList,
            checks,
            "No checks available."
        );

        renderList(
            issuesList,
            result.issues,
            "No obvious issues detected by these checks."
        );

        renderList(
            suggestionsList,
            result.suggestions,
            "No recommendations available."
        );

        searchSpace.textContent =
            result.estimated_search_space_bits !== undefined
                ? "Estimated search-space size: " +
                  result.estimated_search_space_bits +
                  " bits."
                : "No estimate available.";

        report.hidden = false;

    } catch (error) {
        errorMessage.textContent =
            error.message || "Unable to analyze the password.";
    }
});
