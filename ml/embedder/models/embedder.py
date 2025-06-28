class Embedder:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("initializing embedder model")
        self.embedder_model = self.load_model()
        self.logger.info("embedder model initialized")
    
    def load_model(self):
        self.logger.info("Loading embedder model...")
        return True # zamenit' potom