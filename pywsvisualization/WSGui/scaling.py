import logging
import sys
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/tmp/virtualwsgui.log')
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)-8s-[%(filename)s:%(lineno)d]-%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

scaling_factor = 1


def set_scaling_factor(config):
    global scaling_factor
    scaling_factor = config["attributes"]["scaling"]

def get_scaling_factor():
    global scaling_factor
    return scaling_factor

def scale(value):
    """
    Coordinate scaling
    :param value: coordinate value
    :return: scaled coordinates
    """
    global scaling_factor
    try:
        if (type(value) is int) or (type(value) is float):
            return value * scaling_factor
        elif type(value) is list:
            return [v * scaling_factor for v in value]
        else:
            raise AssertionError(f"Type {type(value)} is not scalable")
    except AssertionError as e:
        logging.critical(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.critical(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        sys.exit()
    except Exception as e:
        logging.critical(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.critical(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        sys.exit()
