import requests
import zipfile, io
import pathlib
import os

# url = r"http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais?tipo=2&documentos=46400000"
url = r"http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais?tipo=2&documentos=46400000"

path_folder = pathlib.Path(r"C:\Users\Usuario\Desktop\lhc_hidroweb")
try:
    os.mkdir(pathlib.Path(path_folder))
except:
    pass
r = requests.get(url)
print(r.status_code)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall(path_folder)


for path, dir_list, file_list in os.walk(path_folder):
    for file_name in file_list:
        if file_name.endswith(".zip"):
            abs_file_path = os.path.join(path, file_name)

            # The following three lines of code are only useful if
            # a. the zip file is to unzipped in it's parent folder and
            # b. inside the folder of the same name as the file

            parent_path = os.path.split(abs_file_path)[0]
            output_folder_name = os.path.splitext(abs_file_path)[0]
            output_path = os.path.join(parent_path, output_folder_name)

            zip_obj = zipfile.ZipFile(abs_file_path, 'r')
            zip_obj.extractall(output_path)
            zip_obj.close()
            os.remove(abs_file_path)
