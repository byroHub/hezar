from hezar.preprocessors.tokenizers import Tokenizer


tokenizer = Tokenizer.load(hub_or_local_path="hezar-ai/roberta-fa")
encoded = tokenizer(["Hello guys", "my name is", "Aryan Shekarlaban"], return_attention_mask=True)
decoded = tokenizer.decode(encoded["token_ids"])

tokenizer = Tokenizer.load(hub_or_local_path="hezar-ai/distilbert-fa")
encoded = tokenizer(["Hello guys", "my name is", "Aryan Shekarlaban"], return_attention_mask=True)
decoded = tokenizer.decode(encoded["token_ids"])
...
