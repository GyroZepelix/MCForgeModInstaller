if __name__ == "__main__":
    print("This file is not meant to be run as a script.")
    exit()

BASE_URL = "https://api.curseforge.com"
API_KEY = ''

ENDPOINT_MOD_SEARCH = "/v1/mods/search"
def ENDPOINT_FILE_SEARCH(modID):
    return "/v1/mods/" + str(modID) + "/files"



AUTH_HEADER = {'x-api-key': API_KEY}

def build_query(params):
    query_string = '&'.join(map(lambda item: f"{item[0]}={item[1]}", params.items()))
    return "?"+query_string

def build_final_url(base_url, endpoint, queries):
    return base_url + endpoint + queries

def get_modsearch_url(queries):
    return build_final_url(BASE_URL, ENDPOINT_MOD_SEARCH, build_query(queries))

def get_filesearch_url(modid, queries):
    return build_final_url(BASE_URL, ENDPOINT_FILE_SEARCH(modid), build_query(queries))