# Pyhon-Django Project

Vesrion 1.0.1

## About Project

Objective of the project is to create a website with news.

### How does it works

Parsing data from any rss website -> making parsed data human-readable -> adding it to a database -> placing data from the database on a webisite created with Django framework.

## Getting Started

### Instaling

Install Django:
  `pip-install Django` 
  
Clone this repository:
  `git clone https://github.com/Alex27Khalupka/Pyhon-Django-Project.git`
  
### Working with utility

To parse data from any website use: `python manage.py new_parse web_site_url`
  
Example:
  `python manage.py new_parse https://www.yahoo.com/news/rss`
  
  
To run created web-site use: `python manage.py runserver`
  
Web-site url: `http://127.0.0.1:8000/`
  
## Built with
  * [Pyhton 3.7](https://www.python.org/downloads/release/python-370/)
  * ["Django"](https://www.djangoproject.com/) - The web framework
  * ["feedparser"](https://pythonhosted.org/feedparser/) - Python lib for feed parsing.
  
## Authors 
  * Aliaksandr Khalupka
