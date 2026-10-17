from dataclasses import dataclass

from ragpdf.embeddings.embedder import embed_query
from ragpdf.vectorstore.chroma_store import ChromaStore


@dataclass
class RetrievedChunk:
    "A chunk  returned from similarity search"

    chunk_id:str
    text: str
    source: str
    page: int
    chunk_index: int
    distance: float        # cosine distance (0 = identical, 2 = opposite)
    score: float           # 1 - distance, so higher = more similar

    def __repr__(self) -> str:
        preview = self.text[:50].replace("\n", " ")
        return f"<RetrievedChunk {self.chunk_id} score={self.score:.3f}: '{preview}...'>"

class Retriever:
    "retrieve chunks from chroma db"
    
    def __init__(self, store: ChromaStore | None = None) -> None:
        self.store = store or ChromaStore()

    def retrieve(self,query:str,top_k:int=5)->list[RetrievedChunk]:
        query_vec= embed_query(query)
        hits=self.store.query(query_embedding=query_vec,top_k=top_k)

        return [RetrievedChunk(
                chunk_id=hit["id"],
                text=hit["text"],
                source=hit["metadata"]["source"],
                page=hit["metadata"]["page"],
                chunk_index=hit["metadata"]["chunk_index"],
                distance=hit["distance"],
                score=1.0 - hit["distance"],   # convert distance → similarity
            ) for hit in hits]