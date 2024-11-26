import logging
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
# Configure the format for log messages
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a summary logger
summary_logger = logging.getLogger('summary_logger')
summary_logger.setLevel(logging.DEBUG)  # Use DEBUG to capture all log levels
summary_handler = logging.FileHandler(f'{dir_path}/../results/summary.log')
summary_handler.setLevel(logging.DEBUG)
summary_handler.setFormatter(log_format)
summary_logger.addHandler(summary_handler)  # Summary captures everything

# Create a logger for errors
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.DEBUG)
error_handler = logging.FileHandler(f'{dir_path}/../results/errors.log')
error_handler.setLevel(logging.DEBUG)
error_handler.setFormatter(log_format)
error_logger.addHandler(error_handler)
error_logger.addHandler(summary_handler)  # Errors also go to summary.log

# Create a logger for HTTP
http_logger = logging.getLogger('http_logger')
http_logger.setLevel(logging.DEBUG)
http_handler = logging.FileHandler(f'{dir_path}/../results/http.log')
http_handler.setLevel(logging.DEBUG)
http_handler.setFormatter(log_format)
http_logger.addHandler(http_handler)
http_logger.addHandler(summary_handler)  # HTTP logs also go to summary.log