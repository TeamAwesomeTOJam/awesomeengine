from ctypes import *
from awesomeengine._ffi.SDL import check_int_error


_sdl_ttf = CDLL('libSDL2_ttf-2.0.so.0')

TTF_Init = _sdl_ttf.TTF_Init
TTF_Init.argtypes = tuple()
TTF_Init.restype = c_int
TTF_Init.errcheck = check_int_error