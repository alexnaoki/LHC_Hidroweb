import requests
import zipfile, io

url = r"http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais?tipo=2&documentos=46400000"
url = r"http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais?tipo=2&documentos=50230000"

r = requests.get(url)
print(r.status_code)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall(r"C:\Users\Usuario\Downloads")

print(z)
