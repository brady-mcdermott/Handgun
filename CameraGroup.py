import constants
import pygame, sys, os
import math
from random import randint
from Target import Target


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        # List of current targets
        self.targets = []

        # Initialize collison
        self.collide = False

        # Create Camera Offset
        self.offset = pygame.math.Vector2()

        # Declare midway points
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Keep track of camera location to calculate hitboxes
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        
        # Create rect
        self.camera_rect = pygame.Rect(l,t,w,h)

        # Surface to zoom into
        self.back_surface = pygame.image.load(os.path.join('Assets', 'background.png')).convert_alpha()
        self.back_rect = self.back_surface.get_rect(topleft = (0,0))

        # Create zoomable surface
        self.internal_surface_size = (2500, 2500)

        # Create surface
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)

        # Place surface in center
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_w, self.half_h))

        # Position data
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)

        # Camera Offset
        self.internal_off = pygame.math.Vector2()
        self.internal_off.x = self.internal_surface_size[0] // 2 - self.half_w
        self.internal_off.y = self.internal_surface_size[1] // 2 - self.half_h

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        
        # Increase speed with distance from center (smoother flow)
        speed = math.hypot(mouse.x - self.half_w, mouse.y - self.half_h) // 15
        
        # Create static zone (no movement) when mouse in center 
            # Sorry about different resolutions! Was and still am too tired to do more math!
        if mouse.x > self.half_w + 100 and self.offset.x < 945 - speed:
            self.offset.x += 1 * speed
        if mouse.x < self.half_w - 100 and self.offset.x > -305 + speed:
            self.offset.x -= 1 * speed
        if mouse.y > self.half_h + 100 and self.offset.y < 509 - speed:
            self.offset.y += 1 * speed
        if mouse.y < self.half_h - 100 and self.offset.y > -190 + speed:
            self.offset.y -= 1 * speed

    # Create new target within aimable bounds (still sorry about resolutions)
    def gen_new_target(self, time):
        x = randint(350, 1480)
        y = randint(200, 810)
        new_target = Target((x,y), self, time)
        self.targets.append(new_target)

    # Check collisions between targets and crosshairs (center of screen + zoom offset)
    def check_targets(self):
        for target in self.targets:
            self.collide = target.rect.collidepoint((self.camera_rect.centerx + self.offset.x, self.camera_rect.centery + self.offset.y))

            now = pygame.time.get_ticks()
            
            # If target hit or has existed for more than 10 seconds (only award points on hit)
            if self.collide:
                self.targets.remove(target)
                return 10
            elif now - target.spawned_at > 10000:
                self.targets.remove(target)
                return 0
        return 0

    # Maintain object positions which out of view
    def custom_draw(self):

        # Update mouse position
        self.mouse_control()

        # Fill outer edge for looks even though you intentionally don't see the outer edge
        self.internal_surface.fill("#71ddee")

        # Show Background
        back_offset = self.back_rect.topleft - self.offset + self.internal_off
        self.internal_surface.blit(self.back_surface, back_offset)

        # Update target positions and place on screen
        for target in self.targets:
            off_pos = target.rect.topleft - self.offset + self.internal_off
            self.internal_surface.blit(target.image, off_pos)

        # Calculate and show zoom
        scaled_surf = pygame.transform.scale(self.internal_surface, (self.internal_rect.size[0] * 2, self.internal_rect.size[1] * 2))
        scaled_rect = scaled_surf.get_rect(center = (self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)
        