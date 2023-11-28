#!/usr/bin/env python

import sys

import runner
import log

rep = 25

try:
    rep = int(sys.argv[1])
except:
    pass

runner.begin_tournament(
    [(200, 150, 0), (300, 200, 0), (400, 300, 2), (800, 600, 4)], rep
)

runner.run_tournament()
