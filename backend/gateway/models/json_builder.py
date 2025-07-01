class JsonMaker:
    @staticmethod
    def make_llm_response(llm_response: str, resume_plain: str) -> str:
        return {
            "llm_response_markdown": llm_response,
            "resume_plain": resume_plain
        }
