from sentence_transformers import SentenceTransformer
from config.config import Config
 
class Embedder:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("initializing embedder model")
        self.embedder_model = self.load_model()
        self.logger.info("embedder model initialized")
    
    def load_model(self):
        self.logger.info("Loading embedder model...")
        model = SentenceTransformer(Config.MODEL_NAME)
        return model
    
    def encode(self, text):
        self.logger.info("Encoding text...")
        embedding = self.embedder_model.encode(text)
        self.logger.info("Text encoded successfully")
        return embedding