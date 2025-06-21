# 📈 Projeto de Cotação de Moedas

## Visão Geral

Este é um projeto web Full-Stack desenvolvido para exibir cotações históricas de moedas. O objetivo é demonstrar a integração entre um frontend dinâmico e um backend robusto, consumindo dados de uma API externa.

## 🚀 Funcionalidades

* **Consulta por Período:** Permite que o usuário selecione um intervalo de datas (data de início e fim) para visualizar as cotações de moedas.
* **Moedas Monitoradas:** Exibe as cotações de Real Brasileiro (BRL), Euro (EUR) e Iene Japonês (JPY) em relação ao Dólar Americano (USD).
* **Visualização Gráfica:** Os dados das cotações são apresentados de forma clara e interativa em gráficos.
* **Validação de Período:** O sistema valida o período de consulta, impedindo requisições para intervalos inválidos ou que excedam um máximo (ex: 7 dias corridos ou 5 dias úteis, conforme a lógica implementada).

## 🛠️ Tecnologias Utilizadas

### Backend
* **Python:** Linguagem de programação principal do backend.
* **Django:** Framework web de alto nível para o desenvolvimento rápido e seguro do backend.
* **Django REST Framework (DRF):** Extensão do Django utilizada para construir a API RESTful que expõe os dados das cotações.
* **`requests`:** Biblioteca Python para realizar requisições HTTP e consumir dados da API externa (VatComply API).
* **`sqlite3`:** Banco de dados padrão utilizado para desenvolvimento e armazenamento dos modelos de dados do Django.

### Frontend
* **HTML, CSS, JavaScript:** Tecnologias fundamentais para a estruturação, estilização e interatividade da interface do usuário no navegador.
* **Vue.js:** Framework JavaScript progressivo para a construção da interface do usuário (UI), focado na reatividade e na construção de componentes.
* **Axios:** Cliente HTTP baseado em Promessas, utilizado no frontend Vue.js para fazer requisições assíncronas à API Django.
* **Highcharts:** Biblioteca JavaScript para a criação de gráficos interativos e visualização dos dados das cotações.

## 📧 Contato

* **Ivanildo Adelino da Silva Junior**
* **Email:** ivanildoodlinavi65@gmail.com
* **LinkedIn:** https://www.linkedin.com/in/0dl1n/
* **GitHub:** https://github.com/0dl1n

---

