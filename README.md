# BikeUnit App

Este tutorial servirá para mostrar o uso da API do app bikeunit.
A API para testes poderá ser acessada na URL https://www.testenv.com.br/

## Recursos de autenticação

Os recursos apresentados a seguir dizem respeito ao registro, login e atualização no que no que diz respeito a autenticação do usuario. O uso de outras informações será disponibilizado na seção de `perfil do usuario`

### Registro de Usuário

Para criar um novo usuario a seguinte url deverá ser acessada: https://www.testenv.com.br/api/autenticacao/usuario/registra/

**A requisição do registro deve ser feita utilizando o método `POST`.**

O header da requisição deve conter:
`Content-Type: application/json`

O corpo da requisição deve ser contruido no formato JSON da seguinte maneira:

    {
        "user": {
            "email": "(email do usuario)",
            "password": "(senha do usuario)",
            "username":"(nome do usuario)"
        }
    }

A resposta do servidor será como segue:

    {
        "user": {
            "pk": (id do usuario - pk é a abreviação de primary key),
            "email": "(email do usuario)",
            "username": "(nome do usuario)",
            "token": "(token de identificação)"
        }
    }

### Login 

Para fazer o login de um usuario a seguinte url deverá ser acessada: https://www.testenv.com.br/api/autenticacao/usuario/login/

**A requisição do login deve ser feita utilizando o método `POST`.**

O header da requisição deve conter:
`Content-Type: application/json`

O corpo da requisição deve ser contruido no formato JSON da seguinte maneira:

    {
        "user": {
            "email": "(email do usuario)",
            "password":"(senha do usuario)"
        }
    }
A resposta do servidor será como segue:

    {
        "user": {
            "pk": (id do usuario - pk é a abreviação de primary key),
            "email": "(email do usuario)",
            "username": "(nome do usuario)",
            "token": "(token de identificação)"
        }
    }

### Update

Para fazer o update de um usuario a seguinte url deverá ser acessada: https://www.testenv.com.br/api/autenticacao/usuario/atualiza/

**A requisição do update deve ser feita utilizando o método `PUT`.**

O header da requisição deve conter:

`Content-Type: application/json`
`Authorization: Token (token do usuario)`

O corpo da requisição deve ser contruido no formato JSON da seguinte maneira:

    {
        "user":{
            "email": "(email do usuario)",
            "username": "(nome do usuario)",
            "password": "(senha do usuario)"
        }
    }

A resposta do servidor será como segue:

    {
        "user": {
            "pk": (id do usuario - pk é a abreviação de primary key),
            "email": "(email do usuario)",
            "username": "(nome do usuario)",
            "token": "(token de identificação)"
        }
    }
