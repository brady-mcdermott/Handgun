import pygame, os
from CameraGroup import CameraGroup
from Target import Target
import constants
from random import randint

# ----------------- System -----------------

pygame.init()
pygame.font.init()

# Window
win = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

# Window Title
pygame.display.set_caption("Saloon Shooter")

# Keep Mouse Constrained
pygame.event.set_grab(True)

# Clock
clock = pygame.time.Clock()

# Create new target every 4 seconds
SPAWNTARGETEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNTARGETEVENT, 4000)

# Create new cowboy target (more points)
SPAWNCOWBOYEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNCOWBOYEVENT, 10000)


# Fonts
points_font = pygame.font.SysFont('Comic Sans MS', 30, bold = pygame.font.Font.bold)


# --------------- Background ----------------

background = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.png')), (constants.WIDTH, constants.HEIGHT))


# ----------------- Rifle -------------------

rifle = pygame.image.load(os.path.join('Assets', 'rifle.png'))


# ----------------- Camera ------------------

camera_group = CameraGroup()


# ---------------- Bullets ------------------

bulletPic = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bullet2.png')), (30, 125))


# ----------------- Sounds ------------------

# Background Music (looping)
soundObjBackground = pygame.mixer.Sound(os.path.join('Assets', 'WildWest.mp3'))
soundObjBackground.play(-1)

# Self Explanatory
gunShot = pygame.mixer.Sound(os.path.join('Assets', 'gunSound.mp3'))
targetHit = pygame.mixer.Sound(os.path.join('Assets', 'targetHit.wav'))
reloadSound = pygame.mixer.Sound(os.path.join('Assets', 'reload.wav'))


# ----------------- Misc --------------------

# Draw static screen objects, update bullets and score
def redraw_foreground(bullets, retical_color, total_points):

    # Rifle
    win.blit(rifle, (constants.WIDTH // 2, constants.HEIGHT - 300))

    # Crosshair
    pygame.draw.line(win, retical_color, (constants.WIDTH // 2 - 10, constants.HEIGHT // 2), (constants.WIDTH // 2 + 10, constants.HEIGHT // 2), 5)
    pygame.draw.line(win, retical_color, (constants.WIDTH // 2, constants.HEIGHT // 2 - 10), (constants.WIDTH // 2, constants.HEIGHT // 2 + 10), 5)
    
    # Bullets
    for i in range(bullets):
        win.blit(bulletPic, (40*i, constants.HEIGHT - 130))

    # Score
    points_text = points_font.render("Score: " + str(total_points), False, (0,0,0))
    win.blit(points_text, (0,0))


# Main Loop
def main():
    run = True

    # Initialize number of bullets
    bullets = 7

    # Reset Score
    total_points = 0

    # Generate first target (populates list so safe to remove later)
    now = pygame.time.get_ticks()
    camera_group.gen_new_target(now)

    while run:
        
        # Increment clock
        clock.tick(constants.FPS)

        # Set crosshairs to red
        retical_color = (255, 0, 0)
        
        # Check for user input
        for event in pygame.event.get():

            # X-button (although inaccessable)
            if event.type == pygame.QUIT:
                run = False

            # Generate new target every 4 seconds
            if event.type == SPAWNTARGETEVENT:
                now = pygame.time.get_ticks()

                camera_group.gen_new_target(now)

            # Mouse clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        # Check if enough bullets to fire
                        if bullets != 0:

                            # Assign points if target hit on click
                            new_points = camera_group.check_targets()

                            # If points given, target was hit
                            if new_points != 0:
                                targetHit.play()

                            # Update score
                            total_points += new_points

                            # Flash retical to yellow
                            retical_color = (255, 255, 0)

                            # Decrement bullet count
                            bullets -= 1

                            # Pow
                            gunShot.play()

        # Check for keyboard input
        pressed_keys = pygame.key.get_pressed()

        # End all processes (Q)
        if pressed_keys[pygame.K_q]: # Quit
            run = False

        # Reload (R) so long as chamber is not full
        if pressed_keys[pygame.K_r] and bullets != constants.CLIP_SIZE: # Reload

            # Reloading takes time people
            pygame.time.delay(500)

            # Fill the chamber
            bullets = 7

            # Chi-chick
            reloadSound.play()

        # Update camera class
        camera_group.update()
        camera_group.custom_draw()

        # Update bullets UI, score, flash retical color, 
        redraw_foreground(bullets, retical_color, total_points)

        # Flip
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()