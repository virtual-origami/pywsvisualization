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
from pywsvisualization.WSGui import WS, set_scaling_factor


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
maps = []


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


async def app(eventloop, config):
    """
    Main Application
    :param eventloop: event loop for publisher and subscriber
    :return: None
    """
    try:
        global is_sighup_received
        global maps

        while True:
            scene_config = read_config(yaml_file=config, rootkey="scene")
            set_scaling_factor(config=scene_config)
            loop_interval = scene_config["attributes"]["interval"]
            pg.init()
            maps = []
            for mape in scene_config["maps"]:
                maps.append(WS(workspace=mape, eventloop=eventloop))

            for workspace in maps:
                await workspace.connect()

            # continuously monitor signal handle and update walker
            while not is_sighup_received:
                gui_event_handler()
                for workspace in maps:
                    workspace.draw()
                pg.display.update()
                await asyncio.sleep(loop_interval)

            # If SIGHUP Occurs, Delete the instances
            del maps

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
