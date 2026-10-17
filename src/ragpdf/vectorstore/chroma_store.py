from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from ragpdf.chunking.models import chunk
from ragpdf.config import settings

COLLECTION_NAME="ragpdf"
METADATA={"hnsw:space": "cosine"}
class ChromaStore:
    def __init__(self,persist_dir:Path|None=None)->None:
        persist_dir=persist_dir or settings.chroma_dir
        persist_dir.mkdir(parents=True,exist_ok=True)
        
        self.client=chromadb.PersistentClient(
            path=str(persist_dir),
            settings=ChromaSettings(anonymized_telemetry=False))

        self.collection=self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata=METADATA# using cosine distance
        )

    def count(self)->int:
        return self.collection.count()

    def reset(self)->None:
        self.client.delete_collection(COLLECTION_NAME)
        self.collection=self.client.get_or_create_collection(
            name=COLLECTION_NAME,metadata=METADATA)

    def add_chunks(self, chunks:list[chunk],embeddings:list[list[float]])->None:
        "Add chunks as there respective embeddings to the db"
        if len(chunks)!=len(embeddings):
            raise ValueError("chunks and embeddings are not the same length")

        self.collection.add(
            ids=[c.chunk_id for c in chunks],
            documents=[c.text for c in chunks],
            embeddings=embeddings,
            metadatas=[{"source":c.source,
                        "page":c.page,
                        "chunk_index":c.chunk_index,
                        "total_pages":c.total_pages} for c in chunks]
        )

    def query(self,query_embedding:list[float],top_k=5)->list[dict[str,Any]]:
        "this function will return the top_k most similar chunks from db"
       
        results=self.collection.query(query_embeddings=query_embedding,
                                      n_results=top_k,
                                      include= ["metadatas", "documents", "distances"])

        hits:list[dict[str,Any]]=[]

        for i in range(len(results["ids"][0])):
            hits.append(
                {
                    "id": results["ids"][0][i],
                    "text":results["documents"][0][i],
                    "metadata":results["metadatas"][0][i],
                    "distance":results["distances"][0][i]
                }
            )
        return hits
