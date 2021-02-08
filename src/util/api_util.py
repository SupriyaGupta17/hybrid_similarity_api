"""
    api_util.py
    ~~~~~~
    Created By : Pankaj Suthar
"""
from resourceprovider import ResourceProvider

from src.exception.application_exception import ApplicationException


class APIUtil:
    """API Util is utility to verify basic request parameters"""

    @staticmethod
    def is_content_type_application_json(request):
        """Verify Content-Type in request. It should be application/json"""
        # Logger
        logger = ResourceProvider.get_resource("logger")
        is_verify, header = True, None
        try:
            header = request.content_type
            if header != 'application/json':
                if header != 'application/json; charset=UTF-8':
                    is_verify = False
        except Exception as ex:
            logger.error("Unable to Verify Content-Type. EXCEPTION [{}]".format(ex))

        if not is_verify:
            logger.error(
                "Invalid Content-Type header. Found = [ {} ], required [ application/json ]".format(
                    header))
            raise ApplicationException(message="Required Header [ application/json ]", status_code=400)
        else:
            logger.info("Content-Type Verified.")
