import requests
import json

url = "https://open.larksuite.com/open-apis/bitable/v1/apps/SAnmbQyfMaOxOzsgxcMlBZ9WgQh/tables/tbl99icrL05oBYDr/records/search"
payload = json.dumps({
	"filter": {
		"conditions": [
			{
				"field_name": "Tình trạng",
				"operator": "is",
				"value": [
					"Chốt"
				]
			}
		],
		"conjunction": "and"
	}
})


headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer t-g20669eGRMG4Y6AF36LXBYLAYP3BJYRYOMNDUTXM'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)