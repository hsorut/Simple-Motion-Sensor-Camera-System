import cv2
import time
import datetime


MIN_ALAN = 5000  
KAMERA_INDEKSI = 0 
BEKLEME_SURESI = 1.0 

print("Hareket Algılayıcı Başlatılıyor...")

kamera = cv2.VideoCapture(KAMERA_INDEKSI)
if not kamera.isOpened():
    print("HATA: Kamera başlatılamadı.")
    print("Kameranın bağlı olduğundan ve raspi-config'den etkinleştirildiğinden emin olun.")
    exit()

print("Kamera hazır. Arka plan için ilk kare alınıyor...")

time.sleep(2) 
basari, arka_plan = kamera.read()

if not basari:
    print("HATA: Kameradan kare okunamadı.")
    kamera.release()
    exit()

# Arka planı griye çevir ve bulanıklaştır
arka_plan_gri = cv2.cvtColor(arka_plan, cv2.COLOR_BGR2GRAY)
arka_plan_gri = cv2.GaussianBlur(arka_plan_gri, (21, 21), 0)

print("Sistem hazır. Hareket bekleniyor... (Çıkış için CTRL+C)")

son_kayit_zamani = 0

try:
    while True:
       
        basari, kare = kamera.read()
        if not basari:
            break 

        
        kare_gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
        kare_gri = cv2.GaussianBlur(kare_gri, (21, 21), 0)

        
        fark_kare = cv2.absdiff(arka_plan_gri, kare_gri)

     
        _, esik_kare = cv2.threshold(fark_kare, 25, 255, cv2.THRESH_BINARY)

        
        esik_kare = cv2.dilate(esik_kare, None, iterations=2)

       
        konturlar, _ = cv2.findContours(esik_kare.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        hareket_algilandi = False

        
        for kontur in konturlar:
           
            if cv2.contourArea(kontur) < MIN_ALAN:
                continue
            
            # Minimum alanı aşan bir kontur bulduk, demek ki hareket var
            hareket_algilandi = True
            break 

        
        su_anki_zaman = time.time()
        if hareket_algilandi and (su_anki_zaman - son_kayit_zamani > BEKLEME_SURESI):
            
            
            simdi = datetime.datetime.now()
            dosya_adi = simdi.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
            
            
            cv2.imwrite(dosya_adi, kare)
            
            print(f"HAREKET ALGILANDI! Fotoğraf kaydedildi: {dosya_adi}")
            
            
            son_kayit_zamani = su_anki_zaman
            
           

        # İsteğe bağlı Görüntüyü ekranda göstermek için:
        cv2.imshow("Kamera Akisi", kare)
        cv2.imshow("Eşiklenmiş Fark", esik_kare)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

except KeyboardInterrupt:
    print("\nProgram kullanıcı tarafından sonlandırıldı.")
finally:
    
    print("Kamera kapatılıyor.")
    kamera.release()
    # cv2.destroyAllWindows() # (Eğer imshow kullanıyorsanız)