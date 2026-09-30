"""Offline robustness tests. Mocked responses test errors, not model accuracy."""
import unittest
from unittest.mock import Mock, patch
from requests.exceptions import ConnectionError as ServiceConnectionError
from EmotionDetection import emotion_detector
from server import app


class TestErrorHandling(unittest.TestCase):
    """Exercise invalid input and service failures independently of Watson."""

    def test_blank_input(self):
        with patch("EmotionDetection.emotion_detection.requests.post") as post:
            self.assertTrue(all(value is None for value in emotion_detector("   ").values()))
            post.assert_not_called()

    def test_http_400(self):
        with patch("EmotionDetection.emotion_detection.requests.post",
                   return_value=Mock(status_code=400)):
            result = emotion_detector("invalid input")
            self.assertEqual(set(result),
                             {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"})
            self.assertTrue(all(value is None for value in result.values()))

    def test_blank_web_request(self):
        response = app.test_client().get("/emotionDetector?textToAnalyze=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Invalid text! Please try again!")

    def test_missing_web_parameter(self):
        self.assertEqual(app.test_client().get("/emotionDetector").text,
                         "Invalid text! Please try again!")

    def test_unavailable_service(self):
        with patch("server.emotion_detector", side_effect=ServiceConnectionError("offline")):
            with self.assertLogs(app.logger, level="ERROR"):
                response = app.test_client().get("/emotionDetector?textToAnalyze=hello")
        self.assertEqual(response.status_code, 503)
        self.assertIn("temporarily unavailable", response.text)

    def test_home_page(self):
        response = app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("NLP - Emotion Detection", response.text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
