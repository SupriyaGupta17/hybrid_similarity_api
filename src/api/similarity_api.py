"""
    similarity_api.py
    ~~~~~~~~~~~
    Created By : Pankaj Suthar
"""
import flask
from flask import Blueprint, request
from resourceprovider import ResourceProvider

from src.exception.application_exception import ApplicationException
from src.service.hybrid_similarity_calculator_service import HybridSimilarityCalculatorService
from src.util.api_util import APIUtil
from src.util.response_util import ResponseUtil

BLUEPRINT_HYBRID_SIMILARITY_API = Blueprint(
    'similarity_api', __name__)


class HybridSimilarityAPI:
    """Hybrid Similarity API Endpoint"""

    @staticmethod
    @BLUEPRINT_HYBRID_SIMILARITY_API.route("/hybrid-similarity", methods=["POST"])
    def get_hybrid_similarity() -> object:
        """ Get Hybrid Similarity of Two Sentence"""
        # Get Logger
        logger = ResourceProvider.get_resource("logger")

        # Log
        logger.info(
            "Received [GET Hybrid Similarity] request to [{}]".format(
                HybridSimilarityAPI.get_hybrid_similarity.__qualname__))

        # Verify Content Type
        APIUtil.is_content_type_application_json(request)

        # Get Request Body
        try:
            content = flask.request.get_json()
            sentence_1 = content["firstSentence"]
            sentence_2 = content["secondSentence"]
            option = content["option"]
            logger.info("Content is [{}]".format(str(content)))
        except Exception as ex:
            logger.exception(
                "Invalid Request body for hybrid similarity api endpoint. EXCEPTION: {}".format(
                    str(ex)))
            raise ApplicationException(message="Invalid Request Body", status_code=400)

        # Fetch Response
        response = HybridSimilarityCalculatorService().calculate_similarity(
            f_sentence=sentence_1,
            s_sentence=sentence_2,
            option=option
        )

        # Format Response
        response_payload = ResponseUtil.response_with_success(response)
        return response_payload
