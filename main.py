import pygame
from pygame.locals import *
import time

pygame.init()
pygame.mixer.init()  # Initialize the mixer

display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
score = 0  # Track score
button_clicked = False  # Track button click state
game_state = "menu"  # Track game state
score_interval = 5  # Initial interval for adding to the score
last_score_time = time.time()  # Track the last time the score was updated
upgrade_cost = 30  # Initial cost for the upgrade
click_multiplier = 1  # Initial click multiplier
click_upgrade_cost = 50  # Initial cost for the click multiplier upgrade
multiplier_upgrade_purchased = False  # Track if the multiplier upgrade has been purchased
last_display_change_time = time.time()  # Track the last time the display changed
cooldown_period = 1  # Cooldown period in seconds

# Set font for score display
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)  # Smaller font size
large_font = pygame.font.Font(None, 100)  # Larger font size
outline_font = pygame.font.Font(None, 38)  # Outline font size

# Load button images for different states
button_image = pygame.image.load("trash.png")
button_hover_image = pygame.image.load("trash_hover.png")
button_click_image = pygame.image.load("trash_click.png")
button_rect = button_image.get_rect(center=(640, 500))

# Load and scale background images
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (1280, 680))
menu_background_image = pygame.image.load("menu_background.png")
menu_background_image = pygame.transform.scale(menu_background_image, (1280, 680))  # Scale to fit the screen
upgrade_background_image = pygame.image.load("upgrade_menu.png")
upgrade_background_image = pygame.transform.scale(upgrade_background_image, (1280, 680))

# Load and play background music
pygame.mixer.music.load("Background_music.wav")
pygame.mixer.music.play(-1)  # Play the music in a loop

def draw_menu():
    screen.blit(menu_background_image, (0, 0))  # Draw the background image
    start_text = font.render("START", True, (255, 255, 255))
    settings_text = font.render("SETTINGS", True, (255, 255, 255))
    quit_text = font.render("QUIT", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(645, 300))
    settings_rect = settings_text.get_rect(center=(640, 400))
    quit_rect = quit_text.get_rect(center=(640, 500))
    screen.blit(start_text, start_rect.topleft)
    screen.blit(settings_text, settings_rect.topleft)
    screen.blit(quit_text, quit_rect.topleft)
    pygame.display.flip()
    return start_rect, settings_rect, quit_rect

def draw_gameplay():
    screen.blit(background_image, (0, 0))  # Draw the background image
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    back_text = small_font.render("BACK", True, (0, 0, 0))
    upgrades_text = small_font.render("UPGRADES", True, (0, 0, 0))
    back_rect = back_text.get_rect(center=(100, 50))
    upgrades_rect = upgrades_text.get_rect(center=(1100, 50))
    score_rect = score_text.get_rect(center=(640, 50))
    screen.blit(score_text, score_rect.topleft)
    screen.blit(button_image, button_rect.topleft)
    screen.blit(back_text, back_rect.topleft)
    screen.blit(upgrades_text, upgrades_rect.topleft)
    pygame.display.flip()
    return back_rect, upgrades_rect

def draw_upgrade_menu():
    screen.blit(upgrade_background_image, (0, 0))
    upgrade_text = small_font.render(f"UPGRADE ({upgrade_cost})", True, (0, 0, 0))
    click_upgrade_text = small_font.render(f"CLICK UPGRADE ({click_upgrade_cost})", True, (0, 0, 0))
    back_text = small_font.render("BACK", True, (0, 0, 0))
    upgrade_rect = upgrade_text.get_rect(center=(640, 340))
    click_upgrade_rect = click_upgrade_text.get_rect(center=(200, 340))
    back_rect = back_text.get_rect(center=(110, 645))
    screen.blit(upgrade_text, upgrade_rect.topleft)
    screen.blit(click_upgrade_text, click_upgrade_rect.topleft)
    screen.blit(back_text, back_rect.topleft)
    pygame.display.flip()
    return upgrade_rect, click_upgrade_rect, back_rect

def draw_settings():
    screen.blit(background_image, (0, 0))  # Draw the background image
    volume_text = font.render("Volume", True, (0, 0, 0))
    volume_up_text = font.render("+", True, (0, 0, 0))
    volume_down_text = font.render("-", True, (0, 0, 0))
    back_text = small_font.render("BACK", True, (0, 0, 0))
    volume_rect = volume_text.get_rect(center=(640, 300))
    volume_up_rect = volume_up_text.get_rect(center=(740, 300))
    volume_down_rect = volume_down_text.get_rect(center=(540, 300))
    back_rect = back_text.get_rect(center=(150, 50))
    screen.blit(volume_text, volume_rect.topleft)
    screen.blit(volume_up_text, volume_up_rect.topleft)
    screen.blit(volume_down_text, volume_down_rect.topleft)
    screen.blit(back_text, back_rect.topleft)
    pygame.display.flip()
    return volume_up_rect, volume_down_rect, back_rect

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width, _ = font.size(word + ' ')
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width

    lines.append(' '.join(current_line))
    return lines

