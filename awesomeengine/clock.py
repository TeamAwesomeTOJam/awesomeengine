import sdl2hl

class Clock(object):
    def __init__(self):
        self.last_tick = sdl2hl.timer.get_ticks()

    def tick(self, fps=0):
        current_time = sdl2hl.timer.get_ticks()
        time_elapsed = current_time - self.last_tick
        if fps:
            wait_time = max(0, int(1000.0/fps - time_elapsed))
            sdl2hl.timer.delay(wait_time)
        now = sdl2hl.timer.get_ticks()
        spf = (now - self.last_tick)/1000.0
        self.last_tick = now
        return spf