#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <course_name>"
    echo "Example: $0 psicologia"
    exit 1
fi

COURSE_NAME=$1
YEARS="2016 2017 2018 2019 2020 2021 2022 2023 2024 2025"

echo "Starting Docker scraper for years 2016-2025 with course: $COURSE_NAME..."

docker run --rm scraper python main.py $COURSE_NAME $YEARS

echo "All years completed!"
