import requests

def retornar_endereco(lat: float, lon:float):
    url = f"https://us1.locationiq.com/v1/reverse?key=pk.2e0b69dc21fd347754965a4b9d94bd92&lat={lat}&lon={lon}&format=json&"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Erro: {e}')
        return None
    