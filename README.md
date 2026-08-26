# cs50w-pset2
Source code for CS50W's Problem Set 2: Commerce 

About the Problem Set : https://cs50.harvard.edu/web/projects/2/commerce/

---

## Overview

TODO

---

## Use the project with uv and docker

This project uses uv, a modern Python package and project manager, and the container manager tool Docker

More info here:
- https://docs.astral.sh/uv/
- https://docs.docker.com/get-started/

- Install Docker, then in the terminal once you are in the project folder execute the following commands

~~~
$ docker compose up
$ docker compose exec web uv run manage.py makemigrations
$ docker compose exec web uv run manage.py migrate
~~~

The project should now be available at http://127.0.0.1:8000/

---

## Notes

- The project has been tested with Python 3.12+.

- Dependencies are defined in pyproject.toml (handled automatically by uv sync).

- No additional configuration is required before running the server.

---

*Developed as part of Harvard’s CS50W course.*
