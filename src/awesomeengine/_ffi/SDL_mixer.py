from ctypes import *

from awesomeengine._ffi.SDL import check_int_error, check_int_zero_error


_sdl_mixer = CDLL('libSDL2_mixer-2.0.so.0')

Mix_Init = _sdl_mixer.Mix_Init
Mix_Init.argtypes = (c_int,)
Mix_Init.restype = c_int
Mix_Init.errcheck = check_int_zero_error

MIX_INIT_FLAC = 0x00000001
MIX_INIT_MOD = 0x00000002
MIX_INIT_MP3 = 0x00000008
MIX_INIT_OGG = 0x00000010
MIX_INIT_MID = 0x00000020
MIX_INIT_OPUS = 0x00000040

Mix_OpenAudio = _sdl_mixer.Mix_OpenAudio
Mix_OpenAudio.argtypes = (c_int, c_uint16, c_int, c_int)
Mix_OpenAudio.restype = c_int
Mix_OpenAudio.errcheck = check_int_error

AUDIO_U16LSB = 0x0010

Mix_AllocateChannels = _sdl_mixer.Mix_AllocateChannels
Mix_AllocateChannels.argtypes = (c_int,)
Mix_AllocateChannels.restype = c_int
Mix_AllocateChannels.errcheck = check_int_error