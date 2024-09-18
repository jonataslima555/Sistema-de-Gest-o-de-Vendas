from dotenv import load_dotenv
from os import getenv
from requests import get

load_dotenv()

API_KEY = getenv('API_KEY')

# Consultar CEP #
def get_cep(cep):
    if not API_KEY:
        print("Erro: API_KEY não está definida.")
        return False  # Retorna False se não há API_KEY

    url = f'https://api.invertexto.com/v1/cep/{cep}'
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
        response = get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            # Extraindo dados específicos para formatação
            state = data.get('state', 'N/A')
            city = data.get('city', 'N/A')
            neighborhood = data.get('neighborhood', 'N/A')
            street = data.get('street', 'N/A')

            # Formatando a saída
            formatted_data = (f"CEP: {cep}\n"
                              f"ESTADO: {state}\n"
                              f"CIDADE: {city}\n"
                              f"BAIRRO: {neighborhood}\n"
                              f"RUA: {street}")
            
            print(formatted_data)
            return True  # Retorna True se o CEP foi validado com sucesso
        else:
            print(f"Erro: {response.status_code} - {response.text}")
            return False  # Retorna False se houve um erro na consulta
    except Exception as e:
        print(f"Erro ao tentar conectar à API: {e}")
        return False  # Retorna False se houve uma exceção

# Exemplo de uso
#get_cep('41481047')
