## ONBOARDING US GET W8 BEN DOCUMENT
#### _FISSION PARA RETORNAR O W8 BEN DOCUMENT

- O formulário W-8 é um documento fornecido pela Internal Revenue Service, que é o equivalente a nossa Receita Federal. Existem diversos formulários da “família” W8, mas os principais são: W8-BEN, que é para pessoas físicas, e o W-8BEN-E, para empresas.

- Ele serve para que um prestador de serviços comprove que não é contribuinte fiscal nos Estados Unidos, ou seja, diminui ou isenta a retenção de impostos sobre o dinheiro pelo serviço prestado.
___
### Esse projeto refere-se a rota do Sphinx:

```
UserService.get_w8_form
```
&nbsp; 
### 1.1. `get-w8-ben`
&nbsp; 
#### MODELO DE REQUISIÇÃO:

```http://127.0.0.1:9000/get-w8-ben```

&nbsp; 
##### BODY REQUEST
```
Não há body request nem Query Params
```
&nbsp;

#### MODELO DE RESPOSTA:

```
{
    "result": "https://d1gfu8yyntzl2k.cloudfront.net/02e73c7d-fd38-44f0-acfe-d877de5e037d.pdf?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vZDFnZnU4eXludHpsMmsuY2xvdWRmcm9udC5uZXQvMDJlNzNjN2QtZmQzOC00NGYwLWFjZmUtZDg3N2RlNWUwMzdkLnBkZiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTY1NzY2MTcxOX0sIklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIwLjAuMC4wLzAifX19XX0_&Signature=ZfHOY8ypk-~8qxtWG5M1Mw3URB-QMi2wFUfShGkCP2z5jazRFR6NYF-UWxPM1P0hugA1l3VIFQCkJKTExE-BDAGnrJMyZDoA2JA9k98tXJjJFJN9Prfgidhc-emGYn4jg-pyiN4VK2~g-olrQLiYwnYzHQj6i4FyxDzr-AxcOrVgpDRK75a83MjWDRVGt53QMaFFJ9QPQxEz8JZKrh-n1Ag461jwlvJWsOw8UNLJsVZwRUcNiPiP3AVdyMYQ-QqjINIfv8YbyEoHdhFPBfgJj0ZbzHIMImhlDquPU1ir4x49uFRKa1A0cGPb9-KzBSbi0owwxX3r5e0GsQILFiUAhg__&Key-Pair-Id=APKAJD7VLH4OKOE2R73Q",
    "message": "The W8 BEN Link was generated successfully",
    "success": true,
    "code": 0
}
```
&nbsp;
#### RODAR SCRIPT DE TESTS:

- No mesmo nível da pasta root, rodar o seguinte comando no terminal: `bash tests.sh`

&nbsp;