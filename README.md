# cs50w-pset2
Source code for CS50W's Problem Set 2: Commerce 

Source code for CS50 Web Programming with Python and JavaScript (Problem Set 2: Commerce).

Course specifications: https://cs50.harvard.edu/web/projects/2/commerce/

---

## Prerequisites

- **Docker** & **Docker Compose**
- **Make** (optional, but recommended for shortcut commands)

---

## Quick start (with Makefile)

1. **Start the application:**

~~~
make dev
~~~

(Use make dev-build if you updated the Dockerfile or dependencies)


2. **Run database migrations:**

~~~
make migrate
~~~

3. **Create the admin user: (optional):**

~~~
make superuser
~~~

4. **Open your browser at http://127.0.0.1:8000/**


## Tech Stack & Notes

- Python: 3.13
- Framework: Django 5.2+
- Package Manager: uv
- Containerization: Docker & Docker Compose

*Developed as part of Harvard’s CS50W course.*
https://cs50.harvard.edu/web/



