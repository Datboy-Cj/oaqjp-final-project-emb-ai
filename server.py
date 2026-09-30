"""Serve the Emotion Detector interface and its Watson-backed analysis route."""
import os
from flask import Flask, render_template, request
from requests.exceptions import RequestException
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Render the supplied project's web interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detection():
    """Analyze the supplied text and return a readable summary of the scores."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text_to_analyze)
    except (RequestException, ValueError, KeyError, IndexError, TypeError):
        app.logger.exception("Emotion analysis service failed")
        return "Emotion analysis is temporarily unavailable. Please try again.", 503
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"
    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host=os.environ.get("HOST", "0.0.0.0"),
            port=int(os.environ.get("PORT", "5000")), debug=False)
