# Coleta de Dados de Preço Médios Mensais no site LME

Objetivo: Desenvolver um script em Python que acesse o site da LME (London Metal Exchange), navegue até a seção "monthly average" e compile os dados dos últimos 3 meses em um arquivo Excel.


## Funcionalidades
- Acessa a página da LME para extração de dados.
- Navega automaticamente entre diferentes produtos e coleta seus preços médios.
- Salva os dados coletados em um arquivo Excel.


## Requisitos
- Python 3.10 
- BotCity Web Automation
- Pandas & Openpyxl
- WebDriver Manager


## Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/MatheeusPinheiro/desafio01.git

2. Navegue até o diretório do projeto:
	```bash
   cd desafio01

3. Crie um ambiente virtual:
	```bash
   python -m venv venv

4. Ative o ambiente virtual no Windows:
	```bash
   .\venv\Scripts\activate

5. Instale as dependências:
	```bash
   pip install -r requirements.txt