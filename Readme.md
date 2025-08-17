# Friday Legal DDoS Test Script

MIT License

## Açıklama
Bu Python scripti, **legal ve etik DDoS testi** yapmak için geliştirilmiştir.  
Sadece kendi kontrolünüzdeki sunucular veya izinli hedefler üzerinde çalıştırılmalıdır.  
Üçüncü taraflara zarar vermek için kullanılamaz.

## Özellikler
- Terminal tabanlı kontrol, GUI yok.
- URL/IP, port, toplam istek sayısı ve eşzamanlı istek sayısını ayarlayabilme.
- GET ve POST istekleri ile test yapabilme, POST payload opsiyonel.
- Çoklu çekirdek kullanımı ve eşzamanlı asenkron istekler (`asyncio + aiohttp + multiprocessing`).
- Terminalde canlı istatistik: tamamlanan istek sayısı, ortalama/min/max süre, CPU ve RAM kullanımı.
- Test sonrası CSV log dosyası oluşturma.

## Kurulum
1. Python 3.8 veya üstünü kurun.
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install aiohttp psutil
