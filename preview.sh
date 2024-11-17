#!/bin/bash

cd app
uvicorn main:api --reload --log-level debug
