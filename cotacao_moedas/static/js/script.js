// static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    // --- Lógica de Dark Mode ---
    const darkModeToggle = document.getElementById('darkModeToggle');
    console.log('DEBUG: Elemento darkModeToggle encontrado:', darkModeToggle); // Confirma se o elemento é encontrado
    const body = document.body;

    // Função para aplicar o tema (claro ou escuro)
    function applyTheme(isDarkMode) {
        if (isDarkMode) {
            body.classList.add('dark-mode');
            console.log('DEBUG: Aplicando tema escuro (dark-mode adicionado ao body)');
        } else {
            body.classList.remove('dark-mode');
            console.log('DEBUG: Aplicando tema claro (dark-mode removido do body)');
        }
        // Salva a preferência do usuário no localStorage para persistência
        localStorage.setItem('darkMode', isDarkMode);

        // Atualiza o tema do Highcharts também, para que o gráfico reflita o modo
        updateHighchartsTheme(isDarkMode);
    }

    // Verifica a preferência do usuário ao carregar a página
    // e aplica o tema salvo (ou o padrão claro se não houver preferência)
    const savedDarkMode = localStorage.getItem('darkMode');
    if (darkModeToggle) { // CORREÇÃO: Garante que o elemento existe antes de tentar manipulá-lo
        if (savedDarkMode === 'true') {
            darkModeToggle.checked = true; // Marca o checkbox se o modo escuro estava salvo
            applyTheme(true);
        } else {
            darkModeToggle.checked = false; // Desmarca o checkbox
            applyTheme(false); // Garante que o modo claro é aplicado se não houver preferência ou for 'false'
        }

        // Adiciona um 'listener' para detectar quando o checkbox de dark mode é alterado
        darkModeToggle.addEventListener('change', () => {
            applyTheme(darkModeToggle.checked); // Chama applyTheme com base no estado atual do checkbox
            console.log('DEBUG: Toggle clicado, checked:', darkModeToggle.checked); // DEBUG DE CLIQUE
        });
    } else {
        console.warn('DEBUG: darkModeToggle não foi encontrado. Dark Mode desativado.'); // ALERTA SE O ELEMENTO NÃO EXISTE
    }


    // --- Lógica de Cotação (cálculo de datas iniciais e chamada da API) ---

    // Define as datas padrão para os campos de entrada
    const today = new Date();
    let startDate = new Date(today);
    let endDate = new Date(today);

    // Lógica revisada para encontrar os últimos 5 dias úteis,
    // garantindo que o período inicial respeite a validação do backend (max 7 dias corridos)
    const maxDaysToLookBack = 10; // Limite para evitar loops infinitos em busca de dias úteis
    let currentCheckDate = new Date(today);
    let validDates = []; // Array para armazenar as datas úteis encontradas

    // CORREÇÃO: daysOffset deve ser inicializado UMA VEZ neste escopo.
    // Remover qualquer outra declaração 'let daysOffset = 0;' dentro do loop 'while'.
    let daysOffset = 0; // Esta é a declaração correta para o loop abaixo.

    // Loop para encontrar os 5 últimos dias úteis (para o período padrão)
    while (validDates.length < 5 && daysOffset < maxDaysToLookBack) {
        // Verifica se o dia atual da iteração não é domingo (0) nem sábado (6)
        if (currentCheckDate.getDay() !== 0 && currentCheckDate.getDay() !== 6) {
            // Adiciona a data no início do array para mantê-lo em ordem crescente
            validDates.unshift(new Date(currentCheckDate));
        }
        // Decrementa a data para verificar o dia anterior
        currentCheckDate.setDate(currentCheckDate.getDate() - 1);
        daysOffset++;
    }

    // Define as datas de início e fim com base nos dias úteis encontrados
    if (validDates.length > 0) {
        startDate = validDates[0]; // Primeira data útil encontrada (mais antiga)
        endDate = validDates[validDates.length - 1]; // Última data útil encontrada (mais recente)
        console.log(`DEBUG: Datas iniciais calculadas: ${formatDate(startDate)} a ${formatDate(endDate)}`);
    } else {
        // Fallback: Se não conseguir encontrar 5 dias úteis (muito improvável), usa um período fixo pequeno
        console.warn("DEBUG: Não foi possível calcular 5 dias úteis. Usando período padrão de 5 dias corridos.");
        startDate = new Date(today);
        startDate.setDate(today.getDate() - 4); // 5 dias atrás
        endDate = new Date(today);
    }

    // Formata as datas para o padrão %Y-%m-%d para preencher os campos de input
    // NOTE: Esta função foi declarada DENTRO do DOMContentLoaded,
    // o que é ok, mas se fosse usada fora, precisaria ser global.
    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Mês é base 0
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    // Preenche os campos de input de data no HTML
    document.getElementById('startDate').value = formatDate(startDate);
    document.getElementById('endDate').value = formatDate(endDate);

    // Carrega o gráfico com os dados iniciais assim que a página é carregada
    fetchDataAndRenderChart();
});


// --- Funções Auxiliares para o Dark Mode do Highcharts ---

// Esta função atualiza o tema visual do Highcharts com base no modo (claro/escuro)
function updateHighchartsTheme(isDarkMode) {
    // Define as cores a serem usadas no Highcharts com base no modo atual
    const textColor = isDarkMode ? '#f4f4f4' : '#333'; // Cor do texto
    const gridLineColor = isDarkMode ? '#555' : '#e6e6e6'; // Cor das linhas da grade
    const backgroundColor = isDarkMode ? '#3a3f4a' : '#fff'; // Cor de fundo do chart

    // Aplica as opções de tema globalmente para Highcharts
    Highcharts.setOptions({
        chart: {
            backgroundColor: backgroundColor, // Fundo do gráfico
            style: {
                color: textColor // Cor do texto geral do gráfico
            }
        },
        title: {
            style: {
                color: textColor // Cor do título do gráfico
            }
        },
        subtitle: {
            style: {
                color: textColor // Cor do subtítulo do gráfico
            }
        },
        xAxis: {
            labels: {
                style: {
                    color: textColor // Cor dos rótulos do eixo X
                }
            },
            lineColor: gridLineColor, // Cor da linha do eixo X
            tickColor: gridLineColor, // Cor dos ticks do eixo X
            title: {
                style: {
                    color: textColor // Cor do título do eixo X
                }
            },
            gridLineColor: gridLineColor // Cor das linhas de grade verticais
        },
        yAxis: {
            labels: {
                style: {
                    color: textColor // Cor dos rótulos do eixo Y
                }
            },
            lineColor: gridLineColor, // Cor da linha do eixo Y
            tickColor: gridLineColor, // Cor dos ticks do eixo Y
            title: {
                style: {
                    color: textColor // Cor do título do eixo Y
                }
            },
            gridLineColor: gridLineColor // Cor das linhas de grade horizontais
        },
        legend: {
            itemStyle: {
                color: textColor // Cor do texto da legenda
            },
            itemHoverStyle: {
                color: '#ADD8E6' // Cor do texto da legenda ao passar o mouse (um azul claro)
            }
        },
        tooltip: {
            style: {
                color: textColor // Cor do texto dentro do tooltip
            },
            backgroundColor: isDarkMode ? 'rgba(40, 44, 54, 0.85)' : 'rgba(255, 255, 255, 0.85)', // Fundo do tooltip
            borderColor: isDarkMode ? '#555' : '#ddd' // Borda do tooltip
        },
        // Adicione outras configurações de tema conforme necessário para outros elementos do gráfico
    });

    // Se o gráfico já estiver renderizado, força uma nova renderização para aplicar o tema
    // Highcharts.charts[0] refere-se ao primeiro gráfico na página
    if (Highcharts.charts[0]) {
        Highcharts.charts[0].update({}); // Atualiza o gráfico sem mudar os dados, apenas o tema
    }
}


// --- Funções para Fetch de Dados e Renderização do Gráfico ---

// Função principal para buscar dados da API do Django e renderizar o gráfico
function fetchDataAndRenderChart() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const messageElement = document.getElementById('message');
    messageElement.textContent = ''; // Limpa mensagens anteriores na tela

    // Validação básica se as datas foram selecionadas
    if (!startDate || !endDate) {
        messageElement.textContent = 'Por favor, selecione as datas de início e fim.';
        return;
    }

    // Faz a requisição assíncrona (AJAX) para o endpoint da API do Django
    fetch(`/api/cotacoes/?start_date=${startDate}&end_date=${endDate}`)
        .then(response => {
            // Se a resposta HTTP não for bem-sucedida (ex: 400 Bad Request, 500 Internal Server Error)
            if (!response.ok) {
                // Tenta ler o JSON de erro do backend e lança um erro JavaScript
                return response.json().then(errorData => {
                    throw new Error(errorData.error || 'Erro desconhecido na API.');
                });
            }
            // Se a resposta for OK, converte-a para JSON
            return response.json();
        })
        .then(data => {
            // Se o backend enviar uma mensagem (ex: "Nenhum dado encontrado")
            if (data.message) {
                messageElement.textContent = data.message;
                renderEmptyChart(); // Renderiza um gráfico vazio ou com a mensagem
                return;
            }

            // Se não houver datas nos dados retornados, também exibe mensagem de ausência de dados
            if (!data.dates || data.dates.length === 0) {
                messageElement.textContent = 'Nenhum dado de cotação disponível para o período selecionado.';
                renderEmptyChart();
                return;
            }

            // Mapeia os dados recebidos para o formato que o Highcharts espera (arrays de séries)
            const seriesData = [
                {
                    name: 'BRL',
                    data: data.BRL.map(val => val !== null ? val : null) // Mapeia para null se o valor for nulo
                },
                {
                    name: 'EUR',
                    data: data.EUR.map(val => val !== null ? val : null)
                },
                {
                    name: 'JPY',
                    data: data.JPY.map(val => val !== null ? val : null)
                }
            ];

            // Chama a função para renderizar o gráfico com os dados obtidos
            renderChart(data.dates, seriesData);
        })
        .catch(error => {
            // Captura e exibe qualquer erro que ocorra durante o fetch ou processamento
            console.error('Erro ao buscar dados:', error);
            messageElement.textContent = `Erro ao carregar cotações: ${error.message}`;
            renderEmptyChart();
        });
} 

// Função para renderizar o gráfico Highcharts com os dados fornecidos
function renderChart(dates, seriesData) {
    Highcharts.chart('chart-container', {
        chart: {
            type: 'line'
            // As configurações de background/estilo são aplicadas via updateHighchartsTheme
        },
        title: {
            text: 'Cotação Dólar (USD) vs. BRL, EUR, JPY'
        },
        subtitle: {
            text: 'Fonte: Vatcomply.com'
        },
        xAxis: {
            categories: dates, // Datas no eixo X
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
            valueDecimals: 4, // Formata os valores no tooltip para 4 casas decimais
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y:.4f}</b><br/>'
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: false
                },
                enableMouseTracking: true
            }
        },
        series: seriesData, // Os dados das séries (BRL, EUR, JPY)
        credits: {
            enabled: false
        }
    });

    // Aplica o tema Highcharts (claro/escuro) após a renderização inicial do gráfico
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) { // Verifica se o toggle existe (boa prática)
        updateHighchartsTheme(darkModeToggle.checked);
    }
}

// Função para renderizar um gráfico vazio, usado quando não há dados
function renderEmptyChart() {
    Highcharts.chart('chart-container', {
        title: {
            text: 'Nenhum dado para exibir' // Título para quando não há dados
        },
        series: [], // Nenhuma série de dados
        xAxis: {
            categories: [] // Nenhum categoria no eixo X
        },
        yAxis: {
            title: {
                text: '' // Nenhum título no eixo Y
            }
        },
        credits: {
            enabled: false
        }
    });
    // Aplica o tema também ao gráfico vazio
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) { // Verifica se o toggle existe
        updateHighchartsTheme(darkModeToggle.checked);
    }
}