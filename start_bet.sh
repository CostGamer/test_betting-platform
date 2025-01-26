#!/bin/bash

export $(grep -v '^#' .env | xargs)
uvicorn --factory bet_maker.app.main:setup_app --host ${UVICORN_BET_HOST} --port ${UVICORN_BET_PORT} --reload