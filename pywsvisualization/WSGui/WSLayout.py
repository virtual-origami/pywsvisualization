import sys
import traceback
import pygame as pg
import logging

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
            self.scaling = config["attributes"]["scaling"]
            self.screen = screen
            self.color = (config["render"]["color"][0],config["render"]["color"][1],config["render"]["color"][2])
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
            self.screen.fill(self.color)
            for obstacle in self.obstacles:
                if obstacle["render"]["shape"] == "line" and len(obstacle["points"]) == 2:
                    startpos = (self.scale(obstacle["points"][0][0]),self.scale(obstacle["points"][0][1]))
                    endpos = (self.scale(obstacle["points"][1][0]),self.scale(obstacle["points"][1][1]))
                    pg.draw.line(surface=self.screen,color=(obstacle["render"]["color"][0],obstacle["render"]["color"][1],obstacle["render"]["color"][2]),start_pos=startpos,end_pos=endpos)
                elif obstacle["render"]["shape"] == "polygon" and len(obstacle["points"]) > 2:
                    points = list()
                    for pt in obstacle["points"]:
                        points.append([self.scale(pt[0]),self.scale(pt[1])])
                    pg.draw.polygon(surface=self.screen,
                                    color=(obstacle["render"]["color"][0],obstacle["render"]["color"][1],obstacle["render"]["color"][2]),
                                    points=points)
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

    def scale(self, value):
        """
        Coordinate scaling
        :param value: coordinate value
        :return: scaled coordinates
        """
        try:
            if (type(value) is int) or (type(value) is float):
                return value * self.scaling
            elif type(value) is list:
                return [v * self.scaling for v in value]
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
