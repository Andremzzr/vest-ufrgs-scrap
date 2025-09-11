#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <course_name>"
    echo "Example: $0 psicologia"
    exit 1
fi

COURSE_NAME=$1

echo "Starting Docker scraper for years 2017-2025 with course: $COURSE_NAME..."

for year in 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025; do
    echo "Running scraper for year: $year"
    docker run --rm scraper python main.py $year $COURSE_NAME
    
    sleep 2
    
    echo "Completed year: $year, course: $COURSE_NAME"
    echo "---"
done

echo "All years completed!"