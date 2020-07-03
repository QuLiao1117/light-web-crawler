import requests
def geocodeB(address):
    base = url = "http://api.map.baidu.com/geocoder?address=" + address + "&output=json&key=1hGi2uRbG7G4ZOviGfHF6ozqeo27WE7l"
    response = requests.get(base)
    answer = response.json()
    return answer['result']['location']['lng'],answer['result']['location']['lat']