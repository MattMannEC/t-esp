import logging

# Configure the logging system to include file name and line number of where the log occurred
class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.filename = record.pathname.split('/')[-1]
        record.lineno = record.lineno
        return super().format(record)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

for handler in logging.root.handlers:
    handler.setFormatter(CustomFormatter(handler.formatter._fmt))

# Create a logger
logger = logging.getLogger(__name__)