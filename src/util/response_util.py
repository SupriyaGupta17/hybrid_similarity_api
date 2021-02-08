"""
    response_util.py
    ~~~~~~
    Response Formatter
"""

import flask
from resourceprovider import ResourceProvider


class ResponseUtil:
    """Response Utility to format response """

    @staticmethod
    def response_with_success(payload, http_code=None, message="success", dev_message=None):
        """ Response With Success"""
        logger = ResourceProvider.get_resource("logger")

        if not http_code:
            http_code = 200

        response = flask.jsonify(
            {
                'status': "success",
                'httpCode': http_code,
                'result': payload
            }
        )

        response.status_code = http_code
        logger.info("Logging Response- [{}]".format(response))
        return response

    @staticmethod
    def response_with_error(http_code, message, dev_message=None):
        """Response With error"""
        logger = ResourceProvider.get_resource("logger")

        if not http_code:
            http_code = 400

        response = flask.jsonify({
            'status': "failed",
            'httpCode': http_code,
            'message': message
        })
        response.status_code = http_code
        logger.info("Logging Response- [{}]".format(response))
        return response
