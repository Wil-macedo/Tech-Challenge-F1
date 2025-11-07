# 🍷 Tech Challenge - API de Dados Vitivinícolas

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-green?style=for-the-badge&logo=flask&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-red?style=for-the-badge&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

<div align="center">
  <h3>🔐 Autenticação JWT | 🌐 Web Scraping | 📊 Dados Públicos Embrapa</h3>
</div>

---

API REST para consulta de dados da indústria vitivinícola brasileira, fornecendo informações sobre produção, processamento, comercialização, importação e exportação de vinhos, uvas e derivados.

## 📑 Índice

- [Descrição do Projeto](#descrição-do-projeto)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
  - [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
  - [Diagrama de Comunicação Cliente-Servidor](#diagrama-de-comunicação-cliente-servidor)
  - [Fluxo Completo de Processamento](#fluxo-completo-de-processamento-de-requisição)
- [Como Funciona a Autenticação](#como-funciona-a-autenticação)
  - [Fluxograma de Autenticação](#fluxograma-de-autenticação)
  - [Estrutura do JWT Token](#2-estrutura-do-jwt-token)
  - [Ciclo de Vida do Token](#3-ciclo-de-vida-do-token)
- [Origem e Processamento dos Dados](#origem-e-processamento-dos-dados)
  - [Mapa de Endpoints](#mapa-de-endpoints-e-fontes-de-dados)
  - [Pipeline de Web Scraping](#diagrama-do-pipeline-de-dados)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Utilização da API](#utilização-da-api)
- [Endpoints Disponíveis](#endpoints-disponíveis)
- [Documentação Swagger](#documentação-swagger)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tratamento de Erros](#tratamento-de-erros)
- [Segurança](#segurança)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato e Suporte](#contato-e-suporte)

---

## 📖 Descrição do Projeto

Esta API consome dados públicos da Embrapa (Empresa Brasileira de Pesquisa Agropecuária) sobre a vitivinicultura brasileira e disponibiliza através de endpoints RESTful com autenticação JWT.

## 🏗️ Arquitetura do Sistema

### Visão Geral da Arquitetura

```
                         ╔═══════════════════════════════════════╗
                         ║      TECH CHALLENGE API - FLASK       ║
                         ╚═══════════════════════════════════════╝
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
    ┌─────────────────┐      ┌─────────────────┐       ┌─────────────────┐
    │   CAMADA DE     │      │   CAMADA DE     │       │   CAMADA DE     │
    │  APRESENTAÇÃO   │      │  AUTENTICAÇÃO   │       │    NEGÓCIO      │
    │                 │      │                 │       │                 │
    │  • Endpoints    │      │  • JWT Tokens   │       │  • Validações   │
    │  • Rotas Flask  │      │  • Basic Auth   │       │  • Regras       │
    │  • JSON Response│      │  • Bearer Token │       │  • Exceções     │
    └─────────────────┘      └─────────────────┘       └─────────────────┘
              │                          │                          │
              └──────────────────────────┼──────────────────────────┘
                                         │
                                         ▼
                              ┌─────────────────┐
                              │   CAMADA DE     │
                              │   INTEGRAÇÃO    │
                              │                 │
                              │  • Web Scraping │
                              │  • BeautifulSoup│
                              │  • Pandas       │
                              └─────────────────┘
                                         │
                                         ▼
                              ┌─────────────────┐
                              │     EMBRAPA     │
                              │   VITIBRASIL    │
                              │  (Dados Públicos)│
                              └─────────────────┘
```

### Diagrama de Comunicação Cliente-Servidor

```
┏━━━━━━━━━━━━┓                      ┏━━━━━━━━━━━━━━━━┓                    ┏━━━━━━━━━━━━┓
┃  Cliente   ┃                      ┃   API Flask    ┃                    ┃  Embrapa   ┃
┃  (Postman, ┃                      ┃ Tech Challenge ┃                    ┃ Vitibrasil ┃
┃   cURL)    ┃                      ┃                ┃                    ┃            ┃
┗━━━━━━━━━━━━┛                      ┗━━━━━━━━━━━━━━━━┛                    ┗━━━━━━━━━━━━┛
      │                                      │                                   │
      │  1. POST /login                     │                                   │
      │  (Basic Auth)                       │                                   │
      ├────────────────────────────────────>│                                   │
      │                                      │                                   │
      │  2. JWT Token                       │                                   │
      │<────────────────────────────────────┤                                   │
      │                                      │                                   │
      │  3. GET /producao?ano=2021          │                                   │
      │  (Bearer Token)                     │                                   │
      ├────────────────────────────────────>│                                   │
      │                                      │  4. HTTP GET Request              │
      │                                      │  (Web Scraping)                   │
      │                                      ├──────────────────────────────────>│
      │                                      │                                   │
      │                                      │  5. HTML Tables                   │
      │                                      │<──────────────────────────────────┤
      │                                      │                                   │
      │                                      │  6. Parse & Process               │
      │                                      │  (BeautifulSoup + Pandas)         │
      │                                      │                                   │
      │  7. JSON Response                   │                                   │
      │<────────────────────────────────────┤                                   │
      │                                      │                                   │
```

### Camadas da Aplicação

1. **Camada de Apresentação (API Endpoints)**
   - Recebe requisições HTTP
   - Valida autenticação JWT
   - Retorna dados em formato JSON

2. **Camada de Autenticação**
   - Implementada com Flask-JWT-Extended
   - Gerencia tokens de acesso
   - Protege endpoints sensíveis

3. **Camada de Negócio**
   - Validação de parâmetros (anos, intervalos)
   - Processamento de dados
   - Tratamento de exceções customizadas

4. **Camada de Integração**
   - Web scraping com BeautifulSoup4
   - Requisições HTTP para Embrapa
   - Parsing de tabelas HTML com Pandas

### Fluxo Completo de Processamento de Requisição

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        FLUXO DE REQUISIÇÃO                              │
└─────────────────────────────────────────────────────────────────────────┘

    ╔════════════╗
    ║  CLIENTE   ║
    ╚════════════╝
         │
         │ GET /producao?ano=2021
         │ Authorization: Bearer {token}
         ▼
    ┌─────────────────────┐
    │  1. RECEBE REQUEST  │────────┐
    │     (app.py)        │        │ Valida JWT Token
    └─────────────────────┘        │ ✓ Token válido?
         │                         │ ✗ Retorna 401
         │ ✓ Token válido          │
         ▼                         │
    ┌─────────────────────┐        │
    │  2. VALIDA PARAMS   │────────┤
    │  (validations.py)   │        │ Valida ano (1970-2023)
    └─────────────────────┘        │ ✓ Parâmetro válido?
         │                         │ ✗ Retorna 400
         │ ✓ Ano válido            │
         ▼                         │
    ┌─────────────────────┐        │
    │  3. MONTA URL       │        │
    │ (request_function)  │        │ Adiciona ano à query string
    └─────────────────────┘        │ http://embrapa.br?ano=2021
         │                         │
         ▼                         │
    ┌─────────────────────┐        │
    │  4. FAZ REQUEST     │────────┤
    │  requests.get()     │        │ Timeout: 30s
    └─────────────────────┘        │ ✓ Sucesso?
         │                         │ ✗ Retorna 500
         │ ✓ HTML recebido         │
         ▼                         │
    ┌─────────────────────┐        │
    │  5. PARSE HTML      │        │
    │  (BeautifulSoup)    │        │ Extrai tabela[4]
    └─────────────────────┘        │
         │                         │
         ▼                         │
    ┌─────────────────────┐        │
    │  6. CONVERTE DF     │        │
    │     (Pandas)        │        │ HTML → DataFrame
    └─────────────────────┘        │
         │                         │
         ▼                         │
    ┌─────────────────────┐        │
    │  7. LIMPA DADOS     │        │
    │  Remove totais      │        │ Filtra linhas válidas
    └─────────────────────┘        │
         │                         │
         ▼                         │
    ┌─────────────────────┐        │
    │  8. SERIALIZA JSON  │        │
    │  df.to_json()       │        │ DataFrame → JSON
    └─────────────────────┘        │
         │                         │
         │ JSON estruturado        │
         ▼                         │
    ╔════════════╗                 │
    ║  RESPONSE  ║                 │
    ║  200 OK    ║◀────────────────┘
    ╚════════════╝
```

## 🔐 Como Funciona a Autenticação

### 1. Mecanismo de Autenticação

A API utiliza um sistema de autenticação em **duas etapas**:

#### Fluxograma de Autenticação

```
┌──────────────────────────────────────────────────────────────────────┐
│                    FLUXO DE AUTENTICAÇÃO JWT                         │
└──────────────────────────────────────────────────────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    ETAPA 1: OBTENÇÃO DO TOKEN                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    ┌─────────────┐
    │   Cliente   │
    └──────┬──────┘
           │
           │ POST /login
           │ Authorization: Basic base64(user:pass)
           ▼
    ┌─────────────────────────┐
    │  API valida credenciais │
    │  (libs/users.py)        │
    └────────┬────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
 ┌─────────┐  ┌─────────┐
 │ VÁLIDO  │  │INVÁLIDO │
 └────┬────┘  └────┬────┘
      │            │
      │            └──> ❌ HTTP 401 Unauthorized
      │                   {"error": "Credenciais inválidas"}
      │
      ▼
 ┌──────────────────┐
 │  Gera JWT Token  │
 │  (HS256 + Secret)│
 └────────┬─────────┘
          │
          ▼
 ┌──────────────────────┐
 │  ✓ HTTP 200 OK       │
 │  {"access_token": ..}│
 └──────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                  ETAPA 2: ACESSO AOS RECURSOS                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    ┌─────────────┐
    │   Cliente   │
    └──────┬──────┘
           │
           │ GET /producao
           │ Authorization: Bearer {jwt_token}
           ▼
    ┌───────────────────────┐
    │  @jwt_required()      │
    │  Valida Token JWT     │
    └──────────┬────────────┘
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
 ┌─────────┐      ┌──────────┐
 │ VÁLIDO  │      │ INVÁLIDO │
 └────┬────┘      └─────┬────┘
      │                 │
      │                 ├──> ❌ Token expirado → HTTP 401
      │                 ├──> ❌ Assinatura inválida → HTTP 401
      │                 └──> ❌ Token malformado → HTTP 401
      │
      ▼
 ┌────────────────────┐
 │  Processa Request  │
 │  (Web Scraping)    │
 └─────────┬──────────┘
           │
           ▼
 ┌────────────────────┐
 │  ✓ HTTP 200 OK     │
 │  {dados JSON}      │
 └────────────────────┘
```

### 2. Estrutura do JWT Token

O token JWT contém:
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "username",
    "iat": 1234567890,
    "exp": 1234571490
  },
  "signature": "hash_assinatura"
}
```

### 3. Ciclo de Vida do Token

```
    ╔═══════════════════════════════════════════════════════╗
    ║            CICLO DE VIDA DO JWT TOKEN                 ║
    ╚═══════════════════════════════════════════════════════╝

    ┌───────────────────────────────────────────────────────┐
    │  Estado: TOKEN NÃO EXISTE                             │
    │  Ação: Cliente precisa fazer login                    │
    └────────────────────┬──────────────────────────────────┘
                         │
                         │ POST /login (Basic Auth)
                         ▼
    ┌───────────────────────────────────────────────────────┐
    │  Estado: TOKEN CRIADO                                 │
    │  iat (issued at): 2024-01-01 10:00:00                │
    │  exp (expires): 2024-01-01 10:30:00                  │
    │  ⏱️  TTL: 30 minutos (configurável)                   │
    └────────────────────┬──────────────────────────────────┘
                         │
                         │ Tempo passa...
                         ▼
    ┌───────────────────────────────────────────────────────┐
    │  Estado: TOKEN ATIVO                                  │
    │  ✓ Pode ser usado em requisições                      │
    │  ✓ Assinatura válida                                  │
    │  ✓ Não expirado                                       │
    │                                                        │
    │  GET /producao (Bearer Token) → ✓ 200 OK             │
    │  GET /importacao (Bearer Token) → ✓ 200 OK           │
    └────────────────────┬──────────────────────────────────┘
                         │
                         │ 30 minutos depois...
                         ▼
    ┌───────────────────────────────────────────────────────┐
    │  Estado: TOKEN EXPIRADO                               │
    │  ❌ exp < now()                                        │
    │  ❌ Não pode ser usado                                 │
    │                                                        │
    │  GET /producao (Bearer Token) → ❌ 401 Unauthorized   │
    └────────────────────┬──────────────────────────────────┘
                         │
                         │ Cliente precisa novo token
                         ▼
    ┌───────────────────────────────────────────────────────┐
    │  Ação: RENOVAR TOKEN                                  │
    │  POST /login novamente                                │
    └───────────────────────────────────────────────────────┘

    ╔═══════════════════════════════════════════════════════╗
    ║  NOTA: Tempo de expiração configurável em app.py     ║
    ║  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta() ║
    ╚═══════════════════════════════════════════════════════╝
```

## 🌐 Origem e Processamento dos Dados

### Fonte de Dados: Embrapa Vitibrasil

**URL Base:** http://vitibrasil.cnpuv.embrapa.br/

A Embrapa (Empresa Brasileira de Pesquisa Agropecuária) mantém um banco de dados público sobre a vitivinicultura brasileira, acessível através do portal Vitibrasil.

### Categorias de Dados Disponíveis

| Categoria | Endpoint API | URL Embrapa | Dados |
|-----------|--------------|-------------|-------|
| **Produção** | `/producao` | `?opcao=opt_02` | Vinhos e derivados |
| **Processamento** | `/processamento` | `?opcao=opt_03` | Uvas por tipo |
| **Comercialização** | `/comercializacao` | `?opcao=opt_04` | Vinhos comercializados |
| **Importação** | `/importacao` | `?opcao=opt_05` | Produtos importados |
| **Exportação** | `/exportacao` | `?opcao=opt_06` | Produtos exportados |

### Mapa de Endpoints e Fontes de Dados

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    MAPEAMENTO API → EMBRAPA                           ║
╚═══════════════════════════════════════════════════════════════════════╝

    📍 /producao
    │
    ├─> http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02
    │
    └─> Retorna: Produção de vinhos e derivados
        ┌────────────────────────────────────────┐
        │ • VINHO DE MESA (Tinto, Branco, Rosado)│
        │ • VINHO FINO DE MESA                    │
        │ • SUCO DE UVA                           │
        │ • DERIVADOS                             │
        └────────────────────────────────────────┘

    📍 /processamento
    │
    ├─> http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03&subopcao=subopt_0X
    │
    └─> Retorna: Processamento de uvas por categoria
        ┌────────────────────────────────────────┐
        │ • VINÍFERAS (Cabernet, Merlot, etc)    │
        │ • AMERICANAS (Isabel, Bordô, etc)      │
        │ • UVAS DE MESA (Itália, Rubi, etc)     │
        │ • SEM CLASSIFICAÇÃO                     │
        └────────────────────────────────────────┘

    📍 /comercializacao
    │
    ├─> http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04
    │
    └─> Retorna: Comercialização no mercado interno
        ┌────────────────────────────────────────┐
        │ • VINHO DE MESA                         │
        │ • VINHO FINO                            │
        │ • ESPUMANTES                            │
        │ • OUTROS                                │
        └────────────────────────────────────────┘

    📍 /importacao
    │
    ├─> http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05&subopcao=subopt_0X
    │
    └─> Retorna: Dados de importação por país
        ┌────────────────────────────────────────┐
        │ País | Quantidade (Kg) | Valor (US$)   │
        │────────────────────────────────────────│
        │ • VINHOS DE MESA                        │
        │ • ESPUMANTES                            │
        │ • UVAS FRESCAS                          │
        │ • UVAS PASSAS                           │
        │ • SUCO DE UVA                           │
        └────────────────────────────────────────┘

    📍 /exportacao
    │
    ├─> http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06&subopcao=subopt_0X
    │
    └─> Retorna: Dados de exportação por país
        ┌────────────────────────────────────────┐
        │ País | Quantidade (Kg) | Valor (US$)   │
        │────────────────────────────────────────│
        │ • VINHOS DE MESA                        │
        │ • ESPUMANTES                            │
        │ • UVAS FRESCAS                          │
        │ • SUCO DE UVA                           │
        └────────────────────────────────────────┘
```

### Processo de Web Scraping

#### Diagrama do Pipeline de Dados

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃              PIPELINE DE PROCESSAMENTO DE DADOS                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌─────────────┐
│   INPUT     │  URL + Parâmetros (ano)
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 1: HTTP REQUEST                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  requests.get(url, timeout=30)                          │   │
│  │  • User-Agent: Python/Requests                          │   │
│  │  • Accept: text/html                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼  HTML Response
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 2: HTML PARSING                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  BeautifulSoup(response.text, 'html.parser')            │   │
│  │  • Localiza: <table> específica (índice 4)              │   │
│  │  • Extrai: Estrutura completa da tabela                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼  HTML Table
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 3: CONVERSÃO PARA DATAFRAME                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  pd.read_html(str(table))[0]                            │   │
│  │  • Converte tabela HTML → DataFrame                     │   │
│  │  • Identifica headers automaticamente                   │   │
│  │  • Mantém tipos de dados originais                      │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼  Raw DataFrame
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 4: FILTRAGEM DE COLUNAS                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  df = df[columns]                                       │   │
│  │  • Remove colunas desnecessárias                        │   │
│  │  • Mantém apenas dados relevantes                       │   │
│  │  Exemplo: ["Produto", "Quantidade (L.)"]                │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼  Filtered DataFrame
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 5: LIMPEZA DE DADOS                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  for index, row in df.iterrows():                       │   │
│  │      value = row[columns[1]].split(".")                 │   │
│  │      if not value[0].isdigit():                         │   │
│  │          df.drop(index, inplace=True)                   │   │
│  │                                                          │   │
│  │  Remove:                                                 │   │
│  │  ❌ Linhas de TOTAL                                      │   │
│  │  ❌ Linhas de SUBTOTAL                                   │   │
│  │  ❌ Cabeçalhos duplicados                                │   │
│  │  ❌ Valores não numéricos                                │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼  Clean DataFrame
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 6: SERIALIZAÇÃO JSON                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  json_data = df.to_json(orient='records', lines=False) │   │
│  │  json_data = json.loads(json_data)                      │   │
│  │                                                          │   │
│  │  Formato:                                                │   │
│  │  [                                                       │   │
│  │    {"Produto": "VINHO", "Quantidade": "123.456"},      │   │
│  │    {"Produto": "SUCO", "Quantidade": "78.910"}         │   │
│  │  ]                                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────┐
│   OUTPUT    │  JSON estruturado
└─────────────┘
```

#### Passo a Passo:

1. **Requisição HTTP**
   ```python
   response = requests.get(url, timeout=30)
   ```
   - Timeout de 30 segundos para evitar travamentos
   - Suporta filtros por ano via query string

2. **Parsing HTML**
   ```python
   soup = BeautifulSoup(response.text, 'html.parser')
   table = soup.find_all('table')[4]  # 5ª tabela da página
   ```
   - Utiliza parser lxml para performance
   - Extrai a tabela específica com os dados

3. **Conversão para DataFrame**
   ```python
   df = pd.read_html(str(table))[0]
   df = df[columns]  # Filtra colunas relevantes
   ```
   - Pandas converte HTML table para DataFrame
   - Seleciona apenas colunas necessárias

4. **Limpeza de Dados**
   ```python
   for index, row in df.iterrows():
       value = row[columns[1]]
       result = value.split(".")
       if not result[0].isdigit():
           df.drop(index, inplace=True)
   ```
   - Remove linhas com totais e subtotais
   - Mantém apenas dados numéricos válidos

5. **Serialização JSON**
   ```python
   json_data = df.to_json(orient='records', lines=False)
   json_data = json.loads(json_data)
   ```
   - Converte DataFrame para formato JSON
   - Estrutura em lista de objetos

### Exemplo de Transformação

**Entrada (HTML da Embrapa):**
```html
<table>
  <tr><td>Produto</td><td>Quantidade (L.)</td></tr>
  <tr><td>VINHO DE MESA</td><td>217.788.008</td></tr>
  <tr><td>Tinto</td><td>104.455.024</td></tr>
  ...
</table>
```

**Saída (JSON da API):**
```json
{
  "Producao_2021": [
    {
      "Produto": "VINHO DE MESA",
      "Quantidade (L.)": "217.788.008"
    },
    {
      "Produto": "Tinto",
      "Quantidade (L.)": "104.455.024"
    }
  ]
}
```

### Tratamento de Erros no Scraping

A API implementa tratamento robusto de erros:

```python
try:
    response = requests.get(link, timeout=30)
    # ... processamento ...
except Exception as ex:
    raise CustomConnectionError("Erro ao carregar os dados") from ex
```

**Possíveis erros tratados:**
- Timeout de conexão
- Site fora do ar
- Mudança na estrutura HTML
- Dados ausentes ou malformados

## ✨ Funcionalidades

- 📊 Consulta de dados de produção de vinhos e derivados
- 🍇 Processamento de uvas por tipo (viníferas, americanas, híbridas e de mesa)
- 💼 Dados de comercialização de vinhos
- 📥 Estatísticas de importação (vinhos, espumantes, uvas e sucos)
- 📤 Estatísticas de exportação (vinhos, espumantes, uvas e sucos)
- 📅 Filtros por ano específico ou intervalo de anos (1970-2023)
- 🔒 Autenticação segura via JWT (JSON Web Tokens)
- 📚 Documentação interativa com Swagger/OpenAPI
- 🚀 API RESTful com respostas JSON estruturadas
- ⚡ Web scraping em tempo real dos dados da Embrapa

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Flask** - Framework web
- **Flask-JWT-Extended** - Autenticação JWT
- **Pandas** - Processamento de dados
- **BeautifulSoup4** - Web scraping
- **Requests** - Requisições HTTP
- **Flasgger** - Documentação Swagger/OpenAPI

## 📦 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd Tech-Challenge-F1
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

A API estará disponível em `http://127.0.0.1:5000`

## 🚀 Utilização da API

### Autenticação

O sistema utiliza JSON Web Tokens (JWT) para autenticação nos endpoints. Antes de acessar qualquer endpoint protegido, você precisa obter um token de acesso.

### 1. Obtenção do Token

Faça uma requisição POST para o endpoint de login:

**Endpoint:** `POST http://127.0.0.1:5000/login`

**Cabeçalho:**
```
Authorization: Basic {credenciais_em_base64}
```

O formato das credenciais em base64 deve ser: `usuario:senha`

**Exemplo de requisição:**
```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Authorization: Basic cHJvZHVjYW86cHJAMTAyMDMw"
```

**Credenciais disponíveis:**
- Usuário: `producao` | Senha: `pr@102030`
- Usuário: `testeDev` | Senha: `te@102030`
- Usuário: `usuario` | Senha: `us@102030`

**Resposta de sucesso:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Uso do Token

Utilize o token obtido no cabeçalho `Authorization` de todas as requisições subsequentes:

```
Authorization: Bearer {access_token}
```


## 🔌 Endpoints Disponíveis

### 1. Login (Público)

**GET /** `/login`
- **Descrição:** Retorna o token JWT para autenticação
- **Autenticação:** Basic Auth
- **Resposta:** Token de acesso JWT

---

### 2. Produção (Protegido)

**GET** `/producao`
- **Descrição:** Dados de produção de vinhos e derivados
- **Autenticação:** Bearer Token (JWT)
- **Parâmetros de Query:**
  - `ano` (opcional): Ano específico (ex: `2021`) ou intervalo (ex: `1999-2023`)
- **Retorna:**
  - Produção de vinhos
  - Produção de sucos e derivados

**Exemplo:**
```bash
curl -X GET "http://127.0.0.1:5000/producao?ano=2021" \
  -H "Authorization: Bearer {seu_token}"
```

---

### 3. Processamento (Protegido)

**GET** `/processamento`
- **Descrição:** Dados de processamento de uvas por tipo
- **Autenticação:** Bearer Token (JWT)
- **Parâmetros de Query:**
  - `ano` (opcional): Ano específico ou intervalo
- **Retorna:**
  - Uvas viníferas processadas
  - Uvas americanas processadas
  - Uvas híbridas processadas
  - Uvas de mesa processadas

**Exemplo:**
```bash
curl -X GET "http://127.0.0.1:5000/processamento?ano=2020-2023" \
  -H "Authorization: Bearer {seu_token}"
```

---

### 4. Comercialização (Protegido)

**GET** `/comercializacao`
- **Descrição:** Dados de comercialização de vinhos e derivados
- **Autenticação:** Bearer Token (JWT)
- **Parâmetros de Query:**
  - `ano` (opcional): Ano específico ou intervalo
- **Retorna:** Dados de comercialização de vinhos

**Exemplo:**
```bash
curl -X GET "http://127.0.0.1:5000/comercializacao" \
  -H "Authorization: Bearer {seu_token}"
```

---

### 5. Importação (Protegido)

**GET** `/importacao`
- **Descrição:** Dados de importação de produtos vitivinícolas
- **Autenticação:** Bearer Token (JWT)
- **Parâmetros de Query:**
  - `ano` (opcional): Ano específico ou intervalo
- **Retorna:**
  - Importação de vinhos de mesa
  - Importação de espumantes
  - Importação de uvas frescas
  - Importação de uvas passas
  - Importação de suco de uva

**Exemplo:**
```bash
curl -X GET "http://127.0.0.1:5000/importacao?ano=2022" \
  -H "Authorization: Bearer {seu_token}"
```

---

### 6. Exportação (Protegido)

**GET** `/exportacao`
- **Descrição:** Dados de exportação de produtos vitivinícolas
- **Autenticação:** Bearer Token (JWT)
- **Parâmetros de Query:**
  - `ano` (opcional): Ano específico ou intervalo
- **Retorna:**
  - Exportação de vinhos de mesa
  - Exportação de espumantes
  - Exportação de uvas frescas
  - Exportação de suco de uva

**Exemplo:**
```bash
curl -X GET "http://127.0.0.1:5000/exportacao?ano=2015-2023" \
  -H "Authorization: Bearer {seu_token}"
```

---

## Parâmetros de Consulta

Todos os endpoints (exceto `/login`) aceitam o parâmetro `ano` para filtrar dados:

### Consulta por ano específico:
```
http://127.0.0.1:5000/producao?ano=2021
```

### Consulta por intervalo de anos:
```
http://127.0.0.1:5000/producao?ano=1999-2023
```

**Intervalo válido:** 1970 a 2023

---

## 📚 Documentação Swagger

Acesse a documentação interativa da API através do Swagger UI:

```
http://127.0.0.1:5000/apidocs
```

A interface Swagger permite testar todos os endpoints diretamente no navegador.

---

## 📁 Estrutura do Projeto

```
Tech-Challenge-F1/
├── app.py                      # Aplicação principal Flask
├── errors.py                   # Classes de exceções customizadas
├── requirements.txt            # Dependências do projeto
├── swagger.yaml               # Especificação OpenAPI/Swagger
├── libs/
│   ├── request_function.py    # Funções de requisição e processamento de dados
│   ├── users.py              # Dados de usuários para autenticação
│   └── validations.py        # Funções de validação de parâmetros
└── README.md                 # Este arquivo
```

---

## ⚠️ Tratamento de Erros

A API retorna os seguintes códigos de status HTTP:

- **200 OK** - Requisição bem-sucedida
- **400 Bad Request** - Parâmetros inválidos (ex: ano fora do intervalo válido)
- **401 Unauthorized** - Credenciais inválidas ou token ausente
- **500 Internal Server Error** - Erro ao processar dados ou conexão com fonte externa

**Exemplo de resposta de erro:**
```json
{
  "error": "Ano ou Intervalo inválido"
}
```

---

## Fonte de Dados

Os dados são obtidos do site da Embrapa (Empresa Brasileira de Pesquisa Agropecuária):
- **URL Base:** http://vitibrasil.cnpuv.embrapa.br/

A API realiza web scraping dos dados públicos e os disponibiliza em formato JSON estruturado.

---

## 🔒 Segurança

- 🛡️ Autenticação JWT para proteção dos endpoints
- Tokens com tempo de expiração configurável
- **IMPORTANTE:** Em produção, altere a chave secreta JWT em `app.py`:
  ```python
  app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta_aqui'
  ```

---

## 🤝 Contribuição

Para contribuir com este projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é um **Tech Challenge** desenvolvido para fins educacionais.

---

## 📞 Contato e Suporte

Para dúvidas, sugestões ou reportar problemas, abra uma issue no repositório do projeto.

---

<div align="center">

### 🌟 Se este projeto foi útil, considere dar uma estrela! ⭐

**Desenvolvido com** ❤️ **para o Tech Challenge**

**Última atualização:** 16-07-2024

</div>

---

## 📊 Status do Projeto

```
┌─────────────────────────────────────────────────────────────┐
│  ✅ Autenticação JWT implementada                           │
│  ✅ Web scraping funcional                                  │
│  ✅ 6 endpoints de dados disponíveis                        │
│  ✅ Documentação Swagger completa                           │
│  ✅ Tratamento de erros robusto                             │
│  ✅ Código com qualidade (Pylint: 9.82/10)                  │
│  ✅ Testes de integração com Embrapa                        │
└─────────────────────────────────────────────────────────────┘
```

---

<div align="center">

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-green?style=flat-square)](https://flask.palletsprojects.com/)
[![JWT](https://img.shields.io/badge/Auth-JWT-orange?style=flat-square)](https://jwt.io/)

</div>
