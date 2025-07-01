from config.prompts import LLMPrompts

class SearchModel:
    def __init__(self, llm_model, qdrant_model):
        self.llm_model = llm_model
        self.qdrant_model = qdrant_model
    
    def search(self, query):
        llm_response = self.llm_model.get_response(LLMPrompts.request_prompt + query)
        search_results = self.qdrant_model.search(llm_response["data"])
        return search_results