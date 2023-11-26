# Development

If you would like to improve c3bottles, you are welcome to do so. Pull requests
are always welcome. Please have a look at the style and choices made so that
your code will fit in nicely.

A few things have been prepared to make development easier. The easiest way to
prepare your development environment is as follows:

    git clone https://github.com/c3bottles/c3bottles.git
    cd c3bottles
    make venv
    pnpm
    pnpm build

If you want to work on the Python code, a pnpm task is available that starts
the development webserver and reloads it on every change made to the code.
Templates are not cached, so changes to templates are reflected as well:

    pnpm watch:py

Please note that the development server might crash and not come back
automatically if you introduce an error that raises an unchecked exception.

To work on the JavaScript code, a similar task is available:

    pnpm watch:js

Any changes to the JavaScript code in the `js/` directory will trigger a
rebuild of all static JavasScript. You then just have to refresh the website
in your browser to see your changes in action.

If you submit a pull request, it would be cool if you add some tests for your
new code on the Python side of things. Tests will be automatically run via
Travis CI, so please make sure that the existing tests do not fail and that
any additional ones succeed as well. The Python tests are available via make.
Just do the following before committing:

    make pytest

Since arguing about how code should be formatted only wastes time, we let
[black](https://github.com/psf/black) do that for us. In addition, we let
isort sort and format nicely all our imports at the start of the files.
Just run

    make format

before committing your changes. If black or isort finds anything to change on
your code, the CI build will fail.

isort, black, flake8 and pytest are added as a git pre-commit hook using husky
as well.

JavaScript tests will be automatically run in the normal build process during
`pnpm build:js`.
