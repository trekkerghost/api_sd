# API CRUD Challenge for SD

[![Build Status](https://travis-ci.org/trekkerghost/api_sd.svg?branch=master)](https://travis-ci.org/trekkerghost/api_sd)

[![Coverage Status](https://coveralls.io/repos/github/trekkerghost/api_sd/badge.svg?branch=master)](https://coveralls.io/github/trekkerghost/api_sd?branch=master)

Creación de API usando Python y Django

## Uso


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

