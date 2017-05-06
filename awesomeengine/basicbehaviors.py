import sdl2hl

from behavior import *
import engine
import rectangle


class DrawHitBox(Behavior):

    def __init__(self):
        self.required_attrs = ('x', 'y', 'width', 'height', ('colour', (255,0,255,255)))
        self.event_handlers = {'draw': self.handle_draw}

    def handle_draw(self, entity, camera):
        camera.draw_rect(entity.colour, rectangle.from_entity(entity))
        camera.draw_rect(entity.colour, rectangle.from_entity(entity).bounding_rect())


class DrawScaledImage(Behavior):

    def __init__(self):
        self.required_attrs = ('x', 'y', 'width', 'height', 'image', ('angle', 0))
        self.event_handlers = {'draw': self.handle_draw}

    def handle_draw(self, entity, camera):
        camera.draw_image(rectangle.from_entity(entity), engine.get().resource_manager.get('image', entity.image))


class MoveUsingVelocity(Behavior):

    def __init__(self):
        self.required_attrs = ('x', 'y', ('vx', 0), ('vy', 0))
        self.event_handlers = {'update': self.handle_update}

    def handle_update(self, entity, dt):
        entity.x += dt * entity.vx
        entity.y += dt * entity.vy
        engine.get().entity_manager.update_position(entity)


class CalculateVelocity(Behavior):
    
    def __init__(self):
        self.required_attrs = ('mass', ('fx', 0), ('fy', 0), ('vx', 0), ('vy', 0))
        self.event_handlers = {'update': self.handle_update}

    def handle_update(self, entity, dt):
        entity.vx += dt * entity.fx / entity.mass
        entity.vy += dt * entity.fy / entity.mass


class DrawStaticText(Behavior):

    def __init__(self):
        self.required_attrs = ('colour', 'size', 'text', 'font')
        self.event_handlers = {'draw': self.handle_draw}

    def add(self, entity):
        font = engine.get().resource_manager.get('font', (entity.font, entity.size))
        surface = font.render_solid(entity.text, entity.colour)
        entity.texture = sdl2hl.Texture.from_surface(engine.get().renderer, surface)

        entity.width = entity.texture.w
        entity.height = entity.texture.h

    def handle_draw(self, entity, camera):
        try:
            x_percent = entity.x_percent
            y_percent = entity.y_percent

            x, y = camera.screen_percent_point((x_percent,y_percent))

        except AttributeError:
            x, y = entity.x , entity.y

        try:
            a = entity.angle
        except AttributeError:
            a = 0

        camera.draw_image(rectangle.Rect(x, y, entity.width, entity.height, a), entity.texture)


class DrawDynamicText(Behavior):

    def __init__(self):
        self.required_attrs = ('colour', 'size', ('text',''), 'topleft', 'font')
        self.event_handlers = {'draw': self.handle_draw}

    def handle_draw(self, entity, camera):
        if len(entity.text) > 0:
            font = engine.get().resource_manager.get('font', (entity.font, entity.size))
            surface = font.render_solid(entity.text, entity.colour)
            texture = sdl2hl.Texture.from_surface(engine.get().renderer, surface)
            x,y = camera.screen_percent_point(entity.topleft)
            r = rectangle.Rect(x + texture.w/2, y - texture.h/2, texture.w, texture.h)
            camera.draw_image(r, texture)

class DrawDynamicTextCentered(Behavior):

    def __init__(self):
        self.required_attrs = ('colour', 'size', ('text',''), 'x', 'y', 'font')
        self.event_handlers = {'draw': self.handle_draw}

    def handle_draw(self, entity, camera):
        if len(entity.text) > 0:
            font = engine.get().resource_manager.get('font', (entity.font, entity.size))
            surface = font.render_solid(entity.text, entity.colour)
            texture = sdl2hl.Texture.from_surface(engine.get().renderer, surface)
            r = rectangle.Rect(entity.x, entity.y, texture.w, texture.h)
            camera.draw_image(r, texture)