def draw_info():
    overlay = pygame.Surface((1280, 680), pygame.SRCALPHA)  # Create a semi-transparent overlay
    overlay.fill((255, 255, 255, 150))  # Fill the overlay with white and set alpha to 150
    screen.blit(overlay, (0, 0))  # Blit the overlay onto the screen

    info_text = large_font.render("Game Info", True, (0, 0, 0))
    wrapped_text = wrap_text("This is a simple game where you press the trash can to collect trash. Use upgrades to multiply how fast you collect trash. (You will collect one trash every 5 seconds)", small_font, 1000)
    back_text = large_font.render("Back", True, (0, 0, 0))
    info_rect = info_text.get_rect(center=(640, 200))
    back_rect = back_text.get_rect(center=(640, 500))  # Updated position to center
    screen.blit(info_text, info_rect.topleft)

    y_offset = 300
    for line in wrapped_text:
        line_surface = small_font.render(line, True, (0, 0, 0))
        line_rect = line_surface.get_rect(center=(640, y_offset))
        screen.blit(line_surface, line_rect.topleft)
        y_offset += small_font.get_height()

    screen.blit(back_text, back_rect.topleft)
    pygame.display.flip()
    return back_rect

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                game_state = "info"
                last_display_change_time = time.time()  # Update the last display change time

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if game_state == "menu":
        start_rect, settings_rect, quit_rect = draw_menu()
        if time.time() - last_display_change_time > cooldown_period:  # Check cooldown period
            if start_rect.collidepoint(mouse_pos) and mouse_click[0]:
                game_state = "playing"
                last_display_change_time = time.time()  # Update the last display change time
            elif settings_rect.collidepoint(mouse_pos) and mouse_click[0]:
                game_state = "settings"
                last_display_change_time = time.time()  # Update the last display change time
            elif quit_rect.collidepoint(mouse_pos) and mouse_click[0]:
                running = False
    elif game_state == "playing":
        back_rect, upgrades_rect = draw_gameplay()
        if time.time() - last_display_change_time > cooldown_period:  # Check cooldown period
            if button_rect.collidepoint(mouse_pos):
                if mouse_click[0] and not button_clicked:
                    score += 1 * click_multiplier
                    button_clicked = True
                    print(f"Button clicked! Score: {score}")
                elif not mouse_click[0]:
                    button_clicked = False
            if back_rect.collidepoint(mouse_pos) and mouse_click[0]:
                game_state = "menu"
                last_display_change_time = time.time()  # Update the last display change time
            if upgrades_rect.collidepoint(mouse_pos) and mouse_click[0]:
                game_state = "upgrades"
                last_display_change_time = time.time()  # Update the last display change time
        # Update score based on interval
        current_time = time.time()
        if current_time - last_score_time >= score_interval:
            score += 1
            if multiplier_upgrade_purchased:
                score += click_multiplier  # Add the multiplier to the score every interval
            last_score_time = current_time
    elif game_state == "upgrades":
        upgrade_rect, click_upgrade_rect, back_rect = draw_upgrade_menu()
        if time.time() - last_display_change_time > cooldown_period:  # Check cooldown period
            if upgrade_rect.collidepoint(mouse_pos) and mouse_click[0]:
                if score >= upgrade_cost:
                    score -= upgrade_cost
                    score_interval = max(1, score_interval - 1)  # Decrease interval, minimum 1 second
                    upgrade_cost += 2  # Increase the cost by 2
                    print(f"Upgrade clicked! New interval: {score_interval} seconds, New cost: {upgrade_cost}")
            if click_upgrade_rect.collidepoint(mouse_pos) and mouse_click[0]:
                if score >= click_upgrade_cost:
                    score -= click_upgrade_cost
                    click_multiplier *= 2  # Double the click multiplier
                    click_upgrade_cost += 10  # Increase the cost by 10
                    multiplier_upgrade_purchased = True  # Mark the multiplier upgrade as purchased
                    print(f"Click Upgrade clicked! New multiplier: {click_multiplier}, New cost: {click_upgrade_cost}")
            if back_rect.collidepoint(mouse_pos) and mouse_click[0]:
                game_state = "playing"
                last_display_change_time = time.time()  # Update the last display change time
    elif game_state == "settings":
        volume_up_rect, volume_down_rect, back_rect = draw_settings()
        if time.time() - last_display_change_time > cooldown_period:  # Check cooldown period
            if volume_up_rect.collidepoint(mouse_pos) and mouse_click[0]:
                current_volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(min(current_volume + 0.1, 1.0))
            elif volume_down_rect.collidepoint(mouse_pos) and mouse_click[0]:
                current_volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(current_volume - 0.1, 0.0))
            elif back_rect.collidepoint(mouse_pos) and mouse_click[0]:
                game_state = "menu"
                last_display_change_time = time.time()  # Update the last display change time
    elif game_state == "info":
        back_rect = draw_info()
        if time.time() - last_display_change_time > cooldown_period:  # Check cooldown period
            if back_rect.collidepoint(mouse_pos) and mouse_click[0]:
                game_state = "playing"
                last_display_change_time = time.time()  # Update the last display change time

    clock.tick(60)  # limits FPS to 60

pygame.quit()