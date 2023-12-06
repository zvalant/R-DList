import requests

parts = [4025036482]
for part in parts:
    api_url = f"http://kc-qadtst-01:9080/qadui/cgi-bin/cgiip/WService=ws-default/us/xx/xxgetitemdata.p?item={part}"
    json_response = requests.get(api_url)
    if json_response.status_code == 200:
        data = json_response.json()
        if "ItemBOM" in data["ItemInv"][0]:
            print(f"part {part} has BOM of {data['ItemInv'][0]['ItemBOM']}")


        else:
            print(f"part {part } is a base component")


