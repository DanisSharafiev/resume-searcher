from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from config.config import Config

def get_tokenizer():
    return AutoTokenizer.from_pretrained(
        Config.MODEL_NAME,
        trust_remote_code=True
        )

def get_model():
    return AutoModelForCausalLM.from_pretrained(
        Config.MODEL_NAME, torch_dtype=torch.float16,
        trust_remote_code=True
        )