# TECH-CHALLENGE

# DOCUMENTAÇÃO SWAGGER <H6>
# /apiDocs <H2>
>
## INSTALAÇÃO DAS DEPENDÊNCIAS:
    
    Use o comando pip install -r requirements.txt

## UTILIZAÇÃO DA API

O sistema utiliza JSON Web Tokens (JWT) para autenticação nos endpoints, permite que um servidor emita um token para um cliente que pode ser usado para autenticar o cliente em solicitações subsequentes.

## 1° OBTENÇÃO DO TOKEN:

Rodando projeto local via POSTMAN enviar uma requeisção POST para o seguinte endpoint:
    <http://127.0.0.1:5000/login>

### Cabeçalho Authorization
        
    Authorization: Basic {credenciais em base 64 no formato usuário:senha}
        
#### Exemplo a ser utilizado na requisição:

    {Authorization: "Basic cHJvZHVjYW86cHJAMTAyMDMw"} > Cabeçalho já com o usuário e senha.


Esse requisição deve retornar o {access_token:"xy"} que será utilizado nas próximas requisições.


## ENDPOINTS DO PROJETO E INFORMAÇÕES FORNECIDAS:
    
> ### /login 
>   
> - Retorna o token que será utilizado nas requisições.

______________________________________________________________________________

> ### /producao 
>
> - Produção de vinhos.
> - Produção de sucos e derivados.

______________________________________________________________________________

> ### /processamento 
>
> - Uvas viníferas processadas.
> - Uvas americanas.
> - Uvas híbridas processadas. 
> - Uvas de mesa processadas.

______________________________________________________________________________

> ### /comercializacao 
>
> - Comercialização de vinhos e derivados.

______________________________________________________________________________

> ### /importacao 
>
> - Importação de vinhos de mesa.
> - Importação de espumantes.
> - Importação de uvas frescas.
> - Importação de uvas passas.
> - Importação de suco de uva.

______________________________________________________________________________

> ### /exportacao 
>
> - Exportação de vinhos de mesa.
> - Exportação de espumantes.
> - Exportação de uvas frescas.
> - Exportação de suco de uva.
    
______________________________________________________________________________

Todos os endpoint possuem a opção de seleção de dados com base no ano ou intervalo.

* Exemplo de consulta com ano especifico:     

    [http://127.0.0.1:5000?ano=2021]


* Exemplo de consulta com um intervalo:

    [http://127.0.0.1:5000?ano=1999-2023]
