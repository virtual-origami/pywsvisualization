import sys
import traceback
import pygame as pg
import logging
from .scaling import scale

# logger for this file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/tmp/virtualwsgui.log')
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)-8s-[%(filename)s:%(lineno)d]-%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class WSLayout:
    def __init__(self,config,screen):
        """
        Initialization of workspace layout
        :param config: configuration file
        :param screen: screen object from pygame
        """
        try:
            self.screen = screen
            self.bg_color = tuple(config["render"]["background_color"])
            self.obstacles = config["obstacles"]
        except AssertionError as e:
            logging.critical(e)
            exc_type,exc_value,exc_traceback = sys.exc_info()
            logging.critical(repr(traceback.format_exception(exc_type,exc_value,exc_traceback)))
            sys.exit()
        except Exception as e:
            logging.critical(e)
            exc_type,exc_value,exc_traceback = sys.exc_info()
            logging.critical(repr(traceback.format_exception(exc_type,exc_value,exc_traceback)))
            sys.exit()

    def draw(self):
        """
        Draw Layout in the workspace.
        Drawing is based on the shape of the obstacles
        1. line
        2. polygon
        :return: None
        """
        try:
            self.screen.fill(self.bg_color)
            for obstacle in self.obstacles:
                if obstacle["render"]["shape"] == "line" and len(obstacle["points"]) == 2:
                    startpos = (scale(obstacle["points"][0][0]),scale(obstacle["points"][0][1]))
                    endpos = (scale(obstacle["points"][1][0]),scale(obstacle["points"][1][1]))
                    width = obstacle["width"]
                    pg.draw.line(surface=self.screen,color=(obstacle["render"]["color"][0],obstacle["render"]["color"][1],obstacle["render"]["color"][2]),start_pos=startpos,end_pos=endpos, width=width)
                elif obstacle["render"]["shape"] == "polygon" and len(obstacle["points"]) > 2:
                    points = list()
                    for pt in obstacle["points"]:
                        points.append([scale(pt[0]),scale(pt[1])])
                    width = obstacle["width"]
                    pg.draw.polygon(surface=self.screen,
                                    color=(obstacle["render"]["color"][0],obstacle["render"]["color"][1],obstacle["render"]["color"][2]),
                                    points=points, width=width)
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

