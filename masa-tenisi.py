import pygame
import sys
import random

# Pygame'yi başlat
pygame.init()

# Ekran ayarları
genislik, yukseklik = 800, 600
ekran = pygame.display.set_mode((genislik, yukseklik))
pygame.display.set_caption("Masa Tenisi Oyunu")

# Renkler
siyah = (0, 0, 0)
beyaz = (255, 255, 255)

# Font ve skor değişkenleri
font = pygame.font.Font(None, 36)
skor_oyuncu1 = 0
skor_oyuncu2 = 0

# Masa tenisi raketi sınıfı
class Raket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 100))
        self.image.fill(beyaz)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hiz = 5

    def hareket_et(self, yon):
        if yon == "YUKARI" and self.rect.top > 0:
            self.rect.y -= self.hiz
        if yon == "ASAGI" and self.rect.bottom < yukseklik:
            self.rect.y += self.hiz

# Masa tenisi topu sınıfı
class Top(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(beyaz)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hiz_x = 5 * random.choice([1, -1])
        self.hiz_y = 5 * random.choice([1, -1])

    def hareket_et(self):
        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y

        # Ekranın kenarlarına çarpınca yön değiştir
        if self.rect.left <= 0 or self.rect.right >= genislik:
            self.hiz_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= yukseklik:
            self.hiz_y *= -1

# Oyun başlangıç fonksiyonu
def oyun_baslangici():
    oyuncu1 = Raket(20, yukseklik // 2)
    oyuncu2 = Raket(genislik - 20, yukseklik // 2)
    top = Top(genislik // 2, yukseklik // 2)

    oyuncular = pygame.sprite.Group(oyuncu1, oyuncu2)
    top_grubu = pygame.sprite.Group(top)

    return oyuncular, top_grubu

# Oyun durumu ve skorları gösteren fonksiyon
def oyun_durumu_goster():
    skor_metni = font.render(f"{skor_oyuncu1} - {skor_oyuncu2}", True, beyaz)
    ekran.blit(skor_metni, (genislik // 2 - 30, 20))

# Oyun döngüsü
def oyun():
    global skor_oyuncu1, skor_oyuncu2

    oyuncular, top_grubu = oyun_baslangici()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            oyuncular.sprites()[0].hareket_et("YUKARI")
        if keys[pygame.K_s]:
            oyuncular.sprites()[0].hareket_et("ASAGI")
        if keys[pygame.K_UP]:
            oyuncular.sprites()[1].hareket_et("YUKARI")
        if keys[pygame.K_DOWN]:
            oyuncular.sprites()[1].hareket_et("ASAGI")

        # Topun hareketi
        top_grubu.sprites()[0].hareket_et()

        # Topun oyuncu raketleri ile çarpışması kontrolü
        if pygame.sprite.spritecollide(oyuncular.sprites()[0], top_grubu, False):
            top_grubu.sprites()[0].hiz_x *= -1
        if pygame.sprite.spritecollide(oyuncular.sprites()[1], top_grubu, False):
            top_grubu.sprites()[0].hiz_x *= -1

        # Top ekranın kenarlarına çarpınca skor güncelle
        if top_grubu.sprites()[0].rect.left <= 0:
            skor_oyuncu2 += 1
            oyuncular, top_grubu = oyun_baslangici()
        if top_grubu.sprites()[0].rect.right >= genislik:
            skor_oyuncu1 += 1
            oyuncular, top_grubu = oyun_baslangici()

        # Ekranı temizle
        ekran.fill(siyah)

        # Oyuncu raketlerini ve topu ekrana çiz
        oyuncular.draw(ekran)
        top_grubu.draw(ekran)

        # Oyun durumu ve skorları göster
        oyun_durumu_goster()

        # Ekranı güncelle
        pygame.display.flip()

        # FPS ayarı
        clock.tick(60)

if __name__ == "__main__":
    oyun()
