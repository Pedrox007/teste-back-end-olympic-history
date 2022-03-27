# Teste Celero

### 📝 Descrição

Este projeto faz parte do teste para a vaga de Desenvolvedor Back-end da Celero. Ele consiste em um crud com base nas informações do dataset “120 years of
Olympic history: athletes and results” presente no [Kaggle](https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results#athlete_events.csv). A partir dos dados presentes nas colunas do csv, foi conceituado e criado um modelo relacional com a seguinte arquitetura:

![Diagrama Relacional](static/diagram.png)

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:
* Você possui `Python 3+`
* Você possui `Poetry`
* Você possui `PostgreSQL 9.4`.

## 🚀 Instalando teste_celero

Para instalar o teste_celero, siga estas etapas:

Primeiramente, crie um arquivo `.env` na raiz do projeto. Abrindo ele, insira as seguintes variáveis de ambiente substituindo os valores entre `<>` para os seus valores locais:
```
SECRET_KEY=<sua_secret_key>
DATABASE_URL="postgres://<usuario_postgres>:<senha_postgres>@localhost:5432/<nome_banco>"
```

Após isso, basta rodar o seguinte comando para criar a virtual environment:
```
poetry install
```

Uma vez estando na raiz do projeto. Rode o seguinte comando para iniciar a importação dos dados, que estão em `data/athlete_events.csv`, para o banco do projeto:

```
python manage.py importcsvdata
```

>❗ Como o comando trata do caminho para o csv internamente, caso queira inserir seus próprios dados seguindo a mesma arquitetura da base de dados original, basta substituir o arquivo em `data/` utilizando o mesmo nome: `athlete_events.csv`.

Com isso, o projeto está devidamente instalado. Agora basta rodar o seguinte comando para iniciar o `Django Server`:
```
python manage.py runserver
```

Finalmente o projeto estará rodando no seu [localhost](http://localhost:8000/admin).

## ☕ Usando <nome_do_projeto>

Para usar <nome_do_projeto>, siga estas etapas:

```
<exemplo_de_uso>
```

