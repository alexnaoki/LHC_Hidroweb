import requests
import zipfile, io
import pathlib
import os

# Input Data
station_code_list = [539037, 36470000, 539078, 36460001, 538087, 36580000, 36586000, 538090, 539083, 539053, 36520000, 36515000, 538034, 539000, 439000, 36521000, 36520200, 36525000, 539049, 36595000, 36598000, 438030, 36590000, 36585000, 439077, 439076, 439064, 439063, 439062, 439082, 539070, 539002, 539073, 539086, 539044, 539047, 539048, 539045, 36470001, 36460000, 539022, 539034, 539038, 440011, 440025, 538000, 538014, 538019, 36584000, 439028, 539024, 539025, 539050, 539010, 539017, 36520001, 439004, 539019, 539080, 539081, 538092, 538093, 538094, 538095, 438045, 538011, 538013, 538021, 539006, 539018, 438025, 538037, 36550000, 538035, 36527000, 539042, 539009, 439039, 36500000, 439012, 539026, 539035, 539007, 539016, 439011, 439026, 438046, 438048, 36536000, 538006, 538012, 539061, 539021, 539033, 539062, 539092, 539039, 539003, 539093, 539096, 539005, 439065, 538060, 540039, 538031, 538032, 440029, 538103, 538075, 438105, 438072, 539077, 539064, 539069, 539066, 539065, 539068, 539072, 539012, 539067, 539095, 539097, 539088, 539084, 539090, 539091, 439083, 539074, 439074, 439001, 439020, 439022, 439067, 538063, 539063, 538064, 438117, 538018, 439080, 538083, 538051, 438024, 439073, 439043, 439044, 539056, 539057, 539055, 539094, 439045, 539089, 539029, 439060, 439061, 439059, 538047, 539054, 538025, 538097, 439002, 539027, 539028, 539031, 539082, 539079, 539043, 36517500, 538067, 36471000, 36594000, 539030, 539001, 539004, 539008, 539014, 36462000, 36512000, 36400000, 36461000, 36459000, 36599000, 36516000, 36593000, 36592500, 36770000, 36518000, 36519000, 36545000, 36565000, 36510000, 36490000, 36517000, 538027, 36522000, 36534000, 36458000, 539060, 539085, 539051, 539059, 540043]

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
    try:
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
    except:
        print("Error on the CODE: {}".format(code))
