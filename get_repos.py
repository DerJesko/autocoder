import requests
r = requests.get('https://api.github.com/search/repositories?q=language:C license:mit&sort=stars&sort=stars&per_page=50').json()["items"]
for i in r:
    print(i["html_url"])