from typing import List, Union

import numpy as np
import torch

from ....constants import Backends
from ....registry import register_model
from ....utils import is_backend_available
from ...model import GenerativeModel
from ...model_outputs import Image2TextOutput
from .beit_roberta_image2text_config import BeitRobertaImage2TextConfig


if is_backend_available(Backends.TRANSFORMERS):
    from transformers import (
        BeitConfig,
        BeitModel,
        GenerationConfig,
        RobertaConfig,
        RobertaForCausalLM,
        VisionEncoderDecoderModel,
    )

if is_backend_available(Backends.PILLOW):
    from PIL import Image

_required_backends = [
    Backends.TRANSFORMERS,
    Backends.TOKENIZERS,
    Backends.PILLOW
]


@register_model("beit_roberta_image2text", config_class=BeitRobertaImage2TextConfig)
class BeitRobertaImage2Text(GenerativeModel):
    """
    BEiT + RoBERTa for image to text
    """
    required_backends = _required_backends
    image_processor = "image_processor"
    tokenizer = "bpe_tokenizer"

    def __init__(self, config: BeitRobertaImage2TextConfig, **kwargs):
        super().__init__(config, **kwargs)
        encoder = BeitModel(config=BeitConfig(**self.config.encoder))
        decoder = RobertaForCausalLM(config=RobertaConfig(**self.config.decoder))
        self.beit_roberta = VisionEncoderDecoderModel(encoder=encoder, decoder=decoder)

    def forward(
        self,
        pixel_values,
        decoder_input_ids=None,
        decoder_attention_mask=None,
        encoder_outputs=None,
        past_key_values=None,
        decoder_inputs_embeds=None,
        labels=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        **kwargs,
    ):

        outputs = self.beit_roberta(
            pixel_values=pixel_values,
            decoder_input_ids=decoder_input_ids,
            decoder_attention_mask=decoder_attention_mask,
            encoder_outputs=encoder_outputs,
            past_key_values=past_key_values,
            decoder_inputs_embeds=decoder_inputs_embeds,
            labels=labels,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
        )

        return outputs

    def generate(self, pixel_values, generation_config=None, **kwargs):
        if generation_config is None:
            generation_config = self.config.dict()["generation"]
        generation_config = GenerationConfig(**generation_config)
        outputs = self.beit_roberta.generate(inputs=pixel_values, generation_config=generation_config, **kwargs)

        return outputs

    def preprocess(self, inputs: Union[List[str], List[np.ndarray], List["Image"], List[torch.Tensor]], **kwargs):
        image_processor = self.preprocessor[self.image_processor]
        processed_outputs = image_processor(inputs, **kwargs)
        return processed_outputs

    def post_process(self, model_outputs, **kwargs):
        tokenizer = self.preprocessor[self.tokenizer]
        decoded_outputs = tokenizer.decode(model_outputs.cpu().numpy().tolist())
        return Image2TextOutput(texts=decoded_outputs)