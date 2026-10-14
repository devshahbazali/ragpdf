from ragpdf.config import settings

DEFGAULT_SAPARATERS=["\n\n","\n", ". ", "! ", "? ", "; ", ", ", " ", ""]

def _split_recursive(text :str, 
                     separators:list[str],
                     chunk_size:int)->list[str]:
    
    if len(text)<=chunk_size:
        return text

    if not separators:
        return  [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    #save the first saparater in sep and remaining in rest variable
    sep, *rest = separators
   
    # Empty separator → hard split (last resort)
    if sep == "":
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    #split the full text into parts according to saparater like ("\n")
    parts=text.split(sep)

   # Re-attach the separator to each part end e.g.(".")(except the last) so we don't lose it
    pieces = [p + sep for p in parts[:-1]] + [parts[-1]]

    chunks: list[str] = []
    #buffer to save the chunk temprorary
    buffer = ""

    for piece in pieces:
        #if the buffer + next piece is < chunksize add piece to buffer 
        if len(buffer) + len(piece)<=chunk_size:
            buffer+=piece
        #adding chunk into buffer exceed chunk_size limit now
        else:

            #if buffer has
            #  some pieces then add 
            # it to chunks without this new piece
            if buffer:
                chunks.append(buffer)
            # If a single piece is bigger than chunk_size, 
            # recurse with finer separators(means with next saparater in list )
            if len(piece)>chunk_size:
                #make small pieces and add to chunks
                chunks.extend(_split_recursive(piece,rest,chunk_size))
                #reset buffer to empty because that piece is added
                buffer=""
            #if piece length is smaller then chunk then save it in a buffer
            else:
                buffer=piece

        #if there is a buffer add to the chunk
        if buffer:
            chunks.append(buffer)
        return chunks

def split_text(text:str,
               chunk_size:int|None=None,
               chunk_overlap: int | None = None)->list[str]:
    chunk_size= chunk_size or settings.chunk_size
    chunk_overlap= chunk_overlap or settings.chunk_overlap

    raw_chunks=_split_recursive(text,DEFGAULT_SAPARATERS,chunk_size)
    #removing the white spaces from chunks
    raw_chunks=[c.strip() for c in raw_chunks if c.strip()]

    if chunk_overlap<=0 or len(raw_chunks)<=1:
        return raw_chunks
    
    overlapped:list[str]=[raw_chunks[0]]
    #apply overlap: combine the tial of previous chunk to next chunk
    for i in range(1,len(raw_chunks)):
        #get the number of chars at end of chunk = chunkoverlap
        prev_tail= raw_chunks[i-1][-chunk_overlap:]
        overlapped.append((prev_tail+raw_chunks[i]).strip())

    return overlapped