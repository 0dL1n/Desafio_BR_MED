# cotacao_moedas/core/views.py
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .services import VatComplyService
from .models import Cotacao 

def index(request):
    """
    renderiza pagina inicial com os graficos de cotacao
    """
    return render(request, 'index.html')

def get_cotacoes_api(request):
    """
    Endpoint para obter as cotações de moedas da API externa.
    Essas cotações também serão persistidas no banco de dados.
    """
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        return JsonResponse({'error': 'Datas de início e fim são obrigatórios.'}, status=400)

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Formato de data inválido. Use %Y-%m-%d.'}, status=400)

    if (end_date - start_date).days < 0:
        return JsonResponse({'error': 'A data de início deve ser anterior à data de fim.'}, status=400)

    if (end_date - start_date).days > 6: # Limite de 7 dias corridos para 5 dias úteis
        return JsonResponse({'error': 'O período máximo permitido é de 5 dias úteis (máximo 7 dias corridos).'}, status=400)

    service = VatComplyService()
    cotacoes = service.get_rates_for_period(start_date, end_date) # Isso vai buscar da API externa E salvar no DB

    if not cotacoes:
        return JsonResponse({'message': 'Nenhum dado de cotação encontrado da API externa para o período.'}, status=200)

    formatted_data = {
        'dates': [c['date'] for c in cotacoes],
        'BRL': [c['rates'].get('BRL', None) for c in cotacoes],
        'EUR': [c['rates'].get('EUR', None) for c in cotacoes],
        'JPY': [c['rates'].get('JPY', None) for c in cotacoes],
    }

    return JsonResponse(formatted_data, status=200)


def get_cotacoes_db_api(request):
    """
    NOVA API: Endpoint para obter as cotações de moedas diretamente do banco de dados.
    Permite filtrar por data de início e fim.
    """
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    query_params_present = bool(start_date_str and end_date_str)

    if query_params_present:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Formato de data inválido. Use %Y-%m-%d.'}, status=400)

        if (end_date - start_date).days < 0:
            return JsonResponse({'error': 'A data de início deve ser anterior à data de fim.'}, status=400)

        # Para dados do banco, não aplicamos o limite de 5 dias úteis,
        # pois são dados históricos que já foram coletados.
        cotacoes_db = Cotacao.objects.filter(data__range=(start_date, end_date)).order_by('data')
    else:
        # Se não houver datas no parâmetro, retorna as últimas 30 cotações do banco, por exemplo.
        print("DEBUG: Nenhuma data especificada, retornando as 30 últimas cotações do banco.")
        cotacoes_db = Cotacao.objects.all().order_by('-data')[:30] # Ordena decrescente e pega as 30 últimas

    if not cotacoes_db.exists():
        return JsonResponse({'message': 'Nenhum dado de cotação encontrado no banco de dados para o período especificado.'}, status=200)

    # Formata os dados do QuerySet para o formato JSON esperado pelo frontend
    formatted_data = {
        'dates': [],
        'BRL': [],
        'EUR': [],
        'JPY': [],
    }

    for cotacao in cotacoes_db:
        formatted_data['dates'].append(cotacao.data.strftime('%Y-%m-%d'))
        # Converte Decimal para float antes de adicionar ao JSON
        formatted_data['BRL'].append(float(cotacao.valor_brl) if cotacao.valor_brl is not None else None)
        formatted_data['EUR'].append(float(cotacao.valor_eur) if cotacao.valor_eur is not None else None)
        formatted_data['JPY'].append(float(cotacao.valor_jpy) if cotacao.valor_jpy is not None else None)

    return JsonResponse(formatted_data, status=200)