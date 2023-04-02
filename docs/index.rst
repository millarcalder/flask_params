Flask Parameters
================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


=============
API Reference
=============

.. autosummary::
   :toctree: api_reference

   flask_parameters.inject_query_params
   flask_parameters.inject_and_validate_query_params
   flask_parameters.exceptions.ArgsException
   flask_parameters.exceptions.TypeCheckException
   flask_parameters.exceptions.register_error_handlers


=============
Example Usage
=============

.. code-block::

   import flask

   from flask_parameters import inject_query_params
   from flask_parameters import inject_and_validate_query_params
   from flask_parameters import register_error_handlers

   app = flask.Flask(__name__)
   register_error_handlers(app)


   @app.route("/foo")
   @inject_query_params()
   def foo(arg, kwarg = 123) -> dict:
      return {"arg": arg, "kwarg": kwarg}


   @app.route("/strict_foo")
   @inject_and_validate_query_params()
   def strict_foo(arg: str, kwarg: int = 123) -> dict:
      return {"arg": arg, "kwarg": kwarg}
