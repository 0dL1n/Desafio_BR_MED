# cotacao_moedas/core/services.py
import requests
from datetime import timedelta, date, datetime
from django.db import IntegrityError 
from .models import Cotacao 

class VatComplyService:
    BASE_URL = "https://api.vatcomply.com/rates" 
    TARGET_CURRENCIES = ['BRL', 'EUR', 'JPY']
    BASE_CURRENCY = 'USD'

    def get_daily_rates(self, target_date):
        """
        Para obter as cotações para uma data específica da API externa.
        Se bem-sucedido, salva ou atualiza a cotação no banco de dados.
        Retorna o dicionário de cotações para a data ou None em caso de erro.
        """
        date_str = target_date.strftime('%Y-%m-%d')
        params = {
            'base': self.BASE_CURRENCY,
            'date': date_str
        }
        try:
            print(f"DEBUG (VatComplyService): Buscando cotações para a data: {date_str} da API externa...")
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status() # Lança um erro para status codes 4xx/5xx

            data = response.json()
            print(f"DEBUG (VatComplyService): Resposta JSON bruta da API para {date_str}: {data}")

            rates = {}
            if 'rates' in data:
                for currency in self.TARGET_CURRENCIES:
                    if currency in data['rates']:
                        rates[currency] = data['rates'][currency]
                    else:
                        print(f"DEBUG (VatComplyService): Moeda {currency} não encontrada nas taxas para {date_str}.")
            else:
                print(f"DEBUG (VatComplyService): Chave 'rates' não encontrada na resposta da API para {date_str}.")
                return None # Não há dados de cotação válidos

            # --- LÓGICA DE PERSISTÊNCIA: Salvar no banco de dados ---
            try:
                # update_or_create tenta encontrar um registro. Se encontra, atualiza; senão, cria.
                cotacao_obj, created = Cotacao.objects.update_or_create(
                    data=target_date, # Condição para encontrar o registro
                    defaults={ # Valores a serem criados/atualizados
                        'valor_brl': rates.get('BRL'),
                        'valor_eur': rates.get('EUR'),
                        'valor_jpy': rates.get('JPY'),
                    }
                )
                if created:
                    print(f"DEBUG (VatComplyService): Cotação para {date_str} SALVA com sucesso no banco de dados.")
                else:
                    print(f"DEBUG (VatComplyService): Cotação para {date_str} ATUALIZADA com sucesso no banco de dados.")
            except IntegrityError as e:
                print(f"DEBUG (VatComplyService): Erro de integridade ao salvar cotação para {date_str} (provavelmente duplicata): {e}")
            except Exception as e:
                print(f"DEBUG (VatComplyService): Erro INESPERADO ao salvar cotação para {date_str}: {e}")
            

            return {
                'date': date_str,
                'rates': rates
            }
        except requests.exceptions.RequestException as e:
            print(f"DEBUG (VatComplyService): Erro na requisição HTTP para a data {date_str}: {e}")
            if response is not None:
                print(f"DEBUG (VatComplyService): Status Code: {response.status_code}")
                print(f"DEBUG (VatComplyService): Resposta da API (texto): {response.text}")
            return None # Retorna None em caso de erro na requisição HTTP

    def get_rates_for_period(self, start_date, end_date):
        """
        Para obter cotações para um período específico, chamando get_daily_rates para cada dia.
        O salvamento no banco ocorre dentro de get_daily_rates.
        """
        all_rates = []
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() < 5: # Verifica se é dia útil (Seg-Sex)
                print(f"DEBUG (get_rates_for_period): Processando dia útil: {current_date}")
                daily_rates = self.get_daily_rates(current_date)
                if daily_rates:
                    all_rates.append(daily_rates)
                else:
                    print(f"DEBUG (get_rates_for_period): Nenhuma cotação válida retornada ou salva para {current_date}.")
            current_date += timedelta(days=1) # Avança para o próximo dia
        return all_rates