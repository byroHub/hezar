from hezar import (
    TrainConfig,
    Trainer,
    build_dataset,
    build_model,
    build_optimizer,
    build_scheduler,
)

name = "distilbert_text_classification"

dataset_config = {
    "path": "hezar-ai/sentiment_digikala_snappfood",
    "text_field": "text",
    "label_field": "label",
    "tokenizer_path": "hezar-ai/distilbert-base-fa",
}
train_dataset = build_dataset(name="text_classification", split="train", **dataset_config)
eval_dataset = build_dataset(name="text_classification", split="test", **dataset_config)

model = build_model(name, id2label=train_dataset.id2label)
optimizer = build_optimizer("adamw", model.parameters(), lr=2e-5)
lr_scheduler = build_scheduler("reduce_on_plateau", optimizer=optimizer)

train_config = TrainConfig(
    name=name,
    device="cuda",
    init_weights_from="hezar-ai/distilbert-base-fa",
    batch_size=16,
    num_train_epochs=10,
    checkpoints_dir="checkpoints/",
    metrics={"f1": {"task": "multiclass"}},
)

trainer = Trainer(
    config=train_config,
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=train_dataset.data_collator,
    optimizer=optimizer,
    lr_scheduler=lr_scheduler,
)
trainer.train()
