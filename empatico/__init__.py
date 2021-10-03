"""
Emotion detection microservice based on natural language inference
"""
from fastapi import FastAPI
from pydantic import BaseModel
from . import zshot

__version__ = '0.0.1'

app = FastAPI()


class Request(BaseModel):
    text: str
    report_threshold: float = 80.0
    hypotheses: dict = dict(
            positive='This text is happy.',
            negative='This text is unhappy.',
            mixed='This text is both happy and unhappy.',
            satisfied='This text is about satisfaction.',
            neutral1='This text is neither happy nor unhappy.',
            neutral2='This text is emotionless.',
            neutral3='This text is neutral.',
            factual='This text is factual.',
            anger='This text is angry.',
            sadness='This text is sad.',
            disappointment='This text is about disappointment.',
            bitter='This text is bitter.',
            sarcastic='This text is sarcastic.',
            helpful='This text is helpful.',
            fear='This text is afraid.',
            disgust='This text is disgusted.',
            surprise='This text is surprised.',
            hope='This text is hopeful.',
            trust='This text is trusting.',
            joy='This text is joyful.',
    )


@app.post("/emotions")
def detect_emotions(payload: Request):
    x = zshot.detect_emotions_raw(payload.text, payload.hypotheses, payload.report_threshold)
    print(x)
    return x
