# Development

If you would like to improve c3bottles, you are welcome to do so. Pull requests
are always welcome. Please have a look at the style and choices made so that
your code will fit in nicely.

A few things have been prepared to make development easier. The easiest way to
prepare your development environment is as follows:

    git clone https://github.com/c3bottles/c3bottles.git
    cd c3bottles
    make venv
    yarn
    yarn build

If you want to work on the Python code, a yarn task is available that starts
the development webserver and reloads it on every change made to the code.
Templates are not cached, so changes to templates are reflected as well:

    yarn watch:py

Please note that the development server might crash and not come back
automatically if you introduce an error that raises an unchecked exception.

To work on the JavaScript code, a similar task is available:

    yarn watch:js

Any changes to the JavaScript code in the `js/` directory will trigger a
rebuild of all static JavasScript. You then just have to refresh the website
in your browser to see your changes in action.

If you submit a pull request, it would be cool if you add some tests for your
new code on the Python side of things. Tests will be automatically run via
Travis CI, so please make sure that the existing tests do not fail and that
any additional ones succeed as well. The Python tests are available via make.
Just do the following before committing:

    make pytest
    make pycodestyle

JavaScript tests will be automatically run in the normal build process during
`yarn build:js`.
