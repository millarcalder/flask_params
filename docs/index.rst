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

   from flask_parameters import Flask

   app = Flask(__name__)


   @app.route("/foo")
   def foo(arg, kwarg = 123) -> dict:
      return {"arg": arg, "kwarg": kwarg}


   @app.route("/strict_foo")
   def strict_foo(arg: str, kwarg: int = 123) -> dict:
      return {"arg": arg, "kwarg": kwarg}
