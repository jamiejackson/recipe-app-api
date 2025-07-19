
```sh
docker compose run --rm app sh -c "python manage.py test && flake8"
```

```sh
docker compose run --rm app sh -c "python manage.py createsuperuser"
```

```sh
docker compose run --rm app sh -c "python manage.py startapp user"
```

In API Docs:
* Create user (`user2@example.com`/`Awesome!23`)
* Go to api/user/token to get the token
* Authenticate with that user in Authentication under Token Auth. Format as follows (notice `Token ` literal prefix.)
    ```
    Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ```
*

Review [Views](https://www.udemy.com/course/django-python-advanced/learn/lecture/32237046#overview) because I don't completely follow.
- APIViews
    - Focused around HTTP methods
    - Class methods for HTTP methods
        - GET, POST, PUT, PATCH, DELETE
    - Provide flexibility over URLs and logic
    - Useful for _non_ CRUD APIs
        - Avoid for simple CRUD APIs
        - Anything that doesn't map to your models
        - Bespoke logic (e.g., auth, jobs, external apis)
- Viewsets:
    - Focused around actions
        - Retrieve, list, update, partial update, destroy
    - Map to Django models
    - Use routers to generate URLs
    - Great for CRUD operations on models


```sh
docker compose run --rm app sh -c "python manage.py makemigrations"

docker compose run --rm app sh -c "python manage.py makemigrations"
```
