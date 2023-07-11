import logging
from config import LOGLEVEL

logger = logging.getLogger()
logging.basicConfig(format='%(levelname)s: %(message)s', level=LOGLEVEL)
