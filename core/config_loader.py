import os
import yaml
from dotenv import load_dotenv

class ConfigLoader:
    def __init__(self, config_path="config.yaml", env_path=".env"):
        self.load_from_yaml(config_path)
        self.load_from_env(env_path)

    def load_from_yaml(self, config_path="config.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        self.drive_folder_id = config["google_drive"]["folder_id"]

        self.ollama_base_url = config["ollama"]["base_url"]
        self.default_model = config["ollama"]["default_model"]
        self.embedding_model = config["ollama"]["embedding_model"]
        self.available_models = config["ollama"]["available_models"]

        self.chunk_size = config["chunking"]["chunk_size"]
        self.chunk_overlap = config["chunking"]["chunk_overlap"]

        self.chroma_path = config["storage"]["chroma_path"]

        self.top_k = config["retrieval"]["top_k"]

        self.max_history_turns = config["memory"]["max_history_turns"]

    def load_from_env(self, path=".env"):
        load_dotenv(dotenv_path=path)
        self.credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        