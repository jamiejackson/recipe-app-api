
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
* Create user
* Go to api/user/token to get the token
* Authenticate with that user in Authentication under Token Auth. Format as follows (notice `Token ` literal prefix.)
    ```
    Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ```
*
