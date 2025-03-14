#!/bin/bash


echo "Initial migration"

export FLASK_APP=create_app:create_app

flask db init
flask db migrate -m "init"
flask db upgrade

exec "$@"