import argparse
import asyncio
import logging
import signal
import functools
import os
import sys
import traceback
import pygame as pg
import yaml
from WSGui.WS import WS

logging.basicConfig(level=logging.WARNING, format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')

# logger for this file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/tmp/virtualwsgui.log')
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)-8s-[%(filename)s:%(lineno)d]-%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# TURN OFF asyncio logger
asyncio_logger = logging.getLogger('asyncio')
asyncio_logger.setLevel(logging.WARNING)

is_sighup_received = False


def parse_arguments():
    """Arguments to run the script"""
    parser = argparse.ArgumentParser(description='Walk Generator')
    parser.add_argument('--config', '-c', required=True, help='YAML Configuration File for Walk Generator with path')
    return parser.parse_args()


def signal_handler(name):
    global is_sighup_received
    is_sighup_received = True


def gui_event_handler():
    """
    GUI event handler
    :return:
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()


class WSApp:
    """
    Workspace Application
    """

    def __init__(self, config_file, event_loop):
        """
        Initialization of Workspace application
        :param config_file: configuration file name
        :param event_loop: event loop
        """
        try:
            pg.init()
            if os.path.exists(config_file):
                with open(config_file, 'r') as yaml_file:
                    yaml_as_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)
                    scene = yaml_as_dict["scene"]
                    assert scene is not None, "Workspace configuration does not exists"
                    assert event_loop is not None, "Event loop can't be none"
                    self.workspaces = []
                    for workspace in scene["workspaces"]:
                        self.workspaces.append(WS(workspace=workspace, eventloop=event_loop))
            else:
                raise AssertionError("Configuration does not exists")
        except FileNotFoundError as e:
            logging.critical(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.critical(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            sys.exit()
        except OSError as e:
            logging.critical(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.critical(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            sys.exit()
        except AssertionError as e:
            logging.critical(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.critical(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            sys.exit()
        except yaml.YAMLError as e:
            logging.critical(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.critical(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            sys.exit()
        except Exception as e:
            logging.critical(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.critical(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            sys.exit()

    async def connect(self):
        """
        Connect AMQP Publisher and Subscriber
        :return:
        """
        try:
            for workspace in self.workspaces:
                await workspace.connect()
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

    async def visualization_loop(self):
        """
        vistualization loop
        :return:
        """
        try:
            gui_event_handler()
            for workspace in self.workspaces:
                workspace.draw()
            pg.display.update()
            await asyncio.sleep(0)
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


async def app(eventloop, config):
    """
    Main Application
    :param eventloop: event loop for publisher and subscriber
    :return: None
    """
    try:
        global is_sighup_received

        while True:
            factory = WSApp(config_file=config, event_loop=eventloop)
            await factory.connect()

            # continuously monitor signal handle and update walker
            while not is_sighup_received:
                await factory.visualization_loop()

            # If SIGHUP Occurs, Delete the instances
            del factory

            # reset sighup handler flag
            is_sighup_received = False

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


def read_config(yaml_file, rootkey):
    """Parse the given Configuration File"""
    if os.path.exists(yaml_file):
        with open(yaml_file, 'r') as config_file:
            yaml_as_dict = yaml.load(config_file, Loader=yaml.FullLoader)
        return yaml_as_dict[rootkey]
    else:
        raise FileNotFoundError
        logger.error('YAML Configuration File not Found.')


def main():
    """Initialization"""
    args = parse_arguments()
    if not os.path.isfile(args.config):
        logger.error("configuration file not readable. Check path to configuration file")
        sys.exit(-1)

    event_loop = asyncio.get_event_loop()
    event_loop.add_signal_handler(signal.SIGHUP, functools.partial(signal_handler, name='SIGHUP'))
    event_loop.run_until_complete(app(event_loop, args.config))


if __name__ == "__main__":
    main()
