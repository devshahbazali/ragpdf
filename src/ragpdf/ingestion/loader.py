from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError
from rich.console import Console

from ragpdf.ingestion.models import Document
from ragpdf.config import settings


console =Console()

def load_pdf(path:Path)-> list[Document]:
    #load pdf and return one document per page 
    try:
        reader=PdfReader(str(path)) 
    except PdfReadError as e:
        console.print(f"[red]Failed to read path.")
        return []

    total_pages=len(reader.pages)
    documents: list[Document]=[]
    
    for i , page in enumerate(reader.pages,start=1):
        try:
            text=page.extract_text()
        except Exception as e:
            console.print(f"[yellow]Skipping {path.name} p{i}: {e}[/yellow]")
        text=text.strip()
        if not text:
            continue
        documents.append(Document(page=i,
                                      total_pages=total_pages,
                                      source=path.name,
                                      text=text))

    return documents

def load_all_pdfs(pdf_dir:Path | None=None)->list[Document]:
    #loading all the pdf in the given directory
    pdf_dir:Path=pdf_dir or settings.pdf_dir
    
    if not pdf_dir.exists():
        console.print(f"[yellow]PDF directory not found {pdf_dir}[/yellow]")
    
    pdf_paths=sorted(pdf_dir.glob("*.pdf"))
    
    if not pdf_paths:
        console.print(f"[yellow]No PDFs found in {pdf_dir}[/yellow]")
        return[]

    all_docs:list[Document]=[]
    
    for path in pdf_paths:
        docs=load_pdf(path)
        all_docs.extend(docs)
        console.print( f"[green]✓[/green] {path.name}: "
            f"{len(docs)} pages with text")
        
    return all_docs
        