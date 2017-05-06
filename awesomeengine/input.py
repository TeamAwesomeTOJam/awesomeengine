from collections import namedtuple

import engine
import sdl2hl


DEADZONE = 0.15


InputEvent = namedtuple('InputEvent', ['target', 'action', 'value'])


class InputManager:

    def __init__(self, input_map = 'default'):
        self._input_map = input_map  
        self._controllers = [sdl2hl.GameController(i) for i in range(sdl2hl.GameController.get_count())]

    def set_input_map(self, input_map):
        self._input_map = input_map

    def process_events(self):
        processed_events = []

        for e in sdl2hl.events.poll():
            if e.type == sdl2hl.EventType.quit:
                processed_events.append(InputEvent('ENGINE', 'QUIT', 1))

            elif e.type == sdl2hl.EventType.controlleraxismotion:
                event = self._new_event(e.which, e.axis, e.value / 32767.0)
                if event != None:
                    processed_events.append(event)
            elif e.type == sdl2hl.EventType.controllerbuttondown:
                event = self._new_event(e.which, e.button, 1)
                if event != None:
                    processed_events.append(event)
            elif e.type == sdl2hl.EventType.controllerbuttonup:
                event = self._new_event(e.which, e.button, 0)
                if event != None:
                    processed_events.append(event)

            elif e.type == sdl2hl.EventType.keydown:
                event = self._new_event(None, e.keycode, 1)
                if event != None:
                    processed_events.append(event)
            elif e.type == sdl2hl.EventType.keyup:
                event = self._new_event(None, e.keycode, 0)
                if event != None:
                    processed_events.append(event)
                    
            elif e.type == sdl2hl.EventType.mousebuttondown:
                event = self._new_event(None, 'Mouse.' + str(e.button), 1)#(1, (e.x, e.y)))
                if event != None:
                    processed_events.append(event)
            elif e.type == sdl2hl.EventType.mousebuttonup:
                event = self._new_event(None, 'Mouse.' + str(e.button), 0)#(0, (e.x, e.y)))
                if event != None:
                    processed_events.append(event)
            elif e.type == sdl2hl.EventType.mousemotion:
                event = self._new_event(None, 'Mouse.Motion', ((e.x, e.y), (e.xrel, e.yrel)))
                if event != None:
                    processed_events.append(event)
            else:
                pass
        
        return processed_events
    
    def _new_event(self, device_id, control_id, value):
        input_map = engine.get().resource_manager.get('inputmap', self._input_map)
        
        if device_id is None:
            target_and_action = input_map.get('%s' % (control_id,))
        else:
            target_and_action = input_map.get('%s %s' % (device_id, control_id))
        
        if target_and_action == None:
            return None
        else:
            target, action = target_and_action
            if action.startswith('-'):
                value = -value
                action = action[1:]
            return InputEvent(target, action, value)

