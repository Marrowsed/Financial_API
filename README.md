[![Financial APP](https://github.com/Marrowsed/Financial_API/actions/workflows/python-app.yml/badge.svg)](https://github.com/Marrowsed/Financial_API/actions/workflows/python-app.yml)
[![CodeQL](https://github.com/Marrowsed/Financial_API/actions/workflows/codeql.yml/badge.svg)](https://github.com/Marrowsed/Financial_API/actions/workflows/codeql.yml)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<h1>Tecnologies and Frameworks</h1>
<img src="https://www.django-rest-framework.org/img/logo.png" alt="Django Rest Framework">
<ul>
<li><a href="https://www.djangoproject.com/" target="_blank">Django</a> - O propósito do Django está no desenvolvimento de aplicações web e sites.</li>
<li><a href="https://www.django-rest-framework.org/" target="_blank">Django Rest Framework</a> - Desenvolvimento de web API'S de forma simples e ágil.</li>
</ul>


<h1>Financial API</h1>
Your control by:
<ul>
  <li><a href="#receitas">Revenues</a></li>
  <li><a href="#despesas">Expenses</a></li>
</ul>

<h1>Methods</h1>
<ul>
  <li>GET - Return Info</li>
  <li>POST - Insert Info</li>
  <li>PUT - Update Info</li>
  <li>DELETE - Delete Info</li>
</ul>

<h1>Endpoints</h1>

<h2 id="receitas">Revenue [GET/POST/PUT/DELETE]</h2>
<ul><b>Basic Auth</b>
  <li>username</li>
  <li>password</li>
</ul>  

<ul>
  <li>/revenue/ [GET]</li>
  <b>Revenue List</b>
  <li>/revenue/ [POST]</li>
  <b>Insert a new Revenue</b>
  <li>/revenue/{pk}/ [PUT/DELETE]</li>
  <b>Update / Delete a Revenue</b>
  <li>/revenue/{yyyy}/{mm} [GET]</li>
  <b>List the filter revenue</b>
  <li>/revenue/?description= [GET]</li>
  <b>List the revenue description</b>
</ul>

<b> Request example: </b>
  ```json
  [
	{
		"description": "Revenue Description",
		"value": 1000,
		"date": "25-12-2000"
	},
  ]
  ```

<b> 200 Return: </b>
  ```json
  [
	{
		"id": "Revenue ID",
		"description": "Revenue Description",
		"value": 1000,
		"date": "25-12-2000"
	},
  ]
  ```
<b> Bad Request: </b>
```json
{
	"detail": "Registry already exists"
}
```

<h2 id="expense">Expense [GET/POST/PUT/DELETE]</h2>

<ul>
  <li>/expense/ [GET]</li>
  <b>Expense List</b>
  <li>/expense/ [POST]</li>
  <b>Insert a new Expense</b>
  <li>/expense/{pk}/ [PUT/DELETE]</li>
  <b>Update / Delete a Registry</b>
  <li>/expense/{yyyy}/{mm} [GET]</li>
  <b>List the filter Expense</b>
  <li>/expense/?description= [GET]</li>
  <b>Expense by description</b>
</ul>

<b> Request example: </b>
  ```json
  [
	{
		"description": "Revenue Description",
		"value": 1000,
                "category": "Food",
		"date": "25-12-2000"
	},
  ]
  ```
<b> 200 Response:</b>

  ```json
  [
	{
		"id": "Expense ID",
		"description": "Expense Description",
		"category": "Expense Category",
		"value": 1000,
		"date": "25-12-2000"
	}
  ]
  ```

<b> Bad Request: </b>
```json

{
	"detail": "Registry already exists"
}

```

<h2>Summary [GET]</h2>
<p>Summary of the month</p>
<ul>
  <li>/summary/{yyyy}/{mm} [GET]</li>
</ul>
<b> 200 Example:</b>

  ```json
{
	"Revenue/Month": 5000
	"Expense/Month": 2000,
        "End of the Month": 3000
	"Category": [
		{
			"category": "Category",
			"Total_Value": 500
		}
	],
}
  ```
  
<b> Bad Request: </b>
```json

{
	"detail": "No registry"
}

```

<h1> Install </h1>
<a href="https://www.python.org/downloads/" target="_blank">Python</a> latest

<h2>Dependencies</h2>

````sh
pip install -r requirements.txt
````

<h1> Config </h1>
<ol>
  <li>Create an `.env` file in the same folder where `migrate.py` is.</li>
  <li>In your terminal with venv, execute `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` generating a new secret key</li>
  <li>Insert the new secret key in `.env` file like this: `SECRET_KEY = oahsdodjifodjfodjfpadjpajsdpojsd` .</li>
  <li>Insert the database URL in the `.env` file like this: `DATABASE_URL = your_db://your_db:password@localhost/my_db`.</li>
  <li>Run `python manage.py migrate` and create the tables</li>
</ol>

<h1>Running</h1>

```sh
python manage.py runserver
```

Server is running in http://127.0.0.1:8000/, access your browser !