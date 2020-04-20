from ctypes import *


_sdl = CDLL('libSDL2-2.0.so.0')


# SDL_error.h

SDL_GetError = _sdl.SDL_GetError
SDL_GetError.argtypes = tuple()
SDL_GetError.restype = c_char_p

SDL_ClearError = _sdl.SDL_ClearError
SDL_ClearError.argtypes = tuple()
SDL_ClearError.restype = c_void_p


class SDLError(Exception):

    def __init__(self, message):
        super().__init__(message)


def raise_sdl_error():
    error = SDLError(SDL_GetError().decode())
    SDL_ClearError()
    raise error


def check_int_error(result, func, arguments):
    if result < 0:
        raise_sdl_error()
    else:
        return result


def check_int_zero_error(result, func, arguments):
    if result == 0:
        raise_sdl_error()
    else:
        return result


def check_ptr_error(result, func, arguments):
    if not result:
        raise_sdl_error()
    else:
        return result


# SDL.h

SDL_Init = _sdl.SDL_Init
SDL_Init.argtypes = (c_uint32,)
SDL_Init.restype = c_int
SDL_Init.errcheck = check_int_error

SDL_Quit = _sdl.SDL_Quit
SDL_Quit.argtypes = tuple()
SDL_Quit.restype = None

SDL_INIT_TIMER = 0x00000001
SDL_INIT_AUDIO = 0x00000010
SDL_INIT_VIDEO = 0x00000020
SDL_INIT_JOYSTICK = 0x00000200
SDL_INIT_HAPTIC = 0x00001000
SDL_INIT_GAMECONTROLLER = 0x00002000
SDL_INIT_EVENTS = 0x00004000
SDL_INIT_SENSOR = 0x00008000
SDL_INIT_EVERYTHING = (SDL_INIT_TIMER | SDL_INIT_AUDIO | SDL_INIT_VIDEO | SDL_INIT_EVENTS |
                       SDL_INIT_JOYSTICK | SDL_INIT_HAPTIC | SDL_INIT_GAMECONTROLLER | SDL_INIT_SENSOR)


# SDL_rect.h

class SDL_Point(Structure):
    _fields_ = [('x', c_int),
                ('y', c_int)]

class SDL_Rect(Structure):
    _fields_ = [('x', c_int),
                ('y', c_int),
                ('w', c_int),
                ('h', c_int)]

# SDL_video.h

class SDL_Window(Structure):
    _fields_ = []


SDL_CreateWindow = _sdl.SDL_CreateWindow
SDL_CreateWindow.argtypes = (c_char_p, c_int, c_int, c_int, c_int, c_uint32)
SDL_CreateWindow.restype = POINTER(SDL_Window)
SDL_CreateWindow.errcheck = check_ptr_error

SDL_GetWindowFlags = _sdl.SDL_GetWindowFlags
SDL_GetWindowFlags.argtypes = (POINTER(SDL_Window),)
SDL_GetWindowFlags.restype = c_uint32

SDL_SetWindowFullscreen = _sdl.SDL_SetWindowFullscreen
SDL_SetWindowFullscreen.argtypes = (POINTER(SDL_Window), c_uint32)
SDL_SetWindowFullscreen.restype = c_int
SDL_SetWindowFullscreen.errcheck = check_int_error

SDL_WINDOW_FULLSCREEN = 0x00000001

SDL_WINDOWPOS_UNDEFINED = 0x1FFF0000


# SDL_render.h

class SDL_Renderer(Structure):
    _fields_ = []

SDL_CreateRenderer = _sdl.SDL_CreateRenderer
SDL_CreateRenderer.argtypes = (POINTER(SDL_Window), c_int, c_uint32)
SDL_CreateRenderer.restype = POINTER(SDL_Renderer)
SDL_CreateRenderer.errcheck = check_ptr_error

SDL_SetRenderDrawColor = _sdl.SDL_SetRenderDrawColor
SDL_SetRenderDrawColor.argtypes = (POINTER(SDL_Renderer), c_int8, c_int8, c_int8, c_int8)
SDL_SetRenderDrawColor.restype = c_int
SDL_SetRenderDrawColor.errcheck = check_int_error

SDL_RenderClear = _sdl.SDL_RenderClear
SDL_RenderClear.argtypes = (POINTER(SDL_Renderer),)
SDL_RenderClear.restype = c_int
SDL_RenderClear.errcheck = check_int_error

SDL_RenderDrawLines = _sdl.SDL_RenderDrawLines
SDL_RenderDrawLines.argtypes = (POINTER(SDL_Renderer), POINTER(SDL_Point), c_int)
SDL_RenderDrawLines.restype = c_int
SDL_RenderDrawLines.errcheck = check_int_error

