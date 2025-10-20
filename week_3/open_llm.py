from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer, BitsAndBytesConfig
import os
import torch

class OpenLLMModel:
    def __init__(self, model):
        self.model = model
        hf_token = os.getenv('HF_TOKEN')
        if hf_token:
            login(token=hf_token, add_to_git_credential=True)
            print("Successfully connected")
        else:
            print("Hugging face token is missing!!!")


        self.quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_quant_type='nf4'
        )

    """
   Generate text using the specified model.

   Args:
       messages: list of dicts (chat-style input)
           Example: [{"role": "user", "content": "Hello!"}]
       quantz: bool - Whether to load the model in 4-bit mode
       max_new_tokens: int - Number of tokens to generate
   """

    def generate(self, messages, quantz=False, max_new_tokens=80):
        if quantz:
            new_model = AutoModelForCausalLM.from_pretrained(
                self.model,
                quantization_config=self.quant_config,
                device_map='auto'
            )
        else:
            new_model = AutoModelForCausalLM.from_pretrained(self.model, device_map='auto')

        tokenizer = AutoTokenizer.from_pretrained(self.model)
        tokenizer.pad_token = tokenizer.eos_token

        inputs = tokenizer.apply_chat_template(
            messages,
            return_tensors='pt',
            add_generation_prompt=True
        ).to(new_model.device)

        streamer = TextStreamer(tokenizer)

        output = new_model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            streamer=streamer,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        return tokenizer.decode(output[0][inputs.shape[-1]:], skip_special_tokens=True)

