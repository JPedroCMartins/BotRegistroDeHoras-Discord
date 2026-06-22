# Ponto Bot - Registro de Horas

Um sistema completo para registro de ponto e gerenciamento de horas focado em estabilidade e facilidade de uso. O projeto utiliza uma arquitetura modularizada, separando a interface do bot do Discord e o dashboard web Flask em aplicações e arquivos distintos.

## 🛠️ Tecnologias Utilizadas

* **Linguagem**: Python 3.12
* **Gerenciamento de Dependências**: `uv`
* **Interface**: Discord.py (Bot) e Flask (Web Dashboard)
* **Banco de Dados**: SQLAlchemy
* **Infraestrutura**: Docker e Docker Compose

## 📁 Estrutura do Projeto

A arquitetura do projeto foi desenhada para isolar responsabilidades, garantindo maior estabilidade:

* `bot/`: Contém a lógica principal do bot do Discord, configurações e comandos (`comandos.py`, `config.py`).
* `web/`: Aplicação do dashboard web em Flask, incluindo rotas, arquivos estáticos (CSS/JS) e templates HTML (`index.html`).
* `database/`: Modelos e configurações de conexão e persistência de dados via SQLAlchemy (`database.py`).
* `main.py`: Ponto de entrada unificado para orquestrar os serviços.
* `docker-compose.yml`: Orquestração de containers para deploy simplificado.

## 🚀 Como Executar

### 1. Configuração do Ambiente e Token do Discord
Para que o bot funcione corretamente, você **precisa obrigatoriamente de um Token de Bot do Discord**. 

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
2. Crie uma nova aplicação (New Application) ou selecione uma existente.
3. Vá até a seção **Bot** no menu lateral.
4. Clique em **Reset Token** (ou Copy se já tiver gerado) para obter o seu token privado.
5. Certifique-se de ativar as **Privileged Gateway Intents** necessárias (como *Presence Intent*, *Server Members Intent* e *Message Content Intent*) na mesma página do Bot.

Com o token em mãos, clone o repositório e configure o arquivo de variáveis de ambiente:

**Configuração do Ambiente**:
   Clone o repositório e crie o seu arquivo de variáveis de ambiente usando o exemplo fornecido:
   ```bash
   cp .env.example .env
   ```

### 2. **Execução via Docker (Recomendado)**:
   Certifique-se de ter o Docker instalado e execute:
   ```bash
   docker-compose up -d
   ```

### 3. **Execução Local**:
   Caso prefira rodar localmente sem Docker, instale as dependências com o `uv` a partir do `pyproject.toml` / `uv.lock`, e inicie a aplicação:
   ```bash
   uv sync
   python main.py
   ```