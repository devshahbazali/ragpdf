from functools import lru_cache
from sentence_transformers import SentenceTransformer
from ragpdf.config import settings

@lru_cache(maxsize=1)
def get_model()->SentenceTransformer:
    "loading the embedding model once then caching it with decorator"
    "so when next all happens the cached modle is returned"
    return SentenceTransformer(settings.embedding_model)

def embed_texts(texts:list[str],batch_size:int=32)->list[list[float]]:
    model=get_model()
    Vectors=model.encode(texts,batch_size=batch_size,
                         show_progress_bar=len(texts)>100,
                         convert_to_numpy=True,
                         normalize_embeddings=True)
    return Vectors.tolist()

def embed_query(text:str)->list[float]:
    return embed_texts([text])[0]