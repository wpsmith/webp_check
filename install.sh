#!/bin/bash

# Get Python.
PYTHON_REF=$(source ./check_python.sh)
if [[ "$PYTHON_REF" == "NoPython" ]]; then
    echo "Python3.6+ is not installed."
    exit
fi

# Install WP CLI
if ! command -v wp &> /dev/null
then
  curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
  chmod +x wp-cli.phar
  sudo mv wp-cli.phar /usr/local/bin/wp
else
  echo "WP CLI is already installed!"
fi

# Install python requirements
$PYTHON_REF -m pip install -r requirements.txt
$PYTHON_REF install.py
