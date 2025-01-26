#!/bin/bash

export $(grep -v '^#' .env | xargs)
uvicorn --factory line_provider.app.main:setup_app --host ${UVICORN_LINE_HOST} --port ${UVICORN_LINE_PORT} --reload
