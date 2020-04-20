import ctypes

from awesomeengine import engine, _ffi


class Action:

    def __init__(self, target, action, value):
        self.target = target
        self.action = action
        self.value = value

    @classmethod
    def from_event(cls, input_map, identifier, value):
        input_map = engine.get().resource_manager.get('inputmap', input_map)
        target_and_action = input_map.get(identifier)

        if target_and_action is None:
            return None
        else:
            target, action = target_and_action
            if action.startswith('-'):
                value = -value
                action = action[1:]
            return cls(target, action, value)


class MouseClick:

    def __init__(self, button, state, clicks, x, y):
        self.button = button
        self.state = state
        self.clicks = clicks
        self.x = x
        self.y = y

    @classmethod
    def from_event(cls, event):
        return cls(
            event.button,
            event.state,
            event.clicks,
            event.x,
            event.y
        )


class MouseMove:

    def __init__(self, x, y, xrel, yrel):
        self.x = x
        self.y = y
        self.xrel = xrel
        self.yrel = yrel

    @classmethod
    def from_event(cls, event):
        return cls(
            event.x,
            event.y,
            event.xrel,
            event.yrel
        )


class InputManager:

    def __init__(self, input_map = 'default'):
        self._input_map = input_map  
        self._controllers = [_ffi.SDL_GameControllerOpen(i) for i in range(_ffi.SDL_NumJoysticks())
                             if _ffi.SDL_IsGameController(i)]

    def set_input_map(self, input_map):
        self._input_map = input_map

    def process_events(self):
        actions = []
        mouse_events = []

        e = _ffi.SDL_Event()
        while _ffi.SDL_PollEvent(ctypes.byref(e)):
            if e.type == _ffi.SDL_QUIT:
                actions.append(Action('ENGINE', 'QUIT', 1))

            elif e.type == _ffi.SDL_CONTROLLERAXISMOTION:
                e = e.caxis
                action = Action.from_event(self._input_map, f'CA.{e.which}.{e.axis}', e.value / 32767.0)
                if action is not None:
                    actions.append(action)
            elif e.type == _ffi.SDL_CONTROLLERBUTTONDOWN:
                e = e.cbutton
                action = Action.from_event(self._input_map, f'CB.{e.which}.{e.button}', 1)
                if action is not None:
                    actions.append(action)
            elif e.type == _ffi.SDL_CONTROLLERBUTTONUP:
                e = e.cbutton
                action = Action.from_event(self._input_map, f'CB.{e.which}.{e.button}', 0)
                if action is not None:
                    actions.append(action)

            elif e.type == _ffi.SDL_KEYDOWN and not e.key.repeat:
                e = e.key
                action = Action.from_event(self._input_map, f'K.{e.keysym.scancode}', 1)
                if action is not None:
                    actions.append(action)
            elif e.type == _ffi.SDL_KEYDOWN and not e.key.repeat:
                e = e.key
                action = Action.from_event(self._input_map, f'K.{e.keysym.scancode}', 0)
                if action is not None:
                    actions.append(action)
                    
            elif e.type == _ffi.SDL_MOUSEBUTTONDOWN:
                e = e.button
                action = Action.from_event(self._input_map, f'M.{e.button}', 1)
                if action is not None:
                    actions.append(action)
                mouse_events.append(MouseClick.from_event(e))
            elif e.type == _ffi.SDL_MOUSEBUTTONUP:
                e = e.button
                action = Action.from_event(self._input_map, f'M.{e.button}', 1)
                if action is not None:
                    actions.append(action)
                mouse_events.append(MouseClick.from_event(e))
            elif e.type == _ffi.SDL_MOUSEMOTION:
                e = e.motion
                mouse_events.append(MouseMove.from_event(e))
            else:
                pass

            e = _ffi.SDL_Event()
        
        return actions, mouse_events