SDL_RenderSetClipRect = _sdl.SDL_RenderSetClipRect
SDL_RenderSetClipRect.argtypes = (POINTER(SDL_Renderer), POINTER(SDL_Rect))
SDL_RenderSetClipRect.restype = c_int
SDL_RenderSetClipRect.errcheck = check_int_error


# SDL_timer.h

SDL_GetTicks = _sdl.SDL_GetTicks
SDL_GetTicks.argtypes = tuple()
SDL_GetTicks.restype = c_uint32

SDL_Delay = _sdl.SDL_Delay
SDL_Delay.argtypes = (c_uint32,)
SDL_Delay.restype = None


#SDL_joystick.h

SDL_JoystickID = c_int32

SDL_NumJoysticks = _sdl.SDL_NumJoysticks
SDL_NumJoysticks.argtypes = tuple()
SDL_NumJoysticks.restype = c_int
SDL_NumJoysticks.errcheck = check_int_error


# SDL_gamecontroller.h

class SDL_GameController(Structure):
    _fields_ = []


SDL_IsGameController = _sdl.SDL_IsGameController
SDL_IsGameController.argtypes = (c_int,)
SDL_IsGameController.restype = c_bool

SDL_GameControllerOpen = _sdl.SDL_GameControllerOpen
SDL_GameControllerOpen.argtypes = (c_int,)
SDL_GameControllerOpen.restype = POINTER(SDL_GameController)
SDL_GameControllerOpen.errcheck = check_ptr_error


# SDL_events.h

SDL_QUIT = 0x100
SDL_KEYDOWN = 0x300
SDL_KEYUP = 0x301
SDL_MOUSEMOTION = 0x400
SDL_MOUSEBUTTONDOWN = 0x401
SDL_MOUSEBUTTONUP = 0x402
SDL_CONTROLLERAXISMOTION = 0x650
SDL_CONTROLLERBUTTONDOWN = 0x651
SDL_CONTROLLERBUTTONUP = 0x652

class SDL_Keysym(Structure):
    _fields_ = [
        ('scancode', c_int),
        ('sym', c_char * 4),
        ('mod', c_uint16),
        ('unused', c_uint32)
    ]

class SDL_CommonEvent(Structure):
    _fields_ = [
        ('type', c_uint32),
        ('timestamp', c_uint32)
    ]


class SDL_KeyboardEvent(SDL_CommonEvent):
    _fields_ = [
        ('windowID', c_uint32),
        ('state', c_uint8),
        ('repeat', c_uint8),
        ('padding2', c_uint8),
        ('padding3', c_uint8),
        ('keysym', SDL_Keysym)
    ]

class SDL_MouseMotionEvent(SDL_CommonEvent):
    _fields_ = [
        ('windowID', c_uint32),
        ('which', c_uint32),
        ('state', c_uint32),
        ('x', c_int32),
        ('y', c_int32),
        ('xrel', c_int32),
        ('yrel', c_int32)
    ]

class SDL_SDL_MouseButtonEvent(SDL_CommonEvent):
    _fields_ = [
        ('windowID', c_uint32),
        ('which', c_uint32),
        ('button', c_uint8),
        ('state', c_uint8),
        ('clicks', c_uint8),
        ('padding1', c_uint8),
        ('x', c_int32),
        ('y', c_int32)
    ]

class SDL_ControllerAxisEvent(SDL_CommonEvent):
    _fields_ = [
        ('which', SDL_JoystickID),
        ('axis', c_uint8),
        ('padding1', c_uint8),
        ('padding2', c_uint8),
        ('padding3', c_uint8),
        ('value', c_int16),
        ('padding4', c_uint16)
    ]

class SDL_ControllerButtonEvent(SDL_CommonEvent):
    _fields_ = [
        ('which', SDL_JoystickID),
        ('button', c_uint8),
        ('state', c_uint8),
        ('padding1', c_uint8),
        ('padding2', c_uint8)
    ]

class SDL_Event(Union):
    _fields_ = [
        ('type', c_uint32),
        ('common', SDL_CommonEvent),
        ('key', SDL_KeyboardEvent),
        ('motion', SDL_MouseMotionEvent),
        ('button', SDL_SDL_MouseButtonEvent),
        ('caxis', SDL_ControllerAxisEvent),
        ('cbutton', SDL_ControllerButtonEvent)
    ]

SDL_PollEvent = _sdl.SDL_PollEvent
SDL_PollEvent.argtypes = (POINTER(SDL_Event),)
SDL_PollEvent.restype = c_int