class WorldMouseFollower(Behavior):

    def __init__(self):
        self.required_attrs = ('x', 'y')
        self.event_handlers = {'input': self.handle_input}

    def handle_input(self, entity, action, value):
        if action == 'move':
            p = (value[0][0], value[0][1])
            # get the camera
            cams = engine.get().entity_manager.get_by_tag('camera')
            for c in cams:
                r = rectangle.Rect(c.screen_x + c.screen_width/2, c.screen_y + c.screen_height/2, c.screen_width, c.screen_height)
                if r.contains(p):
                    world_point = c.camera.screen_to_world(p)
                    entity.x = world_point[0]
                    entity.y = world_point[1]
                    entity.handle('move')
                    break

class ScreenMouseFollower(Behavior):

    def __init__(self):
        self.required_attrs = ('x', 'y')
        self.event_handlers = {'input': self.handle_input}

    def handle_input(self, entity, action, value):
        if action == 'move':
            entity.x, entity.y = (value[0][0], value[0][1])
            entity.handle('move')

class HudWorldMouseClicker(Behavior):

    def __init__(self):
        self.required_attrs = ('x', 'y',
                               ('world_x', 0),
                               ('world_y', 0),
                               ('hud_pressed_list', []),
                               ('world_pressed_list', []))
        self.event_handlers = {'input' : self.handle_input,
                               'move' : self.handle_move}


    def handle_input(self, entity, action, value):
        if action == 'click':
            if value == 1:
                cams = engine.get().entity_manager.get_by_tag('camera')
                for c in cams:
                    r = rectangle.Rect(c.screen_x + c.screen_width / 2, c.screen_y + c.screen_height / 2, c.screen_width, c.screen_height)
                    if r.contains((entity.x, entity.y)):
                        #we found our camera, first check hud
                        hud_point = c.camera.screen_to_hud((entity.x, entity.y))
                        for e in c.camera.hud_entities:
                            if 'clickable' not in e.tags:
                                break
                            hud_ent_rect = rectangle.from_entity(e)
                            if hud_ent_rect.contains(hud_point):
                                entity.hud_pressed_list.append(e)
                                e.handle('pressed')
                        #if we found a hud element, we are done
                        if entity.hud_pressed_list:
                            return
                        #now check world
                        world_point = c.camera.screen_to_world((entity.x, entity.y))
                        entity.world_pressed_list = engine.get().entity_manager.get_in_area('clickable', rectangle.Rect(world_point[0], world_point[1], 0, 0))
                        for e in entity.world_pressed_list:
                            e.handle('pressed')
        if value == 0:
            for e in entity.world_pressed_list:
                e.handle('released')
                e.handle('clicked')
            for e in entity.hud_pressed_list:
                e.handle('released')
                e.handle('clicked')

    def handle_move(self, entity):
        if entity.world_pressed_list:
            cams = engine.get().entity_manager.get_by_tag('camera')
            for c in cams:
                r = rectangle.Rect(c.screen_x + c.screen_width / 2, c.screen_y + c.screen_height / 2, c.screen_width,
                                   c.screen_height)
                if r.contains((entity.x, entity.y)):
                    world_point = c.camera.screen_to_world((entity.x, entity.y))
                    new_world_pressed_list = engine.get().entity_manager.get_in_area('clickable', rectangle.Rect(world_point[0], world_point[1],0,0))
                    for e in entity.world_pressed_list:
                        if e not in new_world_pressed_list:
                            e.handle('released')
                    entity.world_pressed_list = new_world_pressed_list
        if entity.hud_pressed_list:
            cams = engine.get().entity_manager.get_by_tag('camera')
            for c in cams:
                r = rectangle.Rect(c.screen_x + c.screen_width / 2, c.screen_y + c.screen_height / 2, c.screen_width,
                                   c.screen_height)
                if r.contains((entity.x, entity.y)):
                    hud_point = c.camera.screen_to_hud((entity.x, entity.y))
                    new_hud_pressed_list = []
                    for e in c.camera.hud_entities:
                        if 'clickable' not in e.tags:
                            break
                        hud_ent_rect = rectangle.from_entity(e)
                        if hud_ent_rect.contains(hud_point):
                            new_hud_pressed_list.append(e)
                    for e in entity.hud_pressed_list:
                        if e not in new_hud_pressed_list:
                            e.handle('released')
                    entity.hud_pressed_list = new_hud_pressed_list
        #TODO so much code waste here
        cams = engine.get().entity_manager.get_by_tag('camera')
        for c in cams:
            r = rectangle.Rect(c.screen_x + c.screen_width / 2, c.screen_y + c.screen_height / 2, c.screen_width,
                               c.screen_height)
            if r.contains((entity.x, entity.y)):
                world_point = c.camera.screen_to_world((entity.x, entity.y))
                entity.world_x = world_point[0]
                entity.world_y = world_point[1]





class MouseClicker(Behavior):

    def __init__(self):
        self.required_attrs = ('x', 'y', ('pressed_list', []))
        self.event_handlers =  {'input' : self.handle_input,
                                'move' : self.handle_move}

    def handle_input(self, entity, action, value):
        if action == 'click':
            if value == 1:
                #button down, find what we are clicking on
                entity.pressed_list = engine.get().entity_manager.get_in_area('clickable', rectangle.Rect(entity.x, entity.y,0,0))
                for e in entity.pressed_list:
                    e.handle('pressed')
            elif value == 0:
                for e in entity.pressed_list:
                    e.handle('released')
                    e.handle('clicked')

    def handle_move(self, entity):
        if entity.pressed_list:
            new_pressed_list = engine.get().entity_manager.get_in_area('clickable', rectangle.Rect(entity.x, entity.y,0,0))
            for e in entity.pressed_list:
                if e not in new_pressed_list:
                    e.handle('released')
            entity.pressed_list = new_pressed_list

class BasicButton(Behavior):

    def __init__(self):
        self.required_attrs = ('x', 'y', 'width', 'height',
                              'up_text', 'down_text',
                              'up_colour', 'down_colour',
                              ('text', ''),
                              ('current_colour', (0,0,0)),
                               ('pressed', False))
        self.event_handlers = {'draw' : self.handle_draw,
                               'pressed': self.handle_pressed,
                               'released': self.handle_released}

    def add(self, entity):
        super(BasicButton, self).add(entity)
        entity.text = entity.up_text
        entity.current_colour = entity.up_colour

    def handle_draw(self, entity, camera):
        camera.draw_rect(entity.current_colour, rectangle.from_entity(entity))

    def handle_pressed(self, entity):
        entity.text = entity.down_text
        entity.current_colour = entity.down_colour
        entity.pressed = True

    def handle_released(self, entity):
        entity.text = entity.up_text
        entity.current_colour = entity.up_colour
        entity.pressed = False


class RotateOnInput(Behavior):

    def __init__(self):
        self.required_attrs = ('angle', ('va', 0), ('angular_speed', 10))
        self.event_handlers = {
            'update': self.handle_update,
            'input': self.handle_input
        }

    def handle_update(self, entity, dt):
        entity.angle = (entity.angle + entity.va*dt) % 360

        engine.get().entity_manager.update_position(entity)

    def handle_input(self, entity, action, value):
        if action == 'ccw' and value == 1:
            entity.va = entity.angular_speed
        elif action == 'cw' and value == 1:
            entity.va = -entity.angular_speed
        elif (action == 'ccw' or action == 'cw') and value == 0:
            entity.va = 0


class ChangeVelocityOnInput(Behavior):

    def __init__(self):
        self.required_attrs = (('vx', 0), ('vy', 0), ('speed', 100))
        self.event_handlers = {'input': self.handle_input}

    def handle_input(self, entity, action, value):
        if action == 'up' and value == 1:
            entity.vy = entity.speed
        elif action == 'down' and value == 1:
            entity.vy = -entity.speed
        elif (action == 'up' or action == 'down') and value == 0:
            entity.vy = 0
        if action == 'left' and value == 1:
            entity.vx = -entity.speed
        elif action == 'right' and value == 1:
            entity.vx = entity.speed
        elif (action == 'left' or action == 'right') and value == 0:
            entity.vx = 0


class ZoomOnInput(Behavior):

    def __init__(self):
        self.required_attrs = ('width', 'height', ('zoom_speed', 1.5))
        self.event_handlers = {'input': self.handle_input}

    def handle_input(self, entity, action, value):
        if action == 'zoom in' and value == 1:
            entity.width /= entity.zoom_speed
            entity.height /= entity.zoom_speed
        elif action == 'zoom out' and value == 1:
            entity.width *= entity.zoom_speed
            entity.height *= entity.zoom_speed
        
class SyncWithEntity(Behavior):

    def __init__(self):
        self.required_attrs = ('sync_target', 'sync_attributes')
        self.event_handlers = {'update' : self.handle_update}
    
    def handle_update(self, entity, dt):
        target = engine.get().entity_manager.get_by_name(entity.sync_target)
        for attribute in entity.sync_attributes:
            entity.__dict__[attribute] = getattr(target, attribute)
            
class Animate(Behavior):
    
    def __init__(self):
        self.required_attrs = ('default_animation',)
        self.event_handlers = {'update': self.handle_update, 'play_animation': self.handle_play_animation}

    def add(self, entity):
        super(Animate, self).add(entity)
        self.handle_play_animation(entity, entity.default_animation, reset=True, loop=True)

    def handle_update(self, entity, dt):
        animation = engine.get().resource_manager.get('animation', entity.animation_name)
        frame = animation.frames[entity.current_frame]
        
        entity.current_frame_time += dt
        
        if entity.current_frame_time > frame.duration:
            entity.current_frame_time -= frame.duration
            
            if entity.current_frame == len(animation.frames) - 1: # already on the last frame
                if not entity.loop_animation:
                    entity.animation_name = entity.default_animation
                entity.current_frame = 0
            else:
                entity.current_frame += 1
            
            new_frame = animation.frames[entity.current_frame]
            for name in new_frame.attributes._fields:
                value = getattr(new_frame.attributes, name)
                entity.__dict__[name] = value
                
            for event in new_frame.events:
                entity.handle(event[0], *event[1:])
        
    def handle_play_animation(self, entity, animation_name, reset=False, loop=False):
        if reset or entity.animation_name != animation_name:
            entity.animation_name = animation_name
            entity.current_frame = 0
            entity.current_frame_time = 0
            entity.loop_animation = loop

class TimeToLive(Behavior):

    def __init__(self):
        self.required_attrs = ('time_to_live',)
        self.event_handlers = {'update': self.handle_update}

    def handle_update(self, entity, dt):
        entity.time_to_live -= dt
        if entity.time_to_live <= 0:
            engine.get().entity_manager.remove(entity)

class RadioButton(Behavior):

    def __init__(self):
        self.required_attrs = ('x', 'y', 'width', 'height',
                               'up_text', 'down_text',
                               'up_colour', 'down_colour',
                               ('text', ''),
                               ('current_colour', (0, 0, 0)),
                               'radio_group',
                               ('selected', False))
        self.event_handlers = {'draw': self.handle_draw,
                               'clicked': self.handle_clicked,
                               'un_selected': self.unselect}

    def add(self, entity):
        super(RadioButton, self).add(entity)
        if entity.selected:
            entity.text = entity.down_text
            entity.current_colour = entity.down_colour
        else:
            entity.text = entity.up_text
            entity.current_colour = entity.up_colour

    def handle_draw(self, entity, camera):
        camera.draw_rect(entity.current_colour, rectangle.from_entity(entity))

    #def handle_pressed(self, entity):
    #    entity.text = entity.down_text
    #    entity.current_colour = entity.down_colour

    def unselect(self, entity):
        entity.text = entity.up_text
        entity.current_colour = entity.up_colour
        entity.selected = False

    def handle_clicked(self, entity):
        eng = engine.get()
        #find other radio buttons
        all = eng.entity_manager.get_by_tag('radio_button')
        group = []
        for e in all:
            if e.radio_group == entity.radio_group and not e == entity:
                e.handle('un_selected')

        entity.text = entity.down_text
        entity.current_colour = entity.down_colour
        entity.selected = True
