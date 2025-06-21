document.addEventListener('DOMContentLoaded', () => {
    // Define as datas padrão (hoje e 4 dias úteis antes)
    const today = new Date();
    let startDate = new Date(today);
    let endDate = new Date(today);

    let daysOffset = 0;
    let weekdaysCount = 0;

    // Garante que o período seja de 5 dias úteis (contando regressivamente a partir de hoje)
    while (weekdaysCount < 4) { // Precisa de 4 dias úteis antes de hoje para totalizar 5 (incluindo hoje)
        startDate.setDate(today.getDate() - daysOffset);
        if (startDate.getDay() !== 0 && startDate.getDay() !== 6) { // Não é domingo (0) nem sábado (6)
            weekdaysCount++;
        }
        daysOffset++;
    }

    // Formata as datas para YYYY-MM-DD
    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    document.getElementById('startDate').value = formatDate(startDate);
    document.getElementById('endDate').value = formatDate(endDate);

    // Carrega o gráfico com os dados iniciais
    fetchDataAndRenderChart();
});


function fetchDataAndRenderChart() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const messageElement = document.getElementById('message');
    messageElement.textContent = ''; // Limpa mensagens anteriores

    if (!startDate || !endDate) {
        messageElement.textContent = 'Por favor, selecione as datas de início e fim.';
        return;
    }

    // Requisição AJAX para o endpoint Django
    fetch(`/api/cotacoes/?start_date=${startDate}&end_date=${endDate}`)
        .then(response => {
            if (!response.ok) {
                // Se a resposta não for 2xx, tenta ler a mensagem de erro do backend
                return response.json().then(errorData => {
                    throw new Error(errorData.error || 'Erro desconhecido na API.');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.message) { // Se houver uma mensagem do backend (ex: nenhum dado encontrado)
                messageElement.textContent = data.message;
                renderEmptyChart(); // Renderiza um gráfico vazio ou com mensagem
                return;
            }

            if (!data.dates || data.dates.length === 0) {
                messageElement.textContent = 'Nenhum dado de cotação disponível para o período selecionado.';
                renderEmptyChart();
                return;
            }

            // Mapeia os dados para o formato que o Highcharts espera
            const seriesData = [
                {
                    name: 'BRL',
                    data: data.BRL
                },
                {
                    name: 'EUR',
                    data: data.EUR
                },
                {
                    name: 'JPY',
                    data: data.JPY
                }
            ];

            renderChart(data.dates, seriesData);
        })
        .catch(error => {
            console.error('Erro ao buscar dados:', error);
            messageElement.textContent = `Erro ao carregar cotações: ${error.message}`;
            renderEmptyChart();
        });
}

function renderChart(dates, seriesData) {
    Highcharts.chart('chart-container', {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Cotação Dólar (USD) vs. BRL, EUR, JPY'
        },
        subtitle: {
            text: 'Fonte: Vatcomply.com'
        },
        xAxis: {
            categories: dates,
            title: {
                text: 'Data'
            }
        },
        yAxis: {
            title: {
                text: 'Valor da Cotação (USD como base)'
            }
        },
        tooltip: {
            valueDecimals: 4, // Formata para 4 casas decimais
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y:.4f}</b><br/>'
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: false // Desabilita rótulos nos pontos
                },
                enableMouseTracking: true
            }
        },
        series: seriesData,
        credits: {
            enabled: false // Opcional: remove o link do Highcharts
        }
    });
}

function renderEmptyChart() {
    Highcharts.chart('chart-container', {
        title: {
            text: 'Nenhum dado para exibir'
        },
        series: [],
        xAxis: {
            categories: []
        },
        yAxis: {
            title: {
                text: ''
            }
        },
        credits: {
            enabled: false
        }
    });
}