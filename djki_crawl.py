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

def csv_ary(dic):
    ret = []
    for item in items:
        if item in dic:
            ret.append(dic[item])
        else:
            ret.append('')
    return ret

num = int(input())

csv_result = []
with open('number' + str(num) + '.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        try:
            http = urllib3.PoolManager()
            url =  f'https://pdki-indonesia.dgip.go.id/index.php/paten?q={line[0]}&type=1'
            print(url)
            response = http.request('get', url)
            soup = BeautifulSoup(response.data, 'html.parser')
            dom = html.fromstring(str(soup))
            link = dom.xpath('/html/body/div[3]/ul/li/div[2]/a')
            if link:
                result = {'Appnum': line[0]}
                detail_url = link[0].get('href')
                response = http.request('get', detail_url)
                soup = BeautifulSoup(response.data, 'html.parser')
                dom = html.fromstring(str(soup))

                rows = soup.find_all('div', {'class': 'span-1'})
                if rows:
                    for r in rows:
                        title = r.find('span', {'class': 'title'})
                        value = r.find('p', {'class': 'value'})
                        status = r.find('span', {'class' : 'status'})
                        ni = r.find('h2', {'class': 'ni'})
                        # print(title)
                        if title:
                            t = title.get_text()
                            if t == 'NOMOR PATEN' or t == 'NOMOR PERMOHONAN':
                                if ni:  
                                    result[t] = ni.get_text()
                            elif t == 'STATUS':
                                if status:
                                    result[t] = status.get_text()
                            elif t != 'GAMBAR':
                                if value:  
                                    result[t] = value.get_text()
                        
                spans = soup.find_all('div', {'class': 'span-3'})
                priority = spans[2].find_all('ul')[1].find_all('p', {'class': 'value-u'})
                p_s = [p.get_text().strip() for p in priority]
                result['Prioritas'] = ' '.join(p_s) + '\n'
                
                p_ul = spans[4].find_all('ul')
                pg_ret = []
                for i in range(1,len(p_ul)):
                    tmp_p = p_ul[i].find_all('p', {'class': 'value-u'})
                    pg_ret.append(tmp_p[0].get_text().strip())
                
                result['Pemegang Paten'] = '\n'.join(pg_ret)

                # # 登録日
                date = dom.xpath('/html/body/div[4]/div/div[1]/div[1]/div[2]/span[2]')
                if date:
                    result['TANGGAL PEMEBERIAN'] = date[0].text.strip()

                # # Status
                status = dom.xpath("//span[@class='status']")
                if status:
                    result['STATUS'] = status[0].text

                #IPC
                ipcs = soup.find_all('span', {'class': 'value-ipc'})
                ipc_list = []
                for ipc in ipcs:
                    ipc_list.append(ipc.get_text())
                result['IPC'] = ','.join(ipc_list)
                
                csv_result.append(csv_ary(result))

                if len(csv_result) == 50:
                    with open('out'+ str(num) + '.csv', 'a', encoding='utf-8', newline='') as f:
                        dataWriter = csv.writer(f)
                        dataWriter.writerow(items)
                        dataWriter.writerows(csv_result)
                    csv_result = []
            
        except:
            with open('djki_error'+ str(num) + '.log', mode='a') as f:
                f.write(line[0] +'\n')


