A Django project representing an e-shop with a single endpoint. The endpoint allows GET requests in the format
`shop/report/YYYY-MM-DD/` and will return metrics on sales for that day.

### Usage
This project uses an SQLite database that can be created using `python manage.py migrate`. The database can be populated
with sample data using `python manage.py populate_data`. The shop app can be launched from an environment with the
requirements installed by running `python manage.py runserver`.

Included in the project is a `setup.sh` shell script which will install the necessary requirements,
create the database, populate it with sample data, prompt the user to create an admin account and then launch the app locally.

### Requirements
Python 3.6  
Django 3.0  
Django REST framework 3.11

### Sample response:


     {
        "customers": 9,
        "total_discount_amount": 15152814.736907512,
        "items": 2895,
        "order_total_avg": 15895179.735734595,
        "discount_rate_avg": 0.13145131216518066,
        "commissions": {
            "promotions": {
                "5": 1153804.8,
                "2": 188049.40000000002
            },
            "total": 20833236.938148536,
            "order_average": 2314804.104238726
        }
    }


