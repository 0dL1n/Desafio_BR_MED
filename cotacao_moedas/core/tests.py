from django.test import TestCase, Client
from datetime import date, timedelta
from unittest.mock import patch
from .services import VatComplyService # Importação correta
import requests
import json

# Testes para o serviço VatComplyService
class VatComplyServiceTestCase(TestCase):

    def setUp(self):
        self.service = VatComplyService()

    @patch('requests.get') # Correção do caminho do patch
    def test_get_daily_rates_success(self, mock_get):
        # simula a resposta da API
        mock_response = {
            "date": "2024-01-01",
            "base": "USD",
            "rates": { # As chaves devem estar no dicionário 'rates'
                "BRL": 5.25,
                "EUR": 0.85,
                "JPY": 110.0
            }
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        mock_get.return_value.raise_for_status.return_value = None

        target_date = date(2024, 1, 1) # Ajustado para corresponder à data mockada
        rates = self.service.get_daily_rates(target_date)

        self.assertIsNotNone(rates)
        self.assertEqual(rates['date'], '2024-01-01')
        self.assertEqual(rates['rates']['BRL'], 5.25) # AssertEqual para verificar valor
        self.assertEqual(rates['rates']['EUR'], 0.85) # AssertEqual para verificar valor
        self.assertEqual(rates['rates']['JPY'], 110.0) # AssertEqual para verificar valor

    @patch('requests.get') # Correção do caminho do patch
    def test_get_daily_rates_failure(self, mock_get):
        # simula erro na API
        # mock.get.return_value.status_code = 404 # Corrigido: 'mock_get', não 'mock'
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

        test_date = date(2024, 1, 1)
        rates = self.service.get_daily_rates(test_date)
        self.assertIsNone(rates)

    @patch('core.services.VatComplyService.get_daily_rates') # Correção do typo 'sevices'
    def test_get_rates_for_period(self, mock_get_daily_rates):
        # Simula a resposta da API para várias datas
        mock_get_daily_rates.side_effect = [
            {'date': '2024-01-01', 'rates': {'BRL': 5.25, 'EUR': 0.85, 'JPY': 110.0}},
            {'date': '2024-01-02', 'rates': {'BRL': 5.30, 'EUR': 0.86, 'JPY': 111.0}},
            {'date': '2024-01-03', 'rates': {'BRL': 5.35, 'EUR': 0.87, 'JPY': 112.0}},
            {'date': '2024-01-04', 'rates': {'BRL': 5.40, 'EUR': 0.88, 'JPY': 113.0}},
            {'date': '2024-01-05', 'rates': {'BRL': 5.45, 'EUR': 0.89, 'JPY': 114.0}},
        ]

        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 5)
        rates = self.service.get_rates_for_period(start_date, end_date)

        self.assertEqual(len(rates), 5)
        self.assertEqual(rates[0]['date'], '2024-01-01')
        self.assertEqual(rates[-1]['date'], '2024-01-05')

# Testes para as Views (endpoints Django)
class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @patch('core.views.VatComplyService.get_rates_for_period')
    def test_get_cotacoes_api_success(self, mock_get_rates_for_period):
        # simula resposta da API
        mock_get_rates_for_period.return_value = [
            {'date': '2024-01-01', 'rates': {'BRL': 5.25, 'EUR': 0.85, 'JPY': 110.0}},
            {'date': '2024-01-02', 'rates': {'BRL': 5.30, 'EUR': 0.86, 'JPY': 111.0}},
        ]
        response = self.client.get('/api/cotacoes/?start_date=2024-01-01&end_date=2024-01-02')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('dates', data) # Sintaxe corrigida
        self.assertEqual(len(data['dates']), 2)
        self.assertEqual(data['BRL'][0], 5.25)

    def test_get_cotacoes_api_missing_params(self):
        response = self.client.get('/api/cotacoes/')
        self.assertEqual(response.status_code, 400)
        # Verifique a mensagem exata no seu views.py
        self.assertIn('Datas de início e fim são obrigatórias.', response.json()['error'])

    def test_get_cotacoes_api_invalid_date_format(self):
        response = self.client.get('/api/cotacoes/?start_date=2024-01-01&end_date=invalid-date')
        self.assertEqual(response.status_code, 400)
        # Verifique a mensagem exata no seu views.py
        self.assertIn('Formato de data inválido. Use YYYY-MM-DD.', response.json()['error'])

    def test_get_cotacoes_api_period_too_long(self):
        start_date = (date.today() - timedelta(days=8)).strftime('%Y-%m-%d')
        end_date = date.today().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/cotacoes/?start_date={start_date}&end_date={end_date}')
        self.assertEqual(response.status_code, 400)
        # Verifique a mensagem exata no seu views.py
        self.assertIn('O período máximo permitido é de 5 dias úteis (máximo 7 dias corridos).', response.json()['error'])

    @patch('core.views.VatComplyService.get_rates_for_period', return_value=[])
    def test_get_cotacoes_api_no_data_found(self, mock_get_rates_for_period):
        response = self.client.get('/api/cotacoes/?start_date=2024-01-01&end_date=2024-01-02')
        self.assertEqual(response.status_code, 200) # O status code é 200 se não houver erro, apenas sem dados.
        # Verifique a mensagem exata no seu views.py
        self.assertIn('Nenhum dado de cotação encontrado para o período.', response.json()['message'])