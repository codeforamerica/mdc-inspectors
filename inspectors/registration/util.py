import requests

API_URL = 'https://opendata.miamidade.gov/resource/vvjq-pfmc.json'


def is_valid_permit(id):
    # checks if the ID is a valid Miami-Dade Permit or Process Number
    API = API_URL + '?$where=permit_number=%27' + id + '%27%20or%20process_number=%27' + id + '%27'
    response = requests.get(API)
    json_result = response.json()

    return json_result is not None
