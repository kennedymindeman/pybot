#!/usr/bin/env python

import bot
import botloader
import log

bots = botloader.load_bots()

for name, ai, color in bots:
    b = bot.bot(name, (0, 0), None, ai, color)
    if b.check_valid():
        log.major("%s -> %d" % (name, b.calc_cost()))
    else:
        log.major("%s -> INVALID" % name)
