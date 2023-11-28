#!/usr/bin/env python

import math

import mover


class shot(mover.mover):
    def __init__(self, pos, direction, speed, power, bot):
        mover.mover.__init__(self, pos, direction, speed)
        self.owner = bot
        self.power = power
