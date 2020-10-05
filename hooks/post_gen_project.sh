#!/bin/sh

echo '##############################'
echo 'Generating Poetry lock file...'
echo '##############################'

pip install "poetry=={{ cookiecutter.poetry_version }}"

poetry lock

echo '#########################################'
echo 'All done!'
echo "Don't forget to move your project folder!"
echo '#########################################'
