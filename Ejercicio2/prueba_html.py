import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_requests_bcra():
    url = "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables_datos.asp"
    params = {"serie": "7927"}
    response = requests.get(url, params=params, verify=False)
    
    print("Status code:", response.status_code)
    print("Primeros 2000 caracteres del HTML:\n")
    print(response.text[:2000])

if __name__ == "__main__":
    test_requests_bcra()
