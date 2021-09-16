from __future__ import generator_stop
from __future__ import annotations

from .WSLayout import WSLayout
from .WSParticle import WSParticles
from .WSRobot import WSRobots
from .WS import WS
from .scaling import set_scaling_factor, get_scaling_factor, scale

__all__ = [
    'set_scaling_factor',
    'get_scaling_factor',
    'scale',
    'WSLayout',
    'WSParticles',
    'WSRobots',
    'WS'
]

__version__ = '0.0.1'
