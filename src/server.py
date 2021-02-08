"""
    server.py
    ~~~~~~
    Main Server File
    Created By : Pankaj Suthar
"""
# Imports
import flask
from flask_cors import CORS
from inoutlogger.utils import InOutLogger, Logger
from resourceprovider import ResourceProvider
from sentence_transformers import SentenceTransformer
from src.util.logger import ApplicationLogger
from src.util.request_interceptor import intercept_request
from src.util.response_interceptor import intercept_response
from src.util.server_startup import initialize_exception_handlers
from src.util.server_startup import initialize_routes
import nltk
nltk.download("stopwords")
nltk.download('wordnet')
nltk.download('punkt')

# Application Config
APPLICATION_NAME = "HybridSimilarityAPIs"
APPLICATION_VERSION = "1.0.0"
APPLICATION_LOGS_DIR = "logs"
APPLICATION_LOG_BACKUP_COUNT = 10

# Initialize App
app = flask.Flask(__name__)

# App Configuration
CORS(app)

# Set Logger
_logger = ApplicationLogger(logs_dir=APPLICATION_LOGS_DIR,
                            logs_backup_count=APPLICATION_LOG_BACKUP_COUNT)
application_logger = _logger.get_logger

# Set Method In Out Logger
InOutLogger(Logger(log_handler=application_logger, name="ApplicationLogger"))

# BERT Model Initialize
model = SentenceTransformer('bert-base-nli-mean-tokens')
# Initialize Application Resource
ResourceProvider(app=app,
                 app_name=APPLICATION_NAME,
                 app_version=APPLICATION_VERSION,
                 logger=application_logger,
                 model=model
                 )
application_logger.info("Build Resource provider")

# Initialize routes
application_logger.info("Initializing all Endpoints")
initialize_routes()

# Initialize Exception Handlers
application_logger.info("Initializing all Exception Handler")
initialize_exception_handlers()

# Initialize Cache
application_logger.info("Initializing Caches")

# Interceptors
application_logger.info("Initializing Request Interceptor")


@app.before_request
def request_interceptor():
    intercept_request(flask.request)


application_logger.info("Initializing Response Interceptor")


@app.after_request
def response_interceptor(response):
    return intercept_response(response)


# Index Page
@app.route('/')
def index():
    """Index Page"""
    return "<h1 style='color:black'>Hybrid Similarity APIs - Version {}</h1>".format(APPLICATION_VERSION)


application_logger.info("Server Setup Completed.... Starting Server")
