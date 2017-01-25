# Aplicativo Pergunte - Backend

**UNIVERSIDADE FEDERAL DE SÃO CARLOS**<br>
Centro de Ciências Exatas e de Tecnologia<br>
Departamento de Computação<br>
Metodologias de Desenvolvimento de Sistemas - semestre 2016/2<br>
Prof. Dr. Fabiano Cutigi Ferrari

Aluno | RA | GitHub
------------ | ------------- | --------------
Danilo Guarnieri Cardoso | 413437 | [dcardos](https://github.com/dcardos)
Marcelo de Oliveira da Silva | 489085 | [marcelodeolive1ra](https://github.com/marcelodeolive1ra)
Rodolfo Barcelar | 495921 | [rophos_rb](https://github.com/rophos_rb)
Thiago Yonamine | 587001 | [ThiagoYonamine](https://github.com/ThiagoYonamine)

## Descrição do Trabalho

Este repositório é um projeto Django com o backend para o aplicativo Pergunte, que está sendo desenvolvido para a plataforma Android, como projeto final da disciplina.

O código do aplicativo Android, bem como uma descrição mais detalhada do projeto da disciplina está disponível [neste repositório](https://github.com/marcelodeolive1ra/pergunte).

## Créditos de utilização de frameworks e bibliotecas de código aberto

- [Django 1.10.5](https://github.com/django/django)
- [pyqrcode](https://github.com/mnooner256/pyqrcode)
- [PyPNG](https://github.com/drj11/pypng)
- [SendGrid Python](https://github.com/sendgrid/sendgrid-python)

Para instalar essas dependências: `pip install -r requirements.txt`.

## Configuração do envio de e-mails via API do SendGrid

- O SendGrid tem um plano gratuito com limite de envio de 10.000 e-mails por mês. Basta criar uma conta em [sendgrid.com](http://sendgrid.com).
- Criar um arquivo `/api_keys/sendgrid.txt` com uma chave de API do SendGrid escrita na primeira linha do arquivo. A chave criada deve ter permissão de envio de e-mails. 

