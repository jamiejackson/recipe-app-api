
```sh
docker compose run --rm app sh -c "python manage.py test && flake8"
```

```sh
docker compose run --rm app sh -c "python manage.py createsuperuser"
```

```sh
docker compose run --rm app sh -c "python manage.py startapp user"
```