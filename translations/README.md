Localisation
============

The application is designed to be localised using *gettext*. Some helpers
have been added to make localisation as easy as possible.

Most localisation information is stored in the ``translations/`` directory.
To add a new language, simply call the shell script ``translations/add.sh``
with the code of the new language to add, e.g. ``translations/add.sh fr``.
The script will automatically create a subdirectory and generate a ``*.po``
file with all the strings that need to be translated.

Present translations will be automatically compiled into the application
using the usual build mechanism. To refresh the translations files when new
phrases have been added to the source code or templates, simply call
``npm run refresh:babel``. This will call pybabel and refresh all the
``*.po`` files as needed. To build the updated catalogs, run
``npm run build:babel``.

Translation of the JavaScript components is done using a simple gettext-like
function in ``js/l10n.js``. This file also contains an object with all the
phrases to be translated.
