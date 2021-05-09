import logging
import json
import sys
import traceback

import pygame as pg
from pywsvisualization.pub_sub.AMQPubSub import PubSubAMQP
from .WSLayout import WSLayout
from .WSParticle import WSParticles
from .WSRobot import WSRobots

# logger for this file
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
handler = logging.FileHandler('/tmp/virtualwsgui.log')
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)-8s-[%(filename)s:%(lineno)d]-%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class WS:
    def __init__(self, workspace, eventloop):
        """
        Initialization of workspace
        :param workspace: workspace configuration file
        :param eventloop: eventloop for Pub-sub
        """
        try:
            self.id = workspace["id"]
            self.scaling = workspace["attributes"]["scaling"]
            self.dimensions = [workspace["render"]["dimensions"][0] * self.scaling,
                               workspace["render"]["dimensions"][1] * self.scaling]
            self.color = (workspace["render"]["color"][0], workspace["render"]["color"][1], workspace["render"]["color"][2])
            self.type = workspace["render"]["type"]
            self.interval = workspace["attributes"]["interval"]
            self.screen = pg.display.set_mode(self.dimensions)
            self.layout = WSLayout(config=workspace, screen=self.screen)
            self.particles = WSParticles(config=workspace["particles"], screen=self.screen)
            self.robots = WSRobots(config=workspace["robots"], screen=self.screen)
            self.event_loop = eventloop
            self.subscribers = []
            for pub_sub_config in workspace["protocol"]:
                self.subscribers.append(PubSubAMQP(eventloop=self.event_loop,
                                                   config_file=pub_sub_config,
                                                   binding_suffix=self.id,
                                                   app_callback=self._subscriber_callback))
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

    def _subscriber_callback(self, **kwargs):
        """
        Subscriber callback
        :param kwargs: keywork argument of the parameter passed
        :return: None
        """
        try:
            self.consume_telemetry_msgs(kwargs["exchange_name"], kwargs["binding_name"],
                                        json.loads(kwargs["message_body"]))
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

    def draw(self):
        """
        Draw workspace
        1. Layout
        2. robot
        3. particle
        :return: None
        """
        try:
            self.layout.draw()
            self.robots.draw()
            self.particles.draw()
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

    def consume_telemetry_msgs(self, exchange_name, binding_name, message_body):
        """
        Consume telemetry messages from the Subscriber
        :param exchange_name: Exchange name
        :param binding_name: Binding name
        :param message_body: message body
        :return: None
        """
        try:
            if "telemetry.robot" in binding_name:
                # extract robot id
                binding_delimited_array = binding_name.split(".")
                robot_id = binding_delimited_array[len(binding_delimited_array) - 1]
                msg_attributes = message_body.keys()
                if ("id" in msg_attributes) and \
                        ("shoulder" in msg_attributes) and \
                        ("elbow" in msg_attributes) and \
                        ("wrist" in msg_attributes) and \
                        ("base" in msg_attributes):
                    if robot_id == message_body["id"]:
                        logger.debug(message_body)
                        base = [message_body["base"][0], message_body["base"][1]]
                        shoulder = [message_body["shoulder"][0], message_body["shoulder"][1]]
                        elbow = [message_body["elbow"][0], message_body["elbow"][1]]
                        wrist = [message_body["wrist"][0], message_body["wrist"][1]]
                        self.robots.update(id=robot_id,
                                           base=base,
                                           shoulder=shoulder,
                                           elbow=elbow,
                                           wrist=wrist)
                    else:
                        return False  # robot id in binding name and message body does not match
                else:
                    return False  # invalid message body format
            elif "telemetry.pls" in binding_name:
                # extract walker id
                binding_delimited_array = binding_name.split(".")
                walker_id = binding_delimited_array[len(binding_delimited_array) - 1]
                msg_attributes = message_body.keys()
                if ("id" in msg_attributes) and \
                        ("x_ref_pos" in msg_attributes) and \
                        ("y_ref_pos" in msg_attributes) and \
                        ("z_ref_pos" in msg_attributes) and \
                        ("x_uwb_pos" in msg_attributes) and \
                        ("y_uwb_pos" in msg_attributes) and \
                        ("z_uwb_pos" in msg_attributes) and \
                        ("x_ref_pos" in msg_attributes) and \
                        ("y_ref_pos" in msg_attributes) and \
                        ("z_ref_pos" in msg_attributes) and \
                        ("timestamp" in msg_attributes):
                    if walker_id == message_body["id"]:
                        logger.debug(message_body)
                        ref_position = [message_body["x_ref_pos"], message_body["y_ref_pos"]]
                        uwb_position = [message_body["x_uwb_pos"], message_body["y_uwb_pos"]]
                        est_position = [message_body["x_est_pos"], message_body["y_est_pos"]]
                        self.particles.update(id=walker_id,
                                              ref_position=ref_position,
                                              uwb_position=uwb_position,
                                              est_position=est_position,
                                              radius=5,
                                              world=message_body["view"],
                                              ref_heading=message_body['ref_heading'])
                    else:
                        return False  # robot id in binding name and message body does not match
                else:
                    return False  # invalid message body format
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

    async def connect(self):
        """
        Connect AMQP Publisher and subscriber
        :return: None
        """
        try:
            for subscriber in self.subscribers:
                await subscriber.connect(mode="subscriber")
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
