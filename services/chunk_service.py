from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunk_text(pages, chunk_size=500, overlap=100):

    chunks = []

    for page in pages:

        page_number = page["page"]
        text = page["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append({
                "text": chunk,
                "page": page_number
            })

            start += chunk_size - overlap

    return chunks