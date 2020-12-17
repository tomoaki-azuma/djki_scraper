import pickle
import csv
from bs4 import BeautifulSoup
import urllib3
from lxml import html

items = [
    'Appnum',
    'NOMOR PATEN',
    'TANGGAL PEMBERIAN',
    'STATUS',
    'NOMOR PENGUMUMAN',
    'TANGGAL PENGUMUMAN',
    'TANGGAL PENERIMAAN',
    'TANGGAL DIMULAI PELINDUNGAN',
    'Prioritas',
    'IPC',
    'Pemegang Paten',
]

http = urllib3.PoolManager()

def csv_ary(dic):
    ret = []
    for item in items:
        if item in dic:
            ret.append(dic[item])
        else:
            ret.append('')
    return ret

def get_tanngal_pemberian(num):
    try:
        url =  f'https://pdki-indonesia.dgip.go.id/index.php/paten?q={num}&type=1'
        print(url)
        response = http.request('get', url)
        soup = BeautifulSoup(response.data, 'html.parser')
        dom = html.fromstring(str(soup))
        link = dom.xpath('/html/body/div[3]/ul/li/div[2]/a')
        if link:
            detail_url = link[0].get('href')
            response = http.request('get', detail_url)
            soup = BeautifulSoup(response.data, 'html.parser')
            dom = html.fromstring(str(soup))

            # # 登録日
            date = dom.xpath('/html/body/div[4]/div/div[1]/div[1]/div[2]/span[2]')
            if date:
                return date[0].text.strip()
            else:
                return ''
    except:
        return ''

all_num = []
with open('all_number.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        all_num.append(line[0])

data = {}
with open('get_all_data.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        data[line[0]] = line[1:]

for num in all_num:
    pemberian = get_tanngal_pemberian(num)
    result = [num] + data[num]
    result[2] = pemberian
    with open('final_result.csv', 'a', encoding='utf-8', newline='') as f:
        dataWriter = csv.writer(f)
        dataWriter.writerow(result)