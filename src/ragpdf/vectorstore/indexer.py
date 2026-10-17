from rich.console import Console

from ragpdf.chunking.chunker import chunk_documents
from ragpdf.embeddings.embedder import embed_texts
from ragpdf.ingestion.loader import load_all_pdfs
from ragpdf.vectorstore.chroma_store import ChromaStore

console= Console()

def build_index(reset:bool=True)-> ChromaStore:
    "load pdfs -> chunk -> chunk -> embed -> store. Returns the vectore store"
    store = ChromaStore()

    if reset:
        console.print("[yellow]Resetting collection...[/yellow]")
        store.reset()

    docs=load_all_pdfs()
    if not docs:
        console.print("[red]No documents to index.[/red]")
        return store
    console.print(f"[bold]Loaded {len(docs)} pages[/bold]")

    chunks = chunk_documents(docs)
    console.print(f"[bold]Created {len(chunks)} chunks[/bold]")

    console.print("[bold]Embedding...[/bold]")
    embeddings = embed_texts([c.text for c in chunks])

    console.print("[bold]Storing in ChromaDB...[/bold]")
    store.add_chunks(chunks, embeddings)

    console.print(f"[green]✓ Indexed {store.count()} chunks[/green]")

    return store
    