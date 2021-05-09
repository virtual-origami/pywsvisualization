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


class WSRobot:

    def __init__(self, id, color, base, joint_width, base_width, scaling, base_shoulder_width,
                 shoulder_elbow_width, elbow_wrist_width):
        """
        Initialization of Visualization for robots in workspace

        :param id: robot id
        :param color: robot color
        :param base: robot base coordinates
        :param joint_width: robot joints (shoulder, elbow, wrist) radius
        :param base_width: robot base radius
        :param scaling: image scaling
        :param base_shoulder_width: width of base-shoulder line segment
        :param shoulder_elbow_width: width of shoulder-elbow line segment
        :param elbow_wrist_width: width of elbow-wrist line segment
        """
        self.id = id
        self.scaling = scaling
        self.color = color
        self.base = base
        self.shoulder = base
        self.elbow = base
        self.wrist = base
        self.joint_width = joint_width
        self.base_width = base_width
        self.base_shoulder_width = base_shoulder_width
        self.shoulder_elbow_width = shoulder_elbow_width
        self.elbow_wrist_width = elbow_wrist_width

    def draw(self, screen):
        """
        Draw Robot Visualization
        :param screen: rendering screen object from pygame
        :return: None
        """
        pg.draw.line(surface=screen, color=self.color, start_pos=self.scale(self.base),
                     end_pos=self.scale(self.shoulder), width=self.base_shoulder_width)
        pg.draw.line(surface=screen, color=self.color, start_pos=self.scale(self.shoulder),
                     end_pos=self.scale(self.elbow), width=self.shoulder_elbow_width)
        pg.draw.line(surface=screen, color=self.color, start_pos=self.scale(self.elbow), end_pos=self.scale(self.wrist),
                     width=self.elbow_wrist_width)
        pg.draw.circle(surface=screen, color=self.color, center=self.scale(self.base), radius=self.base_width)
        pg.draw.circle(surface=screen, color=self.color, center=self.scale(self.shoulder), radius=self.joint_width)
        pg.draw.circle(surface=screen, color=(255, 255, 255), center=self.scale(self.shoulder),
                       radius=self.joint_width / 2)

        pg.draw.circle(surface=screen, color=self.color, center=self.scale(self.elbow), radius=self.joint_width)
        pg.draw.circle(surface=screen, color=(255, 255, 255), center=self.scale(self.elbow),
                       radius=self.joint_width / 2)

        pg.draw.circle(surface=screen, color=self.color, center=self.scale(self.wrist), radius=self.joint_width)
        pg.draw.circle(surface=screen, color=(255, 255, 255), center=self.scale(self.wrist),
                       radius=self.joint_width / 2)

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


class WSRobots:
    def __init__(self, config, screen):
        """
        Intialization of all robots in workspace
        :param config: configuration file path
        :param screen: pygame screen object
        """
        try:
            self.screen = screen
            self.robots = []
            assert self.screen is not None, "Screen does not exists"
            for robot in config:
                self.robots.append(WSRobot(id=robot["id"],
                                           color=(robot["render"]["color"][0], robot["render"]["color"][1],
                                                  robot["render"]["color"][2]),
                                           base=[0, 0],
                                           joint_width=robot["render"]["joint_width"],
                                           base_width=robot["render"]["base_width"],
                                           scaling=robot["attributes"]["scaling"],
                                           base_shoulder_width=robot["render"]["base_shoulder"],
                                           shoulder_elbow_width=robot["render"]["shoulder_elbow"],
                                           elbow_wrist_width=robot["render"]["shoulder_elbow"]
                                           ))
            for robot in self.robots:
                robot.draw(screen=screen)
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
        for robot in self.robots:
            robot.draw(screen=self.screen)
        return None

    def update(self, id, base=None, shoulder=None, elbow=None, wrist=None):
        """
        Visualization of shoulder-elbow line segmentation Update method for all robots in workspace
        :param id: robot id
        :param base: base coordinates of the robot
        :param shoulder: shoulder coordinate of the robot
        :param elbow: elbow coordinate of the robot
        :param wrist: wrist coordinate of the robot
        :return: None
        """
        for robot in self.robots:
            if robot.id == id:
                if shoulder is not None:
                    robot.shoulder = shoulder
                if elbow is not None:
                    robot.elbow = elbow
                if base is not None:
                    robot.base = base
                if wrist is not None:
                    robot.wrist = wrist
        return None