import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien
from alien_bullet import Alien_Bullet

"""Respond to keypresses."""
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


"""Respond to key releases."""
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


"""Respond to keypresses and mouse events."""
def check_events(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if activity_manager.show_data:
                activity_manager.show_performance_data()
                
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        set_game(ai_settings, aliens, alien_bullets, bullets, sb, screen, ship, stats)

def set_game(ai_settings, aliens, alien_bullets, bullets, sb, screen, ship, stats):
    if not stats.game_active:
        
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        if sb != None:
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()
        
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

"""Fire a bullet, if limit not reached yet."""
def fire_bullet(ai_settings, screen, ship, bullets):
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


"""Fire a bullet from a random alien, if limit not yet reached."""
def fire_alien_bullets(ai_settings, screen, aliens, alien_bullets):
    if len(alien_bullets) < ai_settings.bullets_allowed:
        new_alien_bullet = Alien_Bullet(ai_settings, screen, aliens)
        alien_bullets.add(new_alien_bullet)


"""Update images on the screen, and flip to the new screen."""
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_alien_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    if sb != None:
        sb.show_score()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


"""Update position of bullets, and get rid of old bullets."""
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager):
    # Update ship bullet positions.
    bullets.update()

    # Update Alien bullet positions.
    alien_bullets.update()

    # Get rid of ship bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.top <= 0:
            bullets.remove(bullet)
    
    # Get rid of Alien bullets that have gone offscreen
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.top >= 1000:
            alien_bullets.remove(alien_bullet)
    
    # Check for ship collisions with alien bullets.
    check_ship_alien_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager)
    check_ship_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


"""Check to see if there's a new high score."""
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        if sb != None:
            sb.prep_high_score()


"""Respond to bullet-alien collisions."""
def check_ship_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            if sb != None:
                sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        if sb != None:
            sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


"""Respond to ship-alien_bullet collisions."""
def check_ship_alien_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager):
    collision = pygame.sprite.spritecollideany(ship, alien_bullets)
    if collision != None:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager)


"""Respond appropriately if any aliens have reached an edge."""
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        

"""Drop the entire fleet, and change the fleet's direction."""
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    
    ai_settings.fleet_direction *= -1
    aliens.update()


"""Respond to ship being hit by alien."""
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager):
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        if sb != None:
            sb.prep_ships()

    else:
        activity_manager.finish_epoch(stats.score)
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    alien_bullets.empty()

    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Pause.
    sleep(0.5)

"""Check if any aliens have reached the bottom of the screen."""
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager)
            break

"""Check if the fleet is at an edge, then update the postions of all aliens in the fleet."""
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager):
    check_fleet_edges(ai_settings, aliens)
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager)


"""Determine the number of aliens that fit in a row."""
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

"""Determine the number of rows of aliens that fit on the screen."""
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - (1* alien_height) - ship_height
    number_rows = int(available_space_y/2 / (2 * alien_height))
    return number_rows


"""Create an alien, and place it in the row."""
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


"""Create a full fleet of aliens."""
def create_fleet(ai_settings, screen, ship, aliens):
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # storing the number of aliens for iteration updates
    ai_settings.num_alien_x= number_aliens_x
    ai_settings.num_alien_y= number_rows

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

