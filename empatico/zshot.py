from transformers import BartForSequenceClassification, BartTokenizer
tokenizer = BartTokenizer.from_pretrained(
    'facebook/bart-large-mnli',
    local_files_only=True,
)
model = BartForSequenceClassification.from_pretrained(
    'facebook/bart-large-mnli',
    local_files_only=True,
)

def prob(premise, hypothesis):
    input_ids = tokenizer.encode(premise, hypothesis, return_tensors='pt')
    logits = model(input_ids)[0]

    # Using the "entrainment" (2) category as the likelihood of the
    # hypothesis being correct.
    entail_contradiction_logits = logits[:,[0,2]]
    probs = entail_contradiction_logits.softmax(dim=1)
    true_prob = probs[:,1].item() * 100
    return true_prob

def detect_emotions(text: str, report_threshold: float = 80.0) -> list:
    hypotheses = dict(
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
    return detect_emotions_raw(text, hypotheses, report_threshold)


def detect_emotions_raw(premise: str, hypotheses: dict, report_threshold: float = 80.0) -> list:
    output = []
    for label, h in hypotheses.items():
        x = prob(premise, h)
        if x > report_threshold:
            output.append(dict(
                label=label,
                score=x,
            ))

    return output
