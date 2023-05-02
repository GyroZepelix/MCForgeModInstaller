import json
import requests
from bs4 import BeautifulSoup
from URLManipulator import AUTH_HEADER, get_filesearch_url, get_modsearch_url



QUERIES_MOD_SEARCH = {
    'gameId': 432,
    'modLoaderType': 1,
    'gameVersionTypeId': 73250
}
QUERIES_FILE_SEARCH = {
    'gameVersionTypeId' : 73250,
    'modLoaderType': 1,
}

detected_mods = []
base_url = 'https://www.curseforge.com/minecraft/mc-mods/'
files_dir = '/files'
files_to_download = {}
dependencies_to_download = {}

with open('mods.txt', 'r') as f:
    line_number = 0
    for line in f:
        line_number += 1
        if line.startswith("#"):
            continue
        try:
            link = line.split()[0]
            last_part = link.split('/')[-1]
            detected_mods.append(last_part + "\n")
            print(last_part)
        except:
            print(f"Error processing line [{line_number}]: {line} ")
    f.close()

print("-------------[ Extracting mods finished ]------------\n")

with open('extracted_mods.txt', 'w') as f:
    f.writelines(detected_mods)
    f.close()
        
for mod_name in detected_mods:
    mod_search_query = QUERIES_MOD_SEARCH.copy()
    mod_name_without_newline = str.split(mod_name, '\n')[0]
    mod_search_query['slug'] = mod_name_without_newline

    mod_search_url = get_modsearch_url(mod_search_query)

    response = requests.get(mod_search_url, headers=AUTH_HEADER)

    if response.status_code == 200:
        json_mod_search = json.loads(response.content)
        try:
            mod_id = json_mod_search['data'][0]['id']
            
            file_search_url = get_filesearch_url(mod_id, QUERIES_FILE_SEARCH)

            file_response = requests.get(file_search_url, headers=AUTH_HEADER)
            if file_response.status_code == 200:
                json_file_search = json.loads(file_response.content)
                file_id = json_file_search['data'][0]['modId']
                files_to_download[mod_id] = file_id
                print(f"{mod_name_without_newline} | {mod_id} : {file_id}")
                dependencies = json_file_search['data'][0]['dependencies']
                for dependencie in dependencies:
                    dep_mod_id = dependencie['modId']
                    dep_file_response = requests.get(get_filesearch_url(dep_mod_id, QUERIES_FILE_SEARCH), headers=AUTH_HEADER)
                    if dep_file_response.status_code == 200:
                        dep_json_file_search = json.loads(dep_file_response.content)
                        dep_file_id = dep_json_file_search['data'][0]['modId']
                        dependencies_to_download[dep_mod_id] = dep_file_id
                        print(f"    {dep_json_file_search['data'][0]['displayName']} | {dep_mod_id} : {dep_file_id}")
        except:
            print(f"Error processing mod {mod_name}")

with open('files_to_download.txt', 'w') as f:
    f.write("ModID : FileID\n")
    for key in files_to_download.keys():
        f.write(str(key) + " : " + str(files_to_download[key]) + "\n")
    f.write("\n\n")
    f.write("Dependencies:\n")
    f.write("ModID : FileID\n")
    for key in dependencies_to_download.keys():
        f.write(str(key) + " : " + str(dependencies_to_download[key]) + "\n")
    f.close()


print("-------------[ File search finished ]------------\n")

