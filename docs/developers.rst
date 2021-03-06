.. _developers:

Developers
==========

Hello, developers! This will get you set up with a local WebPay server.
You can also :ref:`use a hosted <use-hosted>` WebPay server.

Install
~~~~~~~

You need Python 2.6, and MySQL, and a few NodeJS commands
like `less`_ for minifying JS/CSS.
Install system requirements with `homebrew`_ (Mac OS X)::

    brew tap homebrew/versions
    brew install python26 mysql swig nodejs

To develop locally you also need:

* An instance of the `Solitude`_ payment API running.
  If you run it with mock services (such as ``BANGO_MOCK=True``)
  then some things will still work.
  You can configure webpay with ``SOLITUDE_URL`` pointing at your
  localhost.
* Access to the zamboni db. For extra points this can be a read only slave.

Let's install webpay! Clone the source::

    git clone git://github.com/mozilla/webpay.git

Install all Python dependencies. You probably want to do this
within a `virtualenv`_. If you use `virtualenvwrapper`_ (recommended)
set yourself up with::

    mkvirtualenv --python=python2.6 webpay

Install with::

    pip install --no-deps -r requirements/dev.txt

Create a database to work in::

    mysql -u root -e 'create database webpay'

Install compressor scripts with `npm`_ for node.js.
You'll probably want to install them globally
in your common node modules, like this::

    npm install -g less clean-css uglify-js

Make sure you see a valid path when you type::

    which lessc
    which cleancss
    which uglifyjs

Make yourself a local settings file::

    cp webpay/settings/local.py-dist webpay/settings/local.py

Edit that file and fill in your database credentials.
Be sure to also set this so you can see errors::

    VERBOSE_LOGGING = True

Sync up your database by running all the migrations::

    schematic ./migrations

Now you should be ready to run the test suite::

    python manage.py test

If they all pass then fire up a development server::

    python manage.py runserver 0.0.0.0:8000

Try it out at http://localhost:8000/mozpay/ .
If you see a form error about a missing JWT then
you are successfully up and running.

If you can't log in with Persona
check the value of ``SITE_URL`` in your local
settings. It must match the
URL bar of how you run your dev server exactly.

See :ref:`this section <use-hosted>` for how to set up a B2G device to
talk to your brand new local development server.

Building the Docs
~~~~~~~~~~~~~~~~~

To build these very docs that you are reading while developing locally,
do this from your webpay root::

    make -C docs/ html

Then open ``docs/_build/html/index.html`` in a browser.

Working on the UI
~~~~~~~~~~~~~~~~~

The webpay server has a very minimal UI. It lets you log in and
create/enter/reset a PIN but after that it redirects you to a
payment processor. You can work on the login and PIN by setting this
in your ``webpay/settings/local.py``::

    TEST_PIN_UI = True

Then load the front page: http://localhost:8000/mozpay/

Using JWTs for development
~~~~~~~~~~~~~~~~~~~~~~~~~~

Each payment begins with a JWT (Json Web Token) so you'll need to
start with a JWT if you want to see the complete payment flow.
The best way to get a valid JWT is to make a real
purchase using your local Marketplace or any app
that has a valid in-app payment key.
When you start a purchase from B2G check your B2G console. In stdout you
should see a link that you can copy and paste into a browser to use better dev
tools. Here is an example of what that looks like::

    http://localhost:8000/mozpay/?req=eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJhdWQiOiAibG9jYWxob3N0IiwgImlzcyI6ICJtYXJrZXRwbGFjZSIsICJyZXF1ZXN0IjogeyJwcmljZSI6IFt7ImN1cnJlbmN5IjogIlVTRCIsICJhbW91bnQiOiAiMC45OSJ9XSwgIm5hbWUiOiAiTXkgYmFuZHMgbGF0ZXN0IGFsYnVtIiwgInByb2R1Y3RkYXRhIjogIm15X3Byb2R1Y3RfaWQ9MTIzNCIsICJkZXNjcmlwdGlvbiI6ICIzMjBrYnBzIE1QMyBkb3dubG9hZCwgRFJNIGZyZWUhIn0sICJleHAiOiAxMzUwOTQ3MjE3LCAiaWF0IjogMTM1MDk0MzYxNywgInR5cCI6ICJtb3ppbGxhL3BheW1lbnRzL3BheS92MSJ9.ZW-Y9-UroJk7-ZpDjebUU-uYOx4h7TfztO7JBi2d5z4

.. _WebPaymentProvider: https://wiki.mozilla.org/WebAPI/WebPaymentProvider
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _`nightly desktop B2G build`: http://ftp.mozilla.org/pub/mozilla.org/b2g/nightly/latest-mozilla-b2g18/
.. _`Gaia Hacking`: https://wiki.mozilla.org/Gaia/Hacking
.. _homebrew: http://mxcl.github.com/homebrew/
.. _virtualenvwrapper: http://pypi.python.org/pypi/virtualenvwrapper
.. _less: http://lesscss.org/
.. _npm: https://npmjs.org/
.. _`nightly B2G desktop`: http://ftp.mozilla.org/pub/mozilla.org/b2g/nightly/latest-mozilla-central/
.. _`Solitude`: https://solitude.readthedocs.org/en/latest/index.html
.. _`Android Developer Tools`: http://developer.android.com/sdk/index.html
.. _git: http://git-scm.com/
.. _`navigator.mozPay()`: https://wiki.mozilla.org/WebAPI/WebPayment
.. _`Zamboni`: https://github.com/mozilla/zamboni
