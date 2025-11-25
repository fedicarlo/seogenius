# SEOgenius v0.1

Motor inicial do SEOgenius — um sistema em Python para análise de palavras-chave, coleta de dados externos e geração de insights de SEO voltados para suplementos, nutricosméticos e produtos de alto tráfego.

Esta versão (v0.1) contém:
- Cliente Ubersuggest funcional
- Pipeline básico de execução (run.py)
- Estrutura inicial de modularização
- Suporte a variáveis de ambiente via .env
- Requisitos mínimos em requirements.txt

====================================
Objetivo do Projeto
====================================

Criar uma ferramenta autônoma de SEO capaz de:

1. Receber um termo ou produto
2. Extrair sugestões de busca (Ubersuggest e outras fontes futuras)
3. Organizar clusters semânticos
4. Processar relevância e intenção de busca
5. Gerar campos de SEO otimizados, títulos e descrições
6. Futuramente realizar scraping, agrupamentos, scoring e IA interpretativa

Este repositório inicia a arquitetura do motor.

====================================
Estrutura do Projeto
====================================

seogenius/
- run.py
- ubersuggest_client.py
- requirements.txt
- .gitignore

====================================
Instalação
====================================

1) Clonar o repositório:

    git clone https://github.com/fedicarlo/seogenius.git
    cd seogenius

2) Criar ambiente virtual (opcional):

    python3 -m venv .venv
    source .venv/bin/activate

3) Instalar dependências:

    pip install -r requirements.txt

====================================
Configuração do .env
====================================

Crie um arquivo .env na raiz do projeto com:

    UBERSUGGEST_API_KEY=coloque_sua_chave_aqui

O arquivo .env não é versionado (está no .gitignore).

====================================
Execução
====================================

Para rodar o motor atual:

    python run.py

O script executa o cliente Ubersuggest e imprime os resultados processados no terminal.

====================================
Próximos Passos (v0.2)
====================================

- Adicionar motor de clusterização automática
- Criar interpretador de IA para combinar tráfego + semântica
- Implementar módulo de scraping
- Implementar cache local e banco SQLite
- Criar presets por categoria (suplementos, vitaminas, nutricosméticos)
- Integrar com Google Trends
- Adicionar testes unitários
- Criar interface de linha de comando (CLI) mais completa

====================================
Notas
====================================

- Projeto em desenvolvimento ativo.
- Cada evolução será versionada com commits claros.
- Objetivo final: fluxo autônomo de busca -> cluster -> análise -> output final.
