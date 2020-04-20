from awesomeengine._ffi.SDL import *


class Clock(object):
    def __init__(self):
        self.previous_time = SDL_GetTicks()

    def tick(self, fps_limit=0):
        current_time = SDL_GetTicks()
        time_elapsed = current_time - self.previous_time
        if fps_limit:
            wait_time = max(0, int(1000.0 / fps_limit - time_elapsed))
            SDL_Delay(wait_time)
        now = SDL_GetTicks()
        dt = (now - self.previous_time) / 1000.0
        self.previous_time = now
        return dt
