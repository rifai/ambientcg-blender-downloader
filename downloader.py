import bpy
import os

import requests
import urllib.request 
from zipfile import ZipFile

directory = bpy.path.abspath("//textures")


def retrieve_assets_info(per_page, page):
    
    offset = str(page * per_page)
    # The API endpoint
    url = "https://ambientCG.com/api/v2/full_json?limit="+str(per_page)+"&offset="+ offset
    
    print("============================== retrieve assetsaa "+url)
    # A GET request to the API
    response = requests.get(url)
    
    assets = response.json()["foundAssets"]
    
#    print(assets)
    
#    for fl in assets:
#        print(fl["assetId"])
        
    if len(assets) > 0:
        selected = assets[0]
        print(selected)
        as_id = selected["assetId"]
        asset_req_url = "https://ambientCG.com/api/v2/downloads_csv?id="+as_id
        response = requests.get(asset_req_url)
        content = response.text
        print(content)
        
        csv = content.splitlines()
        if len(csv) > 1:
            content_line = csv[1]
            url_download = content_line.split(",")[5]
            retrieve_asset(url_download)
            

def retrieve_asset(url_download):
    my_file = download_file(url_download)
    dir_name = extract_file(my_file)
    load_images(dir_name)
            
def extract_file(my_file):
    with ZipFile(my_file, 'r') as zObject:

        dir_name = os.path.dirname(my_file)
        new_folder = os.path.basename(my_file).split('.')[0]
        dir_name = os.path.join(dir_name, new_folder)
    
        print("extract "+my_file+" to "+dir_name)
        zObject.extractall(path=dir_name)
        return dir_name
    
def download_file(url_download):
    file_name = bpy.path.basename(url_download)
    file_name = os.path.join(directory, file_name)
    print("url = "+url_download)
    print("base name = "+file_name)
    
    if os.path.exists(file_name):
        print("EXIST "+file_name)
        return file_name
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(url_download, file_name)
    
    return file_name
    
def load_images(dir_name):
    
    files = os.listdir(dir_name)

    print("eksekusi "+dir_name)
    for content in files:
        path = os.path.join(dir_name, content)
        if os.path.isfile(path):
            if ".jpg" in content:
                print("loaded "+path) 
                bpy.data.images.load(path, check_existing=True)


if not os.path.exists(directory):
    print("blm ada dir "+directory)
    os.mkdir(directory)

retrieve_assets_info(10, 0) 