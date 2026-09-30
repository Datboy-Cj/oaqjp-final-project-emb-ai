"""Detect five emotions using IBM Watson's embedded NLP service."""
import os
import requests

EMOTION_URL = os.environ.get(
    "WATSON_EMOTION_URL",
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict",
)
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyse):
    """Return emotion scores and the dominant emotion; invalid input yields None.

    Service/network errors other than HTTP 400 are raised to the caller rather
    than being presented as successful emotion predictions.
    """
    empty_result = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    if not isinstance(text_to_analyse, str) or not text_to_analyse.strip():
        return empty_result
    response = requests.post(
        EMOTION_URL,
        json={"raw_document": {"text": text_to_analyse}},
        headers={"grpc-metadata-mm-model-id":
                 "emotion_aggregated-workflow_lang_en_stock"},
        timeout=30,
    )
    if response.status_code == 400:
        return empty_result
    response.raise_for_status()
    scores = response.json()["emotionPredictions"][0]["emotion"]
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
