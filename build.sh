#!/usr/bin/env bash
# Exit immediately if any command fails
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files (CSS, JS, images)
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

sudo apt-get update
sudo apt-get install -y libpango-1.0-0 libharfbuzz-dev libcairo2-dev