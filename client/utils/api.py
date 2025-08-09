import requests
from config import API_URL


def upload_pdfs_api(files):
    files_payload=[ ("files",(f.name,f.read(),"application/pdf")) for f in files]
    return requests.post(f"{API_URL}/upload_pdfs/",files=files_payload)

def ask_question(question):
    return requests.post(f"{API_URL}/ask_questions/",data={"question":question})



#  for all types of files


"""import requests
import mimetypes
from config import API_URL


def upload_documents_api(files):
    files_payload = []

    for f in files:
        # Guess MIME type based on file name
        mime_type, _ = mimetypes.guess_type(f.name)
        mime_type = mime_type or "application/octet-stream"  # Fallback for unknown types

        files_payload.append(("files", (f.name, f.read(), mime_type)))

    response = requests.post(f"{API_URL}/upload_documents/", files=files_payload)
    response.raise_for_status()
    return response.json()


def ask_question(question):
    response = requests.post(f"{API_URL}/ask/", json={"question": question})
    response.raise_for_status()
    return response.json()
"""