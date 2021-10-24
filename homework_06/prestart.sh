#!/usr/bin/env sh

#echo "Create migrations"
#flask db migrate

echo "Run migrations"
flask db upgrade