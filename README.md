# Análise Financeira Diária Automatizada - Inteligência de Mercado

Sistema de automação diária para geração de relatórios de inteligência do mercado financeiro, análise de tendências, mitigação de riscos, rastreamento de oportunidades e envio para múltiplos canais corporativos.

---

## 📌 Funcionalidades

- **Coleta e Consolidação Multiafonte**: Consulta de notícias, indicadores e movimentações das últimas 24h, 7 dias e 30 dias de fontes confiáveis (Bloomberg, Reuters, Valor Econômico, InfoMoney, Fed, B3, etc.).
- **Dashboard Executivo**: Resumo consolidado com Tendência Geral (⬆️ ⬇️ ➡️), Sentimento do Mercado, Nível de Risco, Quantidade de Oportunidades Mapeadas, Eventos Críticos e Nível de Confiança (%).
- **Relatório Completo em Markdown**: Estrutura em 10 seções estratégicas incluindo Destaques, Tendências, Indicadores Econômicos, Movimentação de Ativos, Riscos, Oportunidades, Radar de Eventos e Conclusão Estratégica.
- **Resumo Executivo em PDF**: PDF de 1 página limpo, profissional e pronto para leitura rápida pela diretoria.
- **Histórico e Comparativo Diário (Day-over-Day)**: Rastreia mudanças de sentimento, novos riscos identificados e novas oportunidades surgidas comparadas com os relatórios dos dias anteriores.
- **Integração Multi-Canal**: Suporte para distribuição automática via **E-mail**, **Microsoft Teams**, **Slack**, **Notion** e **SharePoint**.
- **Agendamento Automático**: Modo servidor para execução automática diária às 07:00.

---

## 🚀 Como Usar

### 1. Instalação de Dependências

```bash
pip install fpdf2 reportlab pydantic requests pytest
```

### 2. Execução Sob Demanda (CLI)

Gere relatórios imediatamente para tópicos específicos:

```bash
# Executar para um tema específico
python main.py --topic "Bolsa Brasileira"

# Executar para múltiplos temas e enviar para e-mail
python main.py --topic "Bolsa Brasileira" --topic "Criptomoedas" --email "diretoria@empresa.com"
```

### 3. Agendamento Automático Diário às 07:00

Deixe o processo rodando em segundo plano:

```bash
python main.py --schedule --time "07:00" --email "equipe@empresa.com"
```

---

## ⚙️ Configuração de Variáveis de Ambiente

As integrações podem ser configuradas via variáveis de ambiente no arquivo `.env` ou no sistema:

```bash
# E-mail (SMTP)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="seu-email@empresa.com"
export SMTP_PASS="sua-senha-de-app"

# Webhooks Corporativos
export TEAMS_WEBHOOK_URL="https://outlook.office.com/webhook/..."
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Notion & SharePoint
export NOTION_API_TOKEN="secret_notion_token"
export NOTION_DATABASE_ID="notion_db_id"
export SHAREPOINT_SITE_URL="https://empresa.sharepoint.com/sites/Mercado"
```

---

## 🧪 Suíte de Testes Automatizados

Para rodar os testes unitários da aplicação:

```bash
python3 -m pytest
```

---

## 📁 Estrutura do Projeto

```
.
├── main.py                          # CLI e Agendador Diário às 07:00
├── market_intelligence/             # Módulo principal
│   ├── models.py                    # Modelos de dados e Schemas (Pydantic)
│   ├── fetcher.py                   # Coletor e Sintetizador de Dados
│   ├── analyzer.py                  # Consolidador e Calculador de Confiança
│   ├── markdown_generator.py        # Gerador do Relatório em Markdown
│   ├── pdf_generator.py             # Gerador do PDF Resumo Executivo
│   ├── history.py                   # Motor de Histórico e Comparativo Diário
│   └── notifications.py             # Despachante Multi-Canal (Email/Teams/Slack/Notion)
├── output/                          # Relatórios em Markdown, PDFs e Histórico
└── tests/                           # Suíte de Testes Automatizados (pytest)
```
