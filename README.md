# Final Project

## Emotion Detector

A Flask web application that detects anger, disgust, fear, joy, and sadness using IBM Watson's embedded NLP EmotionPredict service. It returns the five scores and the highest-scoring emotion.

## Run

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python server.py
```

Open http://127.0.0.1:5000. Set `PORT=5055` if port 5000 is occupied. In a Skills Network cloud lab, use `HOST=0.0.0.0 python server.py` and the lab's application launcher for port 5000.

The default Watson endpoint is provided by Skills Network and may require its lab network. `WATSON_EMOTION_URL` can override the endpoint. The application does not substitute invented predictions when the service is unavailable.

## Package

```python
from EmotionDetection import emotion_detector
print(emotion_detector("I am glad this happened"))
```

The result has keys `anger`, `disgust`, `fear`, `joy`, `sadness`, and `dominant_emotion`. Blank input and HTTP 400 responses return all six values as `None`. Other service failures raise an exception; the web route returns HTTP 503 and an availability message.

## Validation

```sh
python -m unittest test_error_handling -v
python -m unittest test_emotion_detection -v
pylint server.py
```

`test_error_handling` contains six offline checks of input validation, HTTP 400 handling, service failure behavior, and the web interface. Its mocked error responses do not validate model accuracy. `test_emotion_detection` contains five integration tests and requires access to the real Watson service.

Current verified local results: six offline checks passed; `server.py` scored 10.00/10 with Pylint. All five live Watson tests passed in the Skills Network lab (5 tests in 0.639 seconds). The deployed application returned joy for “I think I am having fun” and the required error message for blank input.

## Attribution

Based on IBM's Apache-2.0 licensed [starter project](https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai). The original interface and license are retained. Implementation and validation were prepared with AI coding assistance; no claim of independent authorship is made.
