from ragpdf.chunking.models import chunk
from ragpdf.chunking.splitter import split_text
from ragpdf.ingestion.models import Document

def _chunk_document(doc:Document,chunk_size:int|None=None,
                   chunk_overlap:int | None=None)->list[chunk]:
    pieces=split_text(doc.text,chunk_size=chunk_size,chunk_overlap=chunk_overlap)

    return[
        chunk(
            text=piece,
            source=doc.source,
            page=doc.page,
            total_pages=doc.total_pages,
            chunk_index=i
        )

        for i ,piece in enumerate(pieces)
    ]


def chunk_documents(docs:list[Document],
                   chunk_size: int | None = None,
                    chunk_overlap: int | None = None):

    all_chunks:list[chunk]=[]

    for doc in docs:
        all_chunks.extend(_chunk_document(doc,chunk_size=chunk_size
                                         ,chunk_overlap=chunk_overlap))

    return all_chunks