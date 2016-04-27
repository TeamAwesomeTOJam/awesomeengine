from collections import namedtuple

import engine
import sdl2hl


DEADZONE = 0.15


InputEvent = namedtuple('InputEvent', ['target', 'action', 'value'])


class InputManager:

    def __init__(self):
        self._input_map = None
        # pygame.joystick.init()
        # joystick_count = pygame.joystick.get_count()
        # for i in range(joystick_count):
        #     joystick = pygame.joystick.Joystick(i)
        #     joystick.init()
            
    def process_events(self):
        self._input_map = engine.get_engine().resource_manager.get('inputmap', 'default')
        processed_events = []

        for e in sdl2hl.events.poll():
            if e.type == sdl2hl.QUIT:
                processed_events.append(InputEvent('ENGINE', 'QUIT', 1))


            # elif e.type == pygame.JOYAXISMOTION:
            #     control_type = 'AXIS'
            #     device_id = e.joy
            #     value, _ = self._normalize_axis(e.value, 0)
            #     if value >= 0:
            #         event = self._new_event(device_id, control_type, "+%d" % e.axis, value)
            #     if value <= 0:
            #         value = -1 * value
            #         event =  self._new_event(device_id, control_type, "-%d" % e.axis, value)
            #     if event != None:
            #         processed_events.append(event)
            # elif e.type == pygame.JOYBUTTONDOWN:
            #     event = self._new_event(e.joy, 'BUTTON', e.button, 1)
            #     if event != None:
            #         processed_events.append(event)
            # elif e.type == pygame.JOYBUTTONUP:
            #     event = self._new_event(e.joy, 'BUTTON', e.button, 0)
            #     if event != None:
            #         processed_events.append(event)
            elif e.type == sdl2hl.KEYDOWN:
                event = self._new_event(None, 'KEY', e.keycode, 1)
                if event != None:
                    processed_events.append(event)
            elif e.type == sdl2hl.KEYUP:
                event = self._new_event(None, 'KEY', e.keycode, 0)
                if event != None:
                    processed_events.append(event)
            # elif e.type == pygame.JOYHATMOTION:
            #     pass
            elif e.type == sdl2hl.MOUSEBUTTONDOWN:
                event = self._new_event(None, 'MOUSE', e.button, 1)
                if event != None:
                    processed_events.append(event)
            elif e.type == sdl2hl.MOUSEBUTTONUP:
                event = self._new_event(None, 'MOUSE', e.button, 0)
                if event != None:
                    processed_events.append(event)
            else:
                pass
        
        # event = InputEvent('mouse','MOUSE_POSITION',pygame.mouse.get_pos())
        # processed_events.append(event)
        
        return processed_events
    
    def _new_event(self, device_id, control_type, control_id, value):
        if device_id == None:
            target_and_action = self._input_map.get('%s %s' % (control_type, control_id))
        else:
            target_and_action = self._input_map.get('%s %s %s' % (device_id, control_type, control_id))
        
        if target_and_action == None:
            return None
        else:
            target, action = target_and_action
            return InputEvent(target, action, value)
    
    def _normalize_axis(self, x, y):              
        magnitude = ((x**2) + (y**2)) ** 0.5

        if magnitude < DEADZONE:
            new_x = 0
            new_y = 0
        else:
            new_x = (x / magnitude) * (magnitude - DEADZONE) / (1 - DEADZONE)
            new_y = (y / magnitude) * (magnitude - DEADZONE) / (1 - DEADZONE)
        
        return new_x, new_y
