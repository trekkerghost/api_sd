# API CRUD Challenge for SD

[![Build Status](https://travis-ci.org/trekkerghost/api_sd.svg?branch=master)](https://travis-ci.org/trekkerghost/api_sd)

[![Coverage Status](https://coveralls.io/repos/github/trekkerghost/api_sd/badge.svg?branch=master)](https://coveralls.io/github/trekkerghost/api_sd?branch=master)

[![Maintainability](https://api.codeclimate.com/v1/badges/59aa134fde4a3901694b/maintainability)](https://codeclimate.com/github/trekkerghost/api_sd/maintainability)

Creación de API usando Python y Django

## Features

1. listar todos los productos GET
2. crear un producto POST
3. obtener producto por id GET
4. actualizar producto por id PUT
5. eliminar producto por id DELETE
6. actualizar un conjunto de elementos PUT
7. Endpoint Pagination
    > Implementación manual. En la repuesta estan todos los links necesarios _first_, _next_,_previous_, _last_, _page count_, _element count_
8. Integracion continua con Travis CI
9. Configuracion de CodeClimate
10. Documentado con Postman. link en sección siguiente
11. Deployed to heroku at <https://sdcpe-api.herokuapp.com/api/>

## Uso

Documentacion POSTMAN
<https://documenter.getpostman.com/view/3755425/api_sd/RVfzhVWf>

## Software

Versiones utilizadas:

1. Python 3.5.2
2. Django 1.11
3. PostgreSQL 9.5.1

## Pasos para deploy

Crear base de datos

`psql -c "CREATE DATABASE api_sd;" -U postgres`

cargar datos iniciales

`python3 manage.py loaddata brands.json`

`python3 manage.py loaddata producttags.json`

`python3 manage.py loaddata productos.json`

`python3 manage.py loaddata productdetail.json`

`python3 manage.py runserver`

El endpoint estará en localhost:8000/api/