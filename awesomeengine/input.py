from collections import namedtuple

import engine
import sdl2hl


DEADZONE = 0.15


InputEvent = namedtuple('InputEvent', ['target', 'action', 'value'])


class InputManager:

    def __init__(self):
        self._input_map = None
        
        self._controllers = [sdl2hl.GameController(i) for i in range(sdl2hl.GameController.get_count())]
            
    def process_events(self):
        self._input_map = engine.get().resource_manager.get('inputmap', 'default')
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
                event = self._new_event(None, e.button, 1)
                if event != None:
                    processed_events.append(event)
            elif e.type == sdl2hl.EventType.mousebuttonup:
                event = self._new_event(None, e.button, 0)
                if event != None:
                    processed_events.append(event)
            else:
                pass
        
        return processed_events
    
    def _new_event(self, device_id, control_id, value):
        if device_id is None:
            target_and_action = self._input_map.get('%s' % (control_id,))
        else:
            target_and_action = self._input_map.get('%s %s' % (device_id, control_id))
        
        if target_and_action == None:
            return None
        else:
            target, action = target_and_action
            if action.startswith('-'):
                value = -value
                action = action[1:]
            return InputEvent(target, action, value)

