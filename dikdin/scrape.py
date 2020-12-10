import requests
from bs4 import BeautifulSoup
import json

urls = [
    'http://localhost:9090/SSCASN DIKDIN.htm',
    'http://localhost:9090/SSCASN DIKDIN 2.htm',
    'http://localhost:9090/SSCASN DIKDIN 3.htm',
    'http://localhost:9090/SSCASN DIKDIN 4.htm',
    'http://localhost:9090/SSCASN DIKDIN 5.htm',
    'http://localhost:9090/SSCASN DIKDIN 6.htm',
]

results = []
for url in urls:
    res = requests.get(url)
    if (res.status_code != 200):
        print("ERROR CEK SERVER!")
        break

    html = BeautifulSoup(res.content)
    for row in html.find('tbody').find_all('tr'):
        col = row.find_all('td')
        nama_instansi   = col[0].text.strip()
        jabatan         = col[1].text.strip()
        lokasi          = col[3].text.strip()
        pendidikan      = col[4].text.strip()
        kuota           = col[5].text.strip()

        results.append({
            'nama_instansi': nama_instansi,
            'jabatan': jabatan,
            'lokasi': lokasi,
            'pendidikan': pendidikan,
            'kuota': kuota,
        })

with open('bkn.json', 'w') as f:
    f.write(json.dumps(results))