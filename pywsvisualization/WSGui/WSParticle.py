import random
import sys
import traceback
import pygame as pg
import logging, math, random
from .scaling import scale

# logger for this file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/tmp/virtualwsgui.log')
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)-8s-[%(filename)s:%(lineno)d]-%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class WSParticle:
    def __init__(self, id, ref_pos_color, uwb_pos_color, est_pos_color, ray_cast_color, center, radius):
        """
        Initialization of Particle (personnel as a point object)
        :param id: personnel ID
        :param ref_pos_color: reference true position color
        :param uwb_pos_color: uwb position color
        :param est_pos_color: estimated position color
        :param ray_cast_color: ray cast ray's colour
        :param center: center coordinates of the particle
        :param radius: radius of the particle
        """
        self.id = id
        self.ref_pos_color = ref_pos_color
        self.uwb_pos_color = uwb_pos_color
        self.est_pos_color = est_pos_color
        self.ray_cast_color = ray_cast_color
        self.ref_center = center
        self.uwb_center = center
        self.est_center = center
        self.radius = radius
        self.world_view = None
        self.ref_heading = None

    def draw(self, screen):
        """
        Draw visualization of particle
        :param screen: screen object from pygame
        :return: None
        """
        try:
            if self.ref_center is not None and self.uwb_center is not None and self.est_center is not None:
                if self.world_view is not None:
                    for ray in self.world_view:
                        pg.draw.line(surface=screen, color=self.ray_cast_color, start_pos=scale(self.ref_center),
                                     end_pos=scale(ray["contact_point"]), width=1)
                pg.draw.circle(surface=screen,
                               color=self.uwb_pos_color,
                               center=scale(self.uwb_center),
                               radius=self.radius)
                pg.draw.circle(surface=screen,
                               color=self.ref_pos_color,
                               center=scale(self.ref_center),
                               radius=self.radius)
                pg.draw.circle(surface=screen,
                               color=self.est_pos_color,
                               center=scale(self.est_center),
                               radius=self.radius)

                if self.ref_heading is not None:
                    num = scale(self.ref_heading['end'])[1] - scale(self.ref_heading['start'])[1]
                    dem = scale(self.ref_heading['end'])[0] - scale(self.ref_heading['start'])[0]
                    m = math.atan2(num, dem)
                    end_pos_x = self.ref_center[0] + (math.cos(m) * 2)
                    end_pos_y = self.ref_center[1] + (math.sin(m) * 2)
                    pg.draw.line(surface=screen, color=(0, 0, 0), start_pos=scale(self.ref_center),
                                 end_pos=scale([end_pos_x, end_pos_y]), width=3)
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



class WSParticles:
    """
    Particles (personnel as a point object) in workspace
    """
    def __init__(self, config, screen):
        """
        Initialization of Particles in Workspace
        :param config: configuration file path
        :param screen: Screen object from pygame
        """
        try:
            self.screen = screen
            self.particles = []

            assert self.screen is not None, "Screen does not exists"
            for particle in config:
                ref_color = particle["render"]["ref_pos_color"]
                uwb_color = particle["render"]["uwb_pos_color"]
                est_color = particle["render"]["est_pos_color"]
                ray_cast_color = particle["render"]["ray_cast_color"]
                self.particles.append(WSParticle(id=particle["id"],
                                                 ref_pos_color=(ref_color[0], ref_color[1], ref_color[2]),
                                                 uwb_pos_color=(uwb_color[0], uwb_color[1], uwb_color[2]),
                                                 est_pos_color=(est_color[0], est_color[1], est_color[2]),
                                                 ray_cast_color=(
                                                 ray_cast_color[0], ray_cast_color[1], ray_cast_color[2]),
                                                 center=None,
                                                 radius=particle["render"]["size"]))
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
        Draw particles. This method draw all particles one by one
        :return: None
        """
        try:
            for particle in self.particles:
                particle.draw(self.screen)
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

    def update(self, id, ref_position=None, uwb_position=None, est_position=None, radius=None, world=None,
               ref_heading=None):
        """
        Update Particle positions ( reference true, uwb position, estimated position)
        :param id: Personnel ID
        :param ref_position: reference true position
        :param uwb_position: uwb position
        :param est_position: estimated position
        :param radius: radius of the particle
        :param world: view of the world around the particle
        :param ref_heading: reference true heading of the particle
        :return: None
        """
        try:
            for particle in self.particles:
                if particle.id == id:
                    if ref_position is not None:
                        particle.ref_center = ref_position
                    if uwb_position is not None:
                        particle.uwb_center = uwb_position
                    if est_position is not None:
                        particle.est_center = est_position
                    if radius is not None:
                        particle.radius = radius
                    if world is not None:
                        particle.world_view = world
                    if ref_heading is not None:
                        particle.ref_heading = ref_heading
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
