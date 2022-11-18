import requests, json, re


def main():
    name = input("Company name: ")
    address = get_data(cik_lookup(name))
    for i in address.values():
        print(i)
    
def get_data(cik):
    cSlice = cik[0]
    cleanZero = 0
    if(len(cik) < 10):
        cleanZero = 10 - len(cSlice)
        for i in range(cleanZero):
            cSlice = '0' + cSlice

    url = (f'https://data.sec.gov/submissions/CIK{cSlice}.json')
    headers = {'User-Agent': '<YOUR NAME> <YOUR EMAIL>', 'Accept-Encoding': 'gzip, deflate'}
    r = requests.get(url, headers=headers).text
    data = json.loads(r)
    address = {'street' : data['addresses']['business']['street1'],
    'city' : data['addresses']['business']['city'],
    'state' : data['addresses']['business']['stateOrCountry'],
    'zip' : data['addresses']['business']['zipCode'] }
    return address

def cik_lookup(name):
    url = f'https://www.sec.gov/cgi-bin/browse-edgar?company={name}&match=starts-with&filenum=&State=&Country=&SIC=&myowner=exclude&action=getcompany'
    headers = {'User-Agent': '<Company name> <your@email.com>', 'Accept-Encoding': 'gzip, deflate'}
    r = requests.get(url, headers=headers).text
    cik = re.findall('(?<=CIK=)[^&]*', r)
    return cik

main()
