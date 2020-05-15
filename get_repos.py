import requests
import os
import sys

urls = []
license_ = "gpl-3.0"
language = "C"
repos = requests.get('https://api.github.com/search/repositories?q=language:'
                     + language + ' license:'+ license_ +
                     '&sort=stars&sort=stars&per_page=100').json()["items"]

urls = []
for repo in repos:
    repo_name = repo["name"]
    url = repo["html_url"]
    os.system("git clone --depth=1 " + url + " " + sys.argv[1] + repo_name)
    urls.append(url)

try:
    with open("repos.txt", "w") as f:
        f.write("\n".join(urls))
except:
    print("\n".join(urls))
