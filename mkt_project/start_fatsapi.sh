#!/bin/bash

# Переход в директорию, где находится ваш проект
cd /team_spirit/mkt_project

source /team_spirit/mkt_project/venv/bin/activate

# Запуск Uvicorn с указанием пути к приложению
uvicorn uber.main_uber:app --host 0.0.0.0 --port 8000 --reload
