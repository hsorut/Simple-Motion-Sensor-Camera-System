# Basit Hareket Algılayıcı Kamera Sistemi (Raspberry Pi)

Bu proje, bir Raspberry Pi ve kamera modülü kullanarak, kameranın görüş alanında bir hareket algılandığında otomatik olarak fotoğraf çeken bir güvenlik sistemi altyapısıdır.

Proje, Python ve OpenCV [cite: 38] kütüphanesi kullanarak çalışır. Temel mantığı, iki video karesi arasındaki farkı analiz etmektir.

# Donanım Gereksinimleri

* Raspberry Pi (Zero W, 3, 4 vb.) 
* Pi Kamera Modülü (veya USB Web Kamerası) 
* SD Kart (Raspberry Pi OS yüklü)
* Güç Kaynağı

# Yazılım Gereksinimleri

* **Python 3**
* **Python Kütüphaneleri:**
* `opencv-python` (veya headless sürümü)
* `numpy` (OpenCV'nin bir bağımlılığıdır)



# Kurulum ve Hazırlık

## FAZ 1: Bilgisayar Hazırlığı 

1.  **Raspberry Pi OS'i Hazırla:**
    * Raspberry Pi OS'in en güncel sürümünü SD karta kurun.
    * `sudo apt update && sudo apt upgrade` komutları ile sistemi güncelleyin.

2.  **Kamerayı Etkinleştir (Pi Kamera kullanıyorsanız):**
    * Terminali açın ve `sudo raspi-config` komutunu çalıştırın.
    * **Interface Options** (Arayüz Seçenekleri) menüsüne gidin.
    * **Camera** seçeneğini bulun, "Enable" (Etkinleştir) yapın ve Pi'yi yeniden başlatın.

3.  **Gerekli Python Kütüphanelerini Yükle (Kritik Adım):**
    * Pi üzerindeki Terminal'i açın.
    * Şu komutları çalıştırın (OpenCV'nin `headless` sürümü, Pi Zero gibi cihazlarda grafik arayüzü olmadan çalışmak için daha iyidir):
    ```sh
    pip install opencv-python-headless numpy
    ```
    * **Neden?** `opencv-python` kütüphanesi, Python'un kameradan görüntü almasını , görüntüleri işlemesini (griye çevirme, fark alma) ve kaydetmesini  sağlar.

## FAZ 2: Devre Kurulumu 

1.  **Pi Kamerayı Bağla:**
    * Raspberry Pi kapalıyken (güçten çekilmişken) kamera şerit kablosunu Pi üzerindeki "CAMERA" yazan porta takın.
    * Kablonun mavi tarafının USB/Ethernet portlarına doğru bakması gerekir (Pi 4'te). Yönü modelinize göre değişebilir, dikkatlice takın ve kilidi kapatın.

2.  **USB Kamera (Alternatif):**
    * Bir USB web kamerası kullanıyorsanız, `hareket_algilayici.py` dosyasındaki `KAMERA_INDEKSI = 0` ayarı genellikle doğrudan çalışacaktır.

## FAZ 3: Python Betiğini Çalıştırma

1.  `hareket_algilayici.py` dosyasını Pi'nize kopyalayın.

2.  (İsteğe bağlı) `hareket_algilayici.py` dosyasını açıp `MIN_ALAN` ayarını değiştirerek hassasiyeti ayarlayabilirsiniz. Değer ne kadar yüksek olursa, algılanması için o kadar büyük bir hareket gerekir.

3.  Terminali açın ve `cd` komutu ile `hareket_algilayici.py` dosyasının bulunduğu klasörün içine gidin.

4.  Şu komutu yazarak programı başlatın:
    ```sh
    python hareket_algilayici.py
    ```

## FAZ 4: Projeyi Test Etme

1.  Programı başlattıktan sonra, "Sistem hazır. Hareket bekleniyor..." mesajını göreceksiniz.
2.  Kameranın önünde elinizi sallayın veya hareket edin.
3.  Terminalde `HAREKET ALGILANDI! Fotoğraf kaydedildi: ...` mesajını görmelisiniz.
4.  Fotoğrafın, betiği çalıştırdığınız klasöre `2025-11-15_03-30-01.jpg` gibi bir isimle kaydedildiğini doğrulayın.