from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from config.config import Config

def get_tokenizer():
    return AutoTokenizer.from_pretrained(
        Config.MODEL_NAME,
        trust_remote_code=True
        )

def get_model():
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        Config.MODEL_NAME,
        torch_dtype=dtype,
        trust_remote_code=True,
        low_cpu_mem_usage=True
    )
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return model.to(device)