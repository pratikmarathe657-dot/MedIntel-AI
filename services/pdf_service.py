import fitz


def extract_text(file_path):

    doc = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(doc, start=1):

        text = page.get_text().strip()

        if text:

            pages.append({
                "page": page_number,
                "text": text
            })

    doc.close()

    return pages