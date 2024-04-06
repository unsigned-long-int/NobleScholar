from docx import Document 

def read_doc(stream_address):
    doc = Document(stream_address)
    return ''.join(paragraph.text for paragraph in doc.paragraphs)

def read_pdf(stream_address):
    pass 

def read_ppt(stream_address):
    pass

def read_txt(stream_address):
    return None