import android
import os
import sys
import time

import vars

droid = android.Android()


class gui:
    def __init__(self):
        self.root = None
        self.last_redraw = time.time()

    def map(self, x):
        return x * vars.GUI_SCALE

    def mapcolor(self, col):
        return "#%.2x%.2x%.2x" % col

    def openwv(self, w, h):
        self.wv = os.path.join(os.path.dirname(sys.argv[0]), "tmp.html")
        self.w = w
        self.h = h

        fp = open(self.wv, "w")
        fp.write(
            """<!doctype html>
<html><head><title>PyBots</title>
<script>
var droid = new Android();

function clear(g,w,h) {
	g.fillStyle="#000000"; g.fillRect(0,0,w,h);
}
function circle(g,col,x,y,r) {
	g.fillStyle=col
	g.beginPath();
	g.arc(x, y, r, 0, Math.PI*2, true); 
	g.closePath();
	g.fill();
}
function cross(g,x,y,r) {
	g.moveTo(x-r, y-r);
	g.lineTo(x+r, y+r);
	g.moveTo(x-r, y+r);
	g.lineTo(x+r, y-r);
}
function act(e) {
// 	var l = document.getElementById("log"); 
	var c = document.getElementById("canvas");
	var g = c.getContext("2d");
	eval(e.data);
}
function start() {
	droid.registerCallback("js", act);
}
</script>
</head>
<body onLoad="start();" style="color: #fff; background-color: #000;">
<canvas id="canvas" width="%d" height="%d" style="border: 1px solid #fff;"></canvas>
<br/><br/><p id="log"></p>
</body></html>
"""
            % (w, h)
        )
        fp.close()

        droid.webViewShow("file://" + self.wv)

    def closewv(self):
        os.unlink(self.wv)

    def circle(self, pos, radius, color=(0xFF, 0xFF, 0xFF)):
        x = self.map(pos[0])
        y = self.map(pos[1])
        r = self.map(radius)
        color = self.mapcolor(color)
        return 'circle(g,"%s",%d,%d,%d);' % (color, x, y, r)

    def cross(self, pos, radius):
        x = self.map(pos[0])
        y = self.map(pos[1])
        r = self.map(radius)
        return "cross(g,%d,%d,%d);" % (x, y, r)

    def clear(self):
        return "clear(g,%d,%d);" % (self.w, self.h)

    def redraw(self):
        cmd = self.clear()

        for b in self.arena.bots:
            cmd += self.circle(b.pos, b.size, b.color)

        cmd += 'g.strokeStyle="%s";g.beginPath();' % self.mapcolor((0xFF, 0, 0))
        for s in self.arena.shots:
            cmd += self.cross(s.pos, 0.5 / vars.GUI_SCALE * s.power)
        cmd += "g.closePath();g.stroke();"

        droid.eventPost("js", cmd)

    def redrawgui(self):
        self.redraw()

        now = time.time()
        sleep_time = (1.0 / vars.GUI_FPS) - (now - self.last_redraw)
        self.last_redraw = now

        if sleep_time > 0:
            time.sleep(sleep_time)

    def startgui(self, ar, callback):
        self.arena = ar
        self.callback = callback

        self.openwv(self.map(self.arena.width), self.map(self.arena.height))
        try:
            self.last_redraw = time.time()
            while self.callback():
                self.redrawgui()
        finally:
            self.closewv()
