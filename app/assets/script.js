const form = document.getElementById("predictionForm");
const placeholder = document.getElementById("placeholder");
const loading = document.getElementById("loading");
const resultPanel = document.getElementById("result");
const submitButton = form.querySelector(".predict-btn");

const numericFields = new Set([
    "age", "studytime", "failures", "G1", "G2", "absences",
    "Medu", "Fedu", "famrel", "health", "freetime"
]);

const modelDefaults = {
    address: "U",
    guardian: "mother",
    Mjob: "at_home",
    Fjob: "teacher",
    Pstatus: "T",
    reason: "course",
    activities: "no",
    schoolsup: "yes",
    nursery: "yes",
    traveltime: 2,
    paid: "no",
    famsup: "no",
    goout: 4,
    Walc: 1,
    romantic: "no",
    Dalc: 1
};

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = {};
    for (const [key, value] of new FormData(form).entries()) {
        data[key] = numericFields.has(key) ? Number.parseInt(value, 10) : value;
    }
    Object.assign(data, modelDefaults);

    placeholder.style.display = "none";
    resultPanel.style.display = "none";
    loading.style.display = "block";
    submitButton.disabled = true;

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json().catch(() => ({}));
        if (!response.ok) {
            throw new Error("The prediction service could not process this profile.");
        }

        renderPrediction(data, result);
    } catch (error) {
        renderError(error.message || "Unable to reach the prediction service. Please try again.");
    } finally {
        loading.style.display = "none";
        submitButton.disabled = false;
    }
});

form.addEventListener("reset", () => {
    window.setTimeout(() => {
        resultPanel.style.display = "none";
        resultPanel.innerHTML = "";
        placeholder.style.display = "flex";
        loading.style.display = "none";
        submitButton.disabled = false;
    }, 0);
});

function renderPrediction(inputData, result) {
    const isPassing = result.pass_fail === "PASS";
    const insights = generateInsights(inputData, result);

    const factorMarkup = insights.factors.map((factor) =>
        '<div class="insight-item"><strong>' + factor.icon + " " + factor.title +
        '</strong><span>' + factor.description + "</span></div>"
    ).join("");

    const recommendationMarkup = insights.recommendations.map((recommendation) =>
        '<div class="recommendation-item"><span class="recommendation-icon">' +
        recommendation.icon + '</span><span>' + recommendation.text + "</span></div>"
    ).join("");

    resultPanel.className = "result " + (isPassing ? "pass" : "fail");
    resultPanel.innerHTML =
        '<div class="outcome-label">' + (isPassing ? "ON TRACK" : "SUPPORT MAY HELP") + "</div>" +
        "<h3>" + (isPassing ? "Predicted to pass" : "At risk of not passing") + "</h3>" +
        '<div class="prediction-metrics">' +
            '<div class="metric-card"><span>Estimated grade</span><strong>' +
                result.predicted_grade + '<small>/20</small></strong><em>' + result.percentage + "</em></div>" +
            '<div class="metric-card"><span>Model confidence</span><strong>' +
                result.confidence + "</strong><em>for this outcome</em></div>" +
        "</div>" +
        '<p class="estimate-note">The model classifies pass/fail. The grade shown is derived from its confidence, not a separate grade prediction.</p>' +
        '<div class="insight-section"><h4>What stands out</h4>' +
            (factorMarkup || '<p class="quiet-copy">No standout factors from these inputs.</p>') +
        "</div>" +
        '<div class="insight-section recommendation-section"><h4>A possible next step</h4>' +
            recommendationMarkup +
        "</div>";

    resultPanel.style.display = "block";
    resultPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function renderError(message) {
    resultPanel.className = "result error";
    resultPanel.innerHTML = '<h3>Prediction unavailable</h3><p></p>';
    resultPanel.querySelector("p").textContent = message;
    resultPanel.style.display = "block";
}

function generateInsights(inputData, result) {
    const factors = [];
    const recommendations = [];

    if (inputData.G1 >= 15 || inputData.G2 >= 15) {
        factors.push({
            icon: "↗",
            title: "Strong recent grades",
            description: "Recent grades show a positive academic pattern."
        });
    } else if (inputData.G1 < 10 || inputData.G2 < 10) {
        factors.push({
            icon: "↘",
            title: "Recent grades may need attention",
            description: "A check-in on coursework could help identify where support is needed."
        });
    }

    if (inputData.studytime >= 3) {
        factors.push({
            icon: "◷",
            title: "Regular study time",
            description: "More weekly study time can support steady progress."
        });
    }

    if (inputData.failures > 0) {
        factors.push({
            icon: "!",
            title: "Previous class challenges",
            description: inputData.failures + " past failure(s) may be worth discussing."
        });
    }

    if (inputData.absences > 10) {
        factors.push({
            icon: "⌂",
            title: "Attendance may be a factor",
            description: inputData.absences + " absences could affect time in class."
        });
    } else if (inputData.absences <= 5) {
        factors.push({
            icon: "✓",
            title: "Consistent attendance",
            description: "The reported absence count is relatively low."
        });
    }

    if (inputData.Medu >= 3 || inputData.Fedu >= 3) {
        factors.push({
            icon: "＋",
            title: "Family education background",
            description: "Consider what learning support is available at home."
        });
    }

    if (result.pass_fail === "PASS") {
        recommendations.push({
            icon: "↗",
            text: "Encourage the student to keep up the study and attendance habits that are working."
        });
    } else {
        recommendations.push({
            icon: "＋",
            text: "Consider a supportive check-in and connecting the student with additional academic help."
        });
    }

    return { factors: factors.slice(0, 3), recommendations };
}