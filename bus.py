import urllib.request
import urllib.parse
import json


def getBus(line_name):
    name = urllib.parse.quote(line_name)
    url = "http://apps.eshimin.com/traffic/gjc/getBusBase?name=" + name
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/11D257",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    req = urllib.request.Request(url, headers=headers)
    data = urllib.request.urlopen(req)
    bus_base = data.read().decode('utf-8')
    busbase = json.loads(bus_base)
    if 'data' in busbase:
        return '线路不存在'
    line_id = busbase['line_id']
    url1 = "http://apps.eshimin.com/traffic/gjc/getBusStop?name=" + name + '&lineid=' + line_id
    req1 = urllib.request.Request(url1, headers=headers)
    data1 = urllib.request.urlopen(req1)
    bus_stop = data1.read().decode('utf-8')
    busstop = json.loads(bus_stop)
    l0 = len(busstop['lineResults0']['stops'])
    result = line_name + '：' + busbase['start_stop'] + ' >>> ' + busbase['end_stop'] + '\n'
    result += '首班车：' + busbase['start_earlytime'] + '  末班车：' + busbase['start_latetime'] + '\n'
    for i in range(l0):
        index = busstop['lineResults0']['stops'][i]['id']
        index = index.replace('start_', '')
        url2 = "http://apps.eshimin.com/traffic/gjc/getArriveBase?name=" + name + '&lineid=' + line_id + '&direction=0&stopid=' + str(index)
        req2 = urllib.request.Request(url2, headers=headers)
        data2 = urllib.request.urlopen(req2)
        arrive_base = data2.read().decode('utf-8')
        arrivebase = json.loads(arrive_base)
        if arrivebase:
            if (arrivebase['cars'][0]['stopdis'] == '1') or (arrivebase['cars'][0]['stopdis'] == '0'):
                result += arrivebase['cars'][0]['terminal'] + ' 距离 ' + busstop['lineResults0']['stops'][i]['zdmc'] + ' ' + arrivebase['cars'][0]['distance'] + ' 米 ' + arrivebase['cars'][0]['time'] + ' 秒 ' + '\n'
    if busstop['lineResults1']['stops']:
        l1 = len(busstop['lineResults1']['stops'])
        result += '\n'
        result += line_name + '：' + busbase['end_stop'] + ' >>> ' + busbase['start_stop'] + '\n'
        result += '首班车：' + busbase['end_earlytime'] + '  末班车：' + busbase['end_latetime'] + '\n'
        for i in range(l1):
            index = busstop['lineResults1']['stops'][i]['id']
            index = index.replace('start_', '')
            url3 = "http://apps.eshimin.com/traffic/gjc/getArriveBase?name=" + name + '&lineid=' + line_id + '&direction=1&stopid=' + str(index)
            req3 = urllib.request.Request(url3, headers=headers)
            data3 = urllib.request.urlopen(req3)
            arrive_base1 = data3.read().decode('utf-8')
            arrivebase1 = json.loads(arrive_base1)
            if arrivebase1:
                if (arrivebase1['cars'][0]['stopdis'] == '1') or (arrivebase1['cars'][0]['stopdis'] == '0'):
                    result += arrivebase1['cars'][0]['terminal'] + ' 距离 ' + busstop['lineResults1']['stops'][i]['zdmc'] + ' ' + arrivebase1['cars'][0]['distance'] + ' 米 ' + arrivebase1['cars'][0]['time'] + ' 秒 ' + '\n'
    return result


if __name__ == '__main__':
    line = '01路'
    result = getBus(line)
    print(result)