#!/bin/sh

# Generates the directories and files needed to translate the application
# into a new language. There are no sanity checks, so use with care.

cd `dirname $0`

pybabel extract -F babel.cfg -o messages.pot ..
pybabel init -i messages.pot -d . -l $1

[ $? -eq 0 ] || exit 1

echo "\nPlease add your new language to 'controller/__init__.py' and add"
echo "the translated phrases to 'translations/$1/LC_MESSAGES/messages.po."
echo "When you are done, run 'npm build:babel' to recompile.\n"
