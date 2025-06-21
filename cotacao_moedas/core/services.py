import requests
from datetime import timedelta, date, datetime

class VatComplyService:
    # CORREÇÃO CRÍTICA AQUI: Usar a URL correta para as taxas de câmbio
    BASE_URL = "https://api.vatcomply.com/rates"
    TARGET_CURRENCIES = ['BRL', 'EUR', 'JPY']
    BASE_CURRENCY = 'USD'

    def get_daily_rates(self, target_date):
        """
        Para obter as cotações para uma data específica.
        O argumento target_date deve ser um objeto date.
        """
        date_str = target_date.strftime('%Y-%m-%d')
        params = {
            'base': self.BASE_CURRENCY,
            'date': date_str
        }
        try:
            print(f"DEBUG (VatComplyService): Buscando cotações para a data: {date_str} com base={self.BASE_CURRENCY}...") # DEBUG
            print(f"DEBUG (VatComplyService): URL da requisição: {self.BASE_URL}?base={self.BASE_CURRENCY}&date={date_str}") # DEBUG

            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status() # Lança um erro para status codes 4xx/5xx

            data = response.json()
            print(f"DEBUG (VatComplyService): Resposta JSON bruta da API para {date_str}: {data}") # DEBUG

            rates = {}
            if 'rates' in data:
                # Sua correção de 'ratrs' para 'rates' já estava no seu código.
                # Apenas confirmando que 'rates' está correto.
                for currency in self.TARGET_CURRENCIES:
                    if currency in data['rates']:
                        rates[currency] = data['rates'][currency]
                    else: # Adiciona depuração para moedas faltantes
                        print(f"DEBUG (VatComplyService): Moeda {currency} não encontrada nas taxas para {date_str}.")
            else: # Adiciona depuração para caso 'rates' não esteja na resposta
                print(f"DEBUG (VatComplyService): Chave 'rates' não encontrada na resposta da API para {date_str}.")

            return {
                'date': date_str,
                'rates': rates
            }            
        except requests.exceptions.RequestException as e:
            # Imprime o erro de forma mais detalhada para depuração
            print(f"DEBUG (VatComplyService): Erro na requisição HTTP para a data {date_str}: {e}") # DEBUG
            if response is not None:
                print(f"DEBUG (VatComplyService): Status Code: {response.status_code}") # DEBUG
                print(f"DEBUG (VatComplyService): Resposta da API (texto): {response.text}") # DEBUG
            return None # Retorna None em caso de erro na requisição

    # O método 'get_rates_for_period' já estava corretamente indentado no seu services.py
    # Mantenho as 'correções' que você tinha, embora elas fossem comentários.
    def get_rates_for_period(self, start_date, end_date):
        """
        Para obter cotações para um período específico.
        start_date e end_date devem ser objetos date.
        """
        all_rates = []
        current_date = start_date

        while current_date <= end_date:
            # Condição para apenas dias de semana (Segunda a Sexta)
            if current_date.weekday() < 5: # 0=seg, 1=ter, 2=qua, 3=qui, 4=sex, 5=sab, 6=dom
                print(f"DEBUG (get_rates_for_period): Processando dia útil: {current_date}") # DEBUG
                daily_rates = self.get_daily_rates(current_date)
                if daily_rates: # Adiciona apenas se daily_rates não for None (ou seja, se a requisição foi bem-sucedida)
                    all_rates.append(daily_rates)
                else: # DEBUG
                    print(f"DEBUG (get_rates_for_period): Nenhuma cotação válida retornada para {current_date}.")

            # Sempre avançar o dia, mesmo que não seja dia útil (para não entrar em loop infinito)
            current_date += timedelta(days=1)

        return all_rates