"use strict";
async function RunSentimentAnalysis() {
    const text = document.getElementById("textToAnalyze").value;
    const output = document.getElementById("system_response");
    output.textContent = "Analyzing…";
    try {
        const response = await fetch(
            "emotionDetector?" + new URLSearchParams({ textToAnalyze: text })
        );
        output.textContent = await response.text();
    } catch (error) {
        output.textContent = "Could not reach the application. Please try again.";
    }
}
