from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .services import VatComplyService


def index(request):
    """
    renderiza pagina inicial com os graficos de cotacao
    """
    return render(request, 'index.html')

def get_cotacoes_api(request):
    """
    Endpoint para obter as cotações de moedas
    """
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        return JsonResponse({'error': 'Datas de início e fim são obrigatórios.'}, status=400)
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Formato de data inválido. Use YYYY-MM-DD.'}, status=400)

    if(end_date - start_date).days < 0:
        return JsonResponse({'error': 'A data de início deve ser anterior à data de fim.'}, status=400)
    if (end_date - start_date).days > 6:
        return JsonResponse({'error': 'O período máximo permitido é de 5 dias uteis(maximo 7 dias corrido).'}, status=400)

    service = VatComplyService()
    cotacoes = service.get_rates_for_period(start_date, end_date)
    

    if not cotacoes:
        return JsonResponse({'error': 'Nenhuma cotação encontrada para o período especificado.'}, status=200)
    
    formatted_data = {
        'dates': [cotacao['date'] for cotacao in cotacoes],
        'BRL': [cotacao['rates'].get('BRL', None) for cotacao in cotacoes],
        'EUR': [cotacao['rates'].get('EUR', None) for cotacao in cotacoes],
        'JPY': [cotacao['rates'].get('JPY', None) for cotacao in cotacoes],
    }

    return JsonResponse(formatted_data, status=200)