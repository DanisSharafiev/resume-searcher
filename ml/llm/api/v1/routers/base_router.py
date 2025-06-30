from fastapi import APIRouter, Request
from api.v1.models.base_model import LLMRequest
import torch

router = APIRouter()

@router.post("/generate")
async def generate(request: Request, data: LLMRequest):
    tokenizer = request.app.state.tokenizer
    model = request.app.state.model
    device = next(model.parameters()).device
    inputs = tokenizer(data.query, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=100, do_sample=True, temperature=0.7)
    output = output[0, inputs['input_ids'].shape[1]:]
    text = tokenizer.decode(output, skip_special_tokens=True)
    return {"response": text}