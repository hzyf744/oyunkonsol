import pygame
import sys
import random

# Pygame'in başlatılması
pygame.init()

# Oyun ekranı boyutları
WIDTH, HEIGHT = 800, 600

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Oyuncu (karakter) sınıfı
class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        pygame.draw.polygon(self.image, BLUE, [(0, 50), (25, 0), (50, 50)])  # Üçgen karakter
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.name = name
        self.score = 0
        self.speed = 8  # Oyuncu hareket hızı

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Mermi (ateş) sınıfı
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = player_rect.centerx
        self.rect.y = player_rect.top

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

# Engellerin sınıfı
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speed = speed  # Engel hareket hızı

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -50)

# Ekranın başlatılması
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Oyun")

# Oyuncu ve mermi gruplarının oluşturulması
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Kullanıcının oyuncu adını girmesi için input alanı
input_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 25)
input_font = pygame.font.Font(None, 36)
input_text = ""
input_active = True

# "Oyunu Başlat" tuşu
start_button_font = pygame.font.Font(None, 36)
start_button_text = start_button_font.render("Oyunu Başlat (ENTER)", True, WHITE)
start_button_rect = start_button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
start_button_active = False

# Oyuncu adı girme döngüsü
while input_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                input_active = False
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, input_rect, 2)
    pygame.draw.rect(screen, WHITE, start_button_rect, 2)
    screen.blit(input_font.render(input_text, True, WHITE), (input_rect.x + 5, input_rect.y + 5))
    screen.blit(start_button_text, start_button_rect)
    pygame.display.flip()

# Oyuncu nesnesinin oluşturulması
player = Player(input_text)
all_sprites.add(player)

# "Oyunu Başlat" tuşuna basma döngüsü
while not start_button_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            start_button_active = True

    screen.fill(BLACK)
    screen.blit(start_button_text, start_button_rect)
    pygame.display.flip()

# Oyuncu adını ekrana yazdırma
font = pygame.font.Font(None, 36)
label_text = font.render(f"Oyuncu: {player.name}", True, WHITE)
label_rect = label_text.get_rect(topleft=(10, 10))
screen.blit(label_text, label_rect)

# Oyuncu ve engel gruplarına eklenmesi
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Ana oyun döngüsü
running = True
clock = pygame.time.Clock()
firing = False  # Ateş etme durumu
fire_rate = 0   # Ateş hızını kontrol etmek için sayaç
obstacle_speed = player.speed / 2  # Engellerin başlangıç hareket hızı

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.rect.x -= player.speed
            elif event.key == pygame.K_d:
                player.rect.x += player.speed
            elif event.key == pygame.K_SPACE and start_button_active:  
                firing = True  # Ateş etme durumu

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                firing = False  # Ateş etme durumu kapatılır

    # Engellerin oluşturulması ve engel grubuna eklenmesi
    if random.randint(0, 100) < 5:
        obstacle = Obstacle(obstacle_speed)
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    # Oyuncu ve mermi gruplarının güncellenmesi
    all_sprites.update()

    # Oyunu kaybetme kontrolü
    if pygame.sprite.spritecollide(player, obstacles, False):
        # Oyunu kaybetme bildirimi
        font_game_over = pygame.font.Font(None, 48)
        game_over_text = font_game_over.render("Oyunu Kaybettiniz", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

        # Yeniden başlatma tuşu
        restart_button_font = pygame.font.Font(None, 36)
        restart_button_text = restart_button_font.render("Yeniden Başla (SPACE)", True, WHITE)
        restart_button_rect = restart_button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        # Yeniden başlatma döngüsü
        restart_button_active = False
        while not restart_button_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    restart_button_active = True
                    # Oyuncuyu tekrar oluştur ve oyunu sıfırla
                    player = Player(player.name)
                    all_sprites.add(player)
                    bullets.empty()
                    obstacles.empty()
                    obstacle_speed = player.speed / 2
                    player.rect.center = (WIDTH // 2, HEIGHT - 50)
                    firing = False
                    fire_rate = 0

            screen.fill(BLACK)
            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_button_text, restart_button_rect)
            pygame.display.flip()

    # Mermi ve engel çarpışmalarının kontrolü
    hits = pygame.sprite.groupcollide(bullets, obstacles, True, True)
    for hit in hits:
        player.score += 1

    # Skor bazlı hız kontrolü
    if player.score >= 100:
        obstacle_speed = player.speed
    elif player.score >= 300:
        obstacle_speed = player.speed * 1.5
    elif player.score >= 600:
        obstacle_speed = player.speed * 2

    # Ekranın temizlenmesi
    screen.fill(BLACK)

    # Yol çizimi
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 50, WIDTH, 50))

    # Oyuncu, mermi ve engellerin çizilmesi
    all_sprites.draw(screen)

    # Skorun ekrana yazdırılması
    score_text = font.render(f"Skor: {player.score}", True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    # Ateş etme işlevselliği
    fire_rate += 1
    if firing and fire_rate % 2 == 0:  # Her 10 frame'de bir ateş et
        bullet = Bullet(player.rect)
        all_sprites.add(bullet)
        bullets.add(bullet)

    # Ekranın güncellenmesi
    pygame.display.flip()

    # FPS (Frame Per Second) ayarı
    clock.tick(30)

pygame.quit()
sys.exit()