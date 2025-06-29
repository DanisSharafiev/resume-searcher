from fastapi import APIRouter, Request
from api.v1.models.base_model import LLMRequest
from config.prompts import LLMPrompts

router = APIRouter()

@router.post("/generate")
async def generate(request: Request, data: LLMRequest):
    tokenizer = request.app.state.tokenizer
    model = request.app.state.model
    prompt = LLMPrompts.request_prompt + f'"{data.query}"'
    input_ids = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**input_ids, max_new_tokens=100, do_sample=True, temperature=0.7)
    text = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"response": text}