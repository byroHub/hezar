from hezar.builders import build_model
from hezar.models import Model
from hezar.preprocessors import Tokenizer


path = "hezar-ai/distilbert-fa-sentiment-v1"
model = Model.load(path)
# model = build_model('distilbert_text_classification', id2label={0: 'negative', 1: 'positive'})
tokenizer = Tokenizer.load(path)
inputs = tokenizer(["یه تست خیلی خفن"], return_tensors="pt")
outputs = model.predict(inputs)
print(outputs)
