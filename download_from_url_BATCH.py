import requests
import zipfile, io
import pathlib
import os

# Input Data
station_code_list = [46400000, 50230000]

# Creation of Folder for the data
path_folder = pathlib.Path(r"C:\Users\Usuario\Desktop\lhc_hidroweb")
try:
    os.mkdir(pathlib.Path(path_folder))
except:
    pass

# Magic URL
url = r"http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais?tipo=2&documentos={}"

# Getting to the URL and download to the folder specified
for code in station_code_list:
    r = requests.get(url.format(code))

    # IF r.status_code == 200, it means that the request was able to be fulfilled
    print(r.status_code)

    # Unzipping the first folder and extracting on the folder
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path_folder)

    # Unzipping the rest of the Zips and deleting the Zip files
    for path, dir_list, file_list in os.walk(path_folder):
        for file_name in file_list:
            if file_name.endswith(".zip"):
                abs_file_path = os.path.join(path, file_name)
                parent_path = os.path.split(abs_file_path)[0]
                output_folder_name = os.path.splitext(abs_file_path)[0]
                output_path = os.path.join(parent_path, output_folder_name)

                zip_obj = zipfile.ZipFile(abs_file_path, 'r')
                zip_obj.extractall(output_path)
                zip_obj.close()
                os.remove(abs_file_path)
