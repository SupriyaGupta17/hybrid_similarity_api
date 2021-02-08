"""
    server_startup.py
    ~~~~~~
    Created By : Pankaj Suthar
"""
from resourceprovider import ResourceProvider

from src.api.similarity_api import BLUEPRINT_HYBRID_SIMILARITY_API
from src.exception.application_exception import ApplicationException
from src.util.response_util import ResponseUtil


def _register_blueprint(bp_name, prefix=None):
    app = ResourceProvider.get_resource("app")
    if prefix is None:
        prefix = "/api/"
    app.register_blueprint(bp_name, url_prefix=prefix)


def initialize_routes():
    """ Register Blueprints """
    _register_blueprint(BLUEPRINT_HYBRID_SIMILARITY_API)


def initialize_exception_handlers():
    """Initialize Exception handlers"""
    app = ResourceProvider.get_resource("app")

    @app.errorhandler(404)
    def handle_404_exception(error):
        """
        handle_404_exception
        :param error:  Standard flask error object
        :return:  Index.html Page to UI for serving 404 page
        """
        return ResponseUtil.response_with_error(404, "Resource Not Found")

    # Exception Handler
    @app.errorhandler(405)
    def handle_405_exception(error):
        '''
        handle_405_exception
        :param error:  Standard flask error object
        :return:  Method not Supported Error
        '''
        # Set Header of Response
        return ResponseUtil.response_with_error(405, "Method not supported")

    @app.errorhandler(ApplicationException)
    def handle_canary_api_exception(error):
        """
        handle_canary_api_exception
        :param error:  Standard flask error object
        :return:  Return Formatted Application Exception
        """
        response = ResponseUtil.response_with_error(error.status_code, error.message, error.dev_message)
        return response

    @app.errorhandler(500)
    def handle_canary_api_exception(error):
        """
        handle_canary_api_exception
        :param error:  Standard flask error object
        :return:  Return Formatted Application Exception
        """
        response = ResponseUtil.response_with_error(500, error.name, error.description)
        return response
