#!/bin/bash
set -e

psql -U "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE "{{cookiecutter.project_name}}";
EOSQL
