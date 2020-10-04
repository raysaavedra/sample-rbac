#!/bin/sh

args=("$@")

if [ $# -eq 0 ]; then
    echo "No arguments provided. Running Dev"
    docker-compose up --build
fi


if [ ${args[0]}  == "dev" ]
then
    echo 'running dev'
    docker-compose up --build
elif [ ${args[0]}  == "staging" ]
then
    echo 'running staging'
    docker-compose up --build
elif [ ${args[0]}  == "prod" ]
then
    echo 'running prod'
    docker-compose up --build
else
    echo 'argument not found. Please use (dev/staging/prod)'
fi
