from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",
                                    env_file_encoding="utf-8",
                                    extra="ignore")
    #now if the variables have some values in the .env file
    #then the following variable will be overridden from env
      # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"

    # Storage
    chroma_dir: Path = Path("data/chroma")
    pdf_dir: Path = Path("data/pdfs")

    # Chunking / retrieval
    chunk_size: int = 800
    chunk_overlap: int = 150
    top_k: int = 5

settings=Settings()
