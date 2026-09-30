"""Live Watson tests for each of the five required emotions."""
import unittest
from EmotionDetection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Verify actual service predictions without mocked scores."""

    def test_joy(self):
        """Verify the joy example."""
        result = emotion_detector('I am glad this happened')
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_anger(self):
        """Verify the anger example."""
        result = emotion_detector('I am really mad about this')
        self.assertEqual(result["dominant_emotion"], "anger")

    def test_disgust(self):
        """Verify the disgust example."""
        result = emotion_detector('I feel disgusted just hearing about this')
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_sadness(self):
        """Verify the sadness example."""
        result = emotion_detector('I am so sad about this')
        self.assertEqual(result["dominant_emotion"], "sadness")

    def test_fear(self):
        """Verify the fear example."""
        result = emotion_detector('I am really afraid that this will happen')
        self.assertEqual(result["dominant_emotion"], "fear")


if __name__ == "__main__":
    unittest.main(verbosity=2)
