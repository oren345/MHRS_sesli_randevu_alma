import speech_recognition as sr
import time
from playsound import playsound
from gtts import gTTS
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

r = sr.Recognizer()
mic = sr.Microphone()
#karşılama ve komut alma fonksiyonu
def mic_to_text():
    text = ''
    with mic as m:
        text_to_speak("merhaba hoşgeldiniz")
        audio = r.listen(m)
        try:
            text = r.recognize_google(audio,language='tr-TR')
        except sr.UnknownValueError:
            text_to_speak("seni anlayamadım")
    return text
#yazıyı ses çevirme fonksiyonu
def text_to_speak(veri):
    tts = gTTS(veri,lang='tr')
    rand = random.randint(1,100000)
    file = "audio-"+str(rand)+".mp3"
    tts.save(file)
    playsound(file)
    os.remove(file)
#sesi yazıya çevirme fonksiyonu
def mic_to_ses():
    text = ''
    with mic as m:
        r.adjust_for_ambient_noise(m)
        audio = r.listen(m)
        text = r.recognize_google(audio,language='tr-TR')
        print(text)
    return text

def rand():

    class Mhrs:
        def __init__(self):
            #tarayıcıyı açıyor.
            self.browser = webdriver.Firefox()
            #tarayıcıda verilen adrese gidiyor.
            self.browser.get("https://www.mhrs.gov.tr/vatandas/#/")
        def login(self):
            try: 
                text_to_speak("tc kimlik numaranızı söyleyiniz.")#yazıyı sese çevirerek bilgisayarın konuşmasını sağlıyor.
                tc_ses = mic_to_ses().lower()#mic_to_ses fonk ile sesi alıp yazıya çeviriyor. lower() ise yazıdaki harflerin hepsinin küçük olmasına yarıyor.
                tc = self.browser.find_element_by_xpath("//*[@id='LoginForm_username']")#find_element_by_xpath metodu ile ögenin xpath'inden ögeyi bulup değişkene atıyor.
                tc.send_keys(tc_ses)#send_keys metodu ile metodun parametresini tc değişkenine yazıyor.
                sifre = self.browser.find_element_by_xpath("//*[@id='LoginForm_password']")#find_element_by_xpath metodu ile ögenin xpath'inden ögeyi bulup değişkene atıyor.
                text_to_speak("şifrenizi giriniz")#yazıyı sese çevirerek bilgisayarın konuşmasını sağlıyor.
                sifre.click()#sifre değikenindeki ögeye tıklıyor.
                sifre.send_keys('')#sifre değişkenindeki ögeye klavyeden giriş yapılmasını sağlıyor.
                #sifre değişkeni de sesli sistem ile alınabilirdi ancak güvenlik sebebiyle klavyeden alınıyor.
                #sifre_ses = mic_to_ses().lower()
                #sifre = self.browser.find_element_by_xpath("//*[@id='LoginForm_password']").send_keys(sifre_ses)
                time.sleep(5)#giriş yapılırken sistemin verilen parametre kadar saniye cinsinden beklemesini sağlar.
                gir = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/div[2]/div[1]/div[2]/form/div[3]/div/div/span/div/div/button")
                gir.click()
                time.sleep(10)
                self.browser.find_element_by_class_name("hasta-randevu-card").click()#find_element_by_class_name fonk ile sınıf isminden ögeyi buluyor ve click() fonk ile tıklıyor.

            except:
                time.sleep(3)
                text_to_speak("Tc numaranızı veya şifrenizi yanlış söylediniz lütfen kontrol ediniz")
                self.browser.find_element_by_css_selector(".ant-btn-primary").click()#find_element_by_css_selector fonk ile css seçicisinden ögeyi buluyor ve click() fonk ile tıklıyor.
                text_to_speak("tc kimlik numaranızı tekrar söyleyiniz")
                tc_ses_2 = mic_to_ses().lower()
                tc.clear()#ögeyi temizliyor. içindekileri siliyor.
                tc.send_keys(tc_ses_2)
                time.sleep(1)
                sifre.clear()
                sifre.click()
                text_to_speak("şifrenizi tekrar giriniz")
                sifre.send_keys('')
                time.sleep(5)
                gir.click()
                time.sleep(5)
                self.browser.find_element_by_class_name("hasta-randevu-card").click()  
     
            time.sleep(3)
            ara_tip = self.browser.find_element_by_class_name("genel-arama-button")
            ara_tip.click()
            time.sleep(3)

        def bilgi(self):
            try:
                time.sleep(5)
                il = self.browser.find_element_by_class_name("ant-select-selection__rendered").click()
                text_to_speak("randevu almak istediğiniz ili söyleyiniz")
                il_ses = mic_to_ses().lower()
                time.sleep(1)
                il_gir = self.browser.find_element_by_xpath("//*[@id='rc-tree-select-list_1']/span/span/input")
                il_gir.clear()
                il_gir.send_keys(il_ses)
                time.sleep(1)
                il_tikla = self.browser.find_element_by_class_name("ant-select-tree")
                il_tikla.click()

            except:
                text_to_speak("bu isimde bir il bulunamadı lütfen tekrar söyleyiniz")
                il_gir.clear()
                il_gir.click()
                il_ses_1 = mic_to_ses().lower()
                il_gir.send_keys(il_ses_1)
                time.sleep(1)
                il_tikla = self.browser.find_element_by_class_name("ant-select-tree")
                il_tikla.click()
             
            try:
                ilce = self.browser.find_element_by_xpath("//*[@id='randevuAramaForm_ilce']/div/div/div[1]")
                text_to_speak("randevu almak istediğiniz ilçeyi söyleyiniz")
                ilce_ses = mic_to_ses().lower()
                time.sleep(1)
                ilce.click()
                ilce_gir = self.browser.find_element_by_class_name("ant-select-search__field")
                ilce_gir.clear()
                ilce_gir.send_keys(ilce_ses)
                time.sleep(1)
                ilce_tikla = self.browser.find_element_by_class_name("ant-select-dropdown-menu")
                ilce_tikla.click()

            except:
                text_to_speak("bu isimde bir ilçe bulunamadı lütfen tekrar söyleyiniz")
                ilce_gir.clear()
                ilce_gir.click()
                ilce_ses_1 = mic_to_ses().lower()
                ilce_gir.send_keys(ilce_ses_1)
                time.sleep(1)
                ilce_tikla = self.browser.find_element_by_class_name("ant-select-dropdown-menu")
                ilce_tikla.click()

            try:
                #klinik inputunu buluyor.
                klinik = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div/div[2]/div[2]/form/div[3]/div/div/span/span/span/span[2]")
                text_to_speak("randevu almak istediğiniz kliniği söyleyiniz")
                klinik.click()
                klinik_ses = mic_to_ses().lower()
                time.sleep(1)
                klinik_gir = self.browser.find_element_by_xpath("//*[@id='rc-tree-select-list_2']/span/span/input")
                klinik_gir.clear()
                klinik_gir.send_keys(klinik_ses)
                time.sleep(1)    
                klinik_tikla = self.browser.find_element_by_xpath("//*[@id='rc-tree-select-list_2']/ul") 
                klinik_tikla.click()

            except:
                text_to_speak("bu isimde bir klinik bulunamadı lütfen tekrar söyleyiniz")
                klinik_gir.clear()
                klinik_ses_1 = mic_to_ses().lower()
                klinik_gir.send_keys(klinik_ses_1)
                time.sleep(1)
                klinik_tikla = self.browser.find_element_by_xpath("//*[@id='rc-tree-select-list_2']/ul")
                klinik_tikla.click()

            try:
                #hastane inputunu buluyor.
                hastane = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div/div[2]/div[2]/form/div[4]/div/div/span/span/span/span/span[1]/span")
                text_to_speak("randevu almak istediğiniz hastaneyi söyleyiniz")
                hastane.click()
                hastane_ses = mic_to_ses().lower()
                time.sleep(1)
                hastane_gir = self.browser.find_element_by_xpath("//*[@id='rc-tree-select-list_3']/span/span/input")
                hastane_gir.clear()
                hastane_gir.send_keys(hastane_ses)
                time.sleep(1)    
                hastane_tikla = self.browser.find_element_by_xpath("//*[@id='rc-tree-select-list_3']/ul") 
                hastane_tikla.click()

            except:
                text_to_speak("bu isimde bir hastane bulunamadı lütfen tekrar söyleyiniz")
                hastane_gir.clear()
                hastane_ses_1 = mic_to_ses().lower()
                hastane_gir.send_keys(hastane_ses_1)
                time.sleep(1)
                hastane_tikla = self.browser.find_element_by_xpath("//*[@id='rc-tree-select-list_3']/ul")
                hastane_tikla.click()      

            try:
                #hekim inputunu buluyor.
                hekim = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div/div[2]/div[2]/form/div[7]/div/div/span/span")
                text_to_speak("randevu almak istediğiniz hekimi söyleyiniz")
                hekim.click()
                hekim_ses = mic_to_ses().lower()
                time.sleep(1)
                hekim_gir = self.browser.find_element_by_xpath("//*[@id='rc-tree-select-list_6']/span/span/input")
                hekim_gir.clear()
                hekim_gir.send_keys(hekim_ses)
                time.sleep(1)    
                hekim_tikla = self.browser.find_element_by_xpath("//*[@id='rc-tree-select-list_6']/ul") 
                hekim_tikla.click()

            except:
                text_to_speak("bu isimde bir hekim bulunamadı lütfen tekrar söyleyiniz")
                hekim_gir.clear()
                hekim_ses_1 = mic_to_ses().lower()
                hekim_gir.send_keys(hekim_ses_1)
                time.sleep(1)
                hekim_tikla = self.browser.find_element_by_xpath("//*[@id='rc-tree-select-list_6']/ul")
                hekim_tikla.click()
    
            #randevu ara butonunu buluyor.
            rand_ara = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div/div[2]/div[2]/form/div[9]/div/div/span/div/div[1]/button")
            #randevu ara butonuna tıklıyor.
            rand_ara.click()
            time.sleep(2)

        def cevap(self):
            tar = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div/ul/li[1]/div/div[2]/span/strong/span").text
            pol = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div/ul/li[1]/div/div[5]").text
            text_to_speak("randevu için en erken tarih"+tar+"ve poliklinik"+pol+",onaylıyor musunuz")
            cvp = mic_to_ses().lower()
            if "evet" in cvp:
                a = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div/ul")
                a.click() 
            elif "hayır" in cvp:
                b = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[1]/div/div/div/div")
                b.click()
                mhrs.bilgi()
                mhrs.cevap()
            
     
        def zaman(self):
        #randevu saatini buluyor.
        #--------------------------------------------------------09:00 RANDEVU---------------------------------------------------------------------------
            try:
                listeler = []#listeler isimli bir liste oluşturuyor. 
                time.sleep(5)
                labels = self.browser.find_elements_by_css_selector("div[tabindex='-1']")#find_element_by_css_selector fonk ile istenilen ögeleri buluyor ve değişkene atıyor.
                for label in labels:#labels değişkeninin uzunluğu kadar devam eden döngü
                    liste = label.text#bulunan ögelerin içerisinde yazılı olan textleri liste değişkenine atıyor.
                    listeler.append(liste)#liste değişkenini listeler isimli listeye ekliyor.
                z = []#tekrar liste oluşturuyor.
                z = listeler[4:]  #aynı css seçiciye sahip 4 tane daha eleman old. için onları eliyor. yani listenin 4. elemanından sonrakileri alıyor.         
                yok_saat = ",".join(z)#liste elemanlarının join()fonk. ile birleştirerek aralarına virgül ekliyor ve değişkene atıyor.
                time.sleep(2)
                text_to_speak("randevu için"+yok_saat+"saati doludur")
            except:
                text_to_speak("randevu için tüm saatler boştur.")

            text_to_speak("randevu almak istediğiniz saati söyleyiniz")
            saat = mic_to_ses().lower()
            time.sleep(2)
    
            if '9' in saat:
                rand_saat = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div[1]")
                rand_saat.click()
                time.sleep(2)
                try:
                    listeler_dk = []
                    time.sleep(5)
                    labels_dk = self.browser.find_elements_by_css_selector("button[disabled='']")
                    for label_dk in labels_dk:
                        liste_dk = label_dk.text
                        listeler_dk.append(liste_dk)
                    z = []
                    z = listeler_dk[1:]           
                    yok_dk = ",".join(z)
                    time.sleep(2)
                    text_to_speak("randevu için"+yok_dk+"dakikası doludur")
                except:
                    text_to_speak("randevu için tüm dakikalar boştur.")

                text_to_speak("randevu almak istediğiniz dakikayı söyleyiniz")
                dakika = mic_to_ses().lower()
                time.sleep(2)
                #09:00 İÇİN
                if '00' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div/button[1]")
                    rand_dk.click()
                    time.sleep(2)

                #09:10 İÇİN
                elif '10' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div/button[2]")
                    rand_dk.click()
                    time.sleep(2)

                #09:20 İÇİN
                elif '20' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div/button[3]")
                    rand_dk.click()
                    time.sleep(2)

                #09:30 İÇİN
                elif '30' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div/button[4]")
                    rand_dk.click()
                    time.sleep(2)

                #09:40 İÇİN
                elif '40' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div/button[5]")
                    rand_dk.click()
                    time.sleep(2)

                #09:50 İÇİN
                elif '50' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div/button[6]")
                    rand_dk.click()
                    time.sleep(2)
    #-----------------------------------------------------09:50'YE KADAR OLAN RANDEVU--------------------------------------------------------------

    #-------------------------------------------------------------10:00 RANDEVU------------------------------------------------------------------
            
            elif '10' in saat:
                rand_saat = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[2]/div")
                rand_saat.click()
                time.sleep(2)

                try:
                    listeler_dk = []
                    time.sleep(5)
                    labels_dk = self.browser.find_elements_by_css_selector("button[disabled='']")
                    for label_dk in labels_dk:
                        liste_dk = label_dk.text
                        listeler_dk.append(liste_dk)
                    z = []
                    z = listeler_dk[1:]           
                    yok_dk = ",".join(z)
                    time.sleep(5)
                    text_to_speak("randevu için"+yok_dk+"dakikası doludur")
                except:
                    text_to_speak("randevu için tüm dakikalar boştur.")


                #randevu dakikasını buluyor.
                text_to_speak("randevu almak istediğiniz dakikayı söyleyiniz")
                dakika = mic_to_ses().lower()
                time.sleep(2)
                #10:00 İÇİN

                if '00' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[2]/div[2]/div/button[1]")
                    rand_dk.click()
                    time.sleep(2)

                #10:10 İÇİN
                elif '10' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[2]/div[2]/div/button[2]")
                    rand_dk.click()
                    time.sleep(2)

                #10:20 İÇİN
                elif '20' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[2]/div[2]/div/button[3]")
                    rand_dk.click() 
                    time.sleep(2)

                #10:30 İÇİN
                elif '30' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[2]/div[2]/div/button[4]")
                    rand_dk.click()
                    time.sleep(2)

                #10:40 İÇİN
                elif '40' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[2]/div[2]/div/button[5]")
                    rand_dk.click()
                    time.sleep(2)

                #10:50 İÇİN
                elif '50' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[2]/div[2]/div/button[6]")
                    rand_dk.click()
                    time.sleep(2)
    #-----------------------------------------------------10:50'YE KADAR OLAN RANDEVU----------------------------------------------------------------

    #-----------------------------------------------------------11:00 RANDEVU------------------------------------------------------------------------
    
            elif '11' in saat:
                rand_saat = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[3]/div")
                rand_saat.click()
                time.sleep(2)

                try:
                    listeler_dk = []
                    time.sleep(5)
                    labels_dk = self.browser.find_elements_by_css_selector("button[disabled='']")
                    for label_dk in labels_dk:
                        liste_dk = label_dk.text
                        listeler_dk.append(liste_dk)
                    z = []
                    z = listeler_dk[1:]           
                    yok_dk = ",".join(z)
                    time.sleep(5)                    
                    text_to_speak("randevu için"+yok_dk+"dakikası doludur")
                except:
                    text_to_speak("randevu için tüm dakikalar boştur.")


                #randevu dakikasını buluyor.
                text_to_speak("randevu almak istediğiniz dakikayı söyleyiniz")
                dakika = mic_to_ses().lower()
                time.sleep(2)
                #11:00 İÇİN
                if '00' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[3]/div[2]/div/button[1]")
                    rand_dk.click()
                    time.sleep(2)

                #11:10 İÇİN
                elif '10' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[3]/div[2]/div/button[2]")
                    rand_dk.click() 
                    time.sleep(2)

                #11:20 İÇİN
                elif '20' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[3]/div[2]/div/button[3]")
                    rand_dk.click()
                    time.sleep(2)

                #11:30 İÇİN
                elif '30' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[3]/div[2]/div/button[4]")
                    rand_dk.click()
                    time.sleep(2)

                #11:40 İÇİN
                elif '40' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[3]/div[2]/div/button[5]")
                    rand_dk.click()
                    time.sleep(2)

                #11:50 İÇİN
                elif '50' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[3]/div[2]/div/button[6]")
                    rand_dk.click()
                    time.sleep(2)
    #-----------------------------------------------------11:50'YE KADAR OLAN RANDEVU-----------------------------------------------------------------

    #-------------------------------------------------------------13:00 RANDEVU------------------------------------------------------------------
            elif '13' in saat:    
                rand_saat = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[4]/div[1]")
                rand_saat.click() 
                time.sleep(2)

                try:
                    listeler_dk = []
                    time.sleep(5)
                    labels_dk = self.browser.find_elements_by_css_selector("button[disabled='']")
                    for label_dk in labels_dk:
                        liste_dk = label_dk.text
                        listeler_dk.append(liste_dk)
                    z = []
                    z = listeler_dk[1:]           
                    yok_dk = ",".join(z)
                    time.sleep(5)                    
                    text_to_speak("randevu için"+yok_dk+"dakikası doludur")
                except:
                    text_to_speak("randevu için tüm dakikalar boştur.")


                #randevu dakikasını buluyor.
                text_to_speak("randevu almak istediğiniz dakikayı söyleyiniz")
                dakika = mic_to_ses().lower()
                time.sleep(2)


                #13:30 İÇİN
                if '30' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/div/button[1]")
                    rand_dk.click()
                    time.sleep(2)

                #13:40 İÇİN
                elif '40' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/div/button[2]")
                    rand_dk.click()
                    time.sleep(2)

                #13:50 İÇİN
                elif '50' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/div/button[3]")
                    rand_dk.click()
                    time.sleep(2)
    #-----------------------------------------------------13:50'YE KADAR OLAN RANDEVU----------------------------------------------------------------

    #-------------------------------------------------------------14:00 RANDEVU------------------------------------------------------------------
            elif '14' in saat:  
                rand_saat = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[5]/div")
                rand_saat.click() 
                time.sleep(2)

                try:
                    listeler_dk = []
                    time.sleep(5)
                    labels_dk = self.browser.find_elements_by_css_selector("button[disabled='']")
                    for label_dk in labels_dk:
                        liste_dk = label_dk.text
                        listeler_dk.append(liste_dk)
                    z = []
                    z = listeler_dk[1:]           
                    yok_dk = ",".join(z)
                    time.sleep(5)
                    text_to_speak("randevu için"+yok_dk+"dakikası doludur")
                except:
                    text_to_speak("randevu için tüm dakikalar boştur.")


                #randevu dakikasını buluyor.
                text_to_speak("randevu almak istediğiniz dakikayı söyleyiniz")
                dakika = mic_to_ses().lower()
                time.sleep(2)
                #14:00 İÇİN
                if '00' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[5]/div[2]/div/button[1]")
                    rand_dk.click()
                    time.sleep(2)

                #14:10 İÇİN
                elif '10' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[5]/div[2]/div/button[2]")
                    rand_dk.click()
                    time.sleep(2)

                #14:20 İÇİN
                elif '20' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[5]/div[2]/div/button[3]")
                    rand_dk.click()
                    time.sleep(2)

                #14:30 İÇİN
                elif '30' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[5]/div[2]/div/button[4]")
                    rand_dk.click()
                    time.sleep(2)

                #14:40 İÇİN
                elif '40' in dakika:   
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[5]/div[2]/div/button[5]")
                    rand_dk.click()
                    time.sleep(2)

                #14:50 İÇİN
                elif '50' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[5]/div[2]/div/button[6]")
                    rand_dk.click()
                    time.sleep(2)
    #-----------------------------------------------------14:50'YE KADAR OLAN RANDEVU----------------------------------------------------------------

    #-------------------------------------------------------------15:00 RANDEVU------------------------------------------------------------------
            elif '15' in saat:    
                rand_saat = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[6]/div[1]")
                rand_saat.click()
                time.sleep(2)

                try:
                    listeler_dk = []
                    time.sleep(5)
                    labels_dk = self.browser.find_elements_by_css_selector("button[disabled='']")
                    for label_dk in labels_dk:
                        liste_dk = label_dk.text
                        listeler_dk.append(liste_dk)
                    z = []
                    z = listeler_dk[1:]           
                    yok_dk = ",".join(z)
                    time.sleep(5)                    
                    text_to_speak("randevu için"+yok_dk+"dakikası doludur")
                except:
                    text_to_speak("randevu için tüm dakikalar boştur.")


                #randevu dakikasını buluyor.
                text_to_speak("randevu almak istediğiniz dakikayı söyleyiniz")
                dakika = mic_to_ses().lower()
                time.sleep(2)
                #15:00 İÇİN
                if '00' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[6]/div[2]/div/button[1]")
                    rand_dk.click()
                    time.sleep(2)

                #15:10 İÇİN
                elif '10' in dakika:
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[6]/div[2]/div/button[2]")
                    rand_dk.click()
                    time.sleep(2)

                #15:20 İÇİN
                elif '20' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[6]/div[2]/div/button[3]")
                    rand_dk.click()
                    time.sleep(2)

                #15:30 İÇİN
                elif '30' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[6]/div[2]/div/button[4]")
                    rand_dk.click()
                    time.sleep(2)

                #15:40 İÇİN
                elif '40' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[6]/div[2]/div/button[5]")
                    rand_dk.click() 
                    time.sleep(2)

                #15:50 İÇİN
                elif '50' in dakika:    
                    rand_dk = self.browser.find_element_by_xpath("//*[@id='vatandasApp']/section/main/div/div/div[2]/div/div[3]/div[2]/div[3]/div[3]/div/div[2]/div/div/div[6]/div[2]/div/button[6]")
                    rand_dk.click()
                    time.sleep(2)
    #-----------------------------------------------------15:50'YE KADAR OLAN RANDEVU----------------------------------------------------------------
        def onay(self):
            zmn = self.browser.find_element_by_css_selector("tr.ant-descriptions-row:nth-child(1) > td:nth-child(2) > span:nth-child(1) > strong:nth-child(1)").text
            hast = self.browser.find_element_by_css_selector("tr.ant-descriptions-row:nth-child(3) > td:nth-child(2)").text
            pol = self.browser.find_element_by_css_selector("tr.ant-descriptions-row:nth-child(4) > td:nth-child(2) > span:nth-child(1) > strong:nth-child(1)").text
            hek = self.browser.find_element_by_css_selector("tr.ant-descriptions-row:nth-child(5) > td:nth-child(2)").text
            mua = self.browser.find_element_by_css_selector("tr.ant-descriptions-row:nth-child(6) > td:nth-child(2)").text
            kisi = self.browser.find_element_by_css_selector("tr.ant-descriptions-row:nth-child(8) > td:nth-child(2)").text

            text_to_speak("randevu tarihiniz"+zmn+"hastane"+hast+"poliklinik"+pol+"doktorunuz"+hek+"muayene yeriniz"+mua+"ve randevu alınan kişi"+kisi+"onaylıyor musunuz")
            ynt = mic_to_ses().lower()

            if "evet" in ynt:
                onay = self.browser.find_element_by_css_selector(".ant-modal-footer > div:nth-child(1) > button:nth-child(2)")
                onay.click()
                time.sleep(2)
                text_to_speak("randevunuz başarıyla oluşturulmuştur")
                son = self.browser.find_element_by_css_selector(".ant-modal-confirm-btns > button:nth-child(1)")
                son.click()
                text_to_speak("tarayıcınız kapatılıyor")
                cikis = self.browser.find_element_by_css_selector("button.workspace-buttons:nth-child(4)").click
                self.browser.close()#browser'ı kapatıyor.
            elif "hayır" in ynt:
                red = self.browser.find_element_by_css_selector(".anticon-close > svg:nth-child(1)")
                red.click()
                time.sleep(2)
                text_to_speak("tekrar randevu oluşturmak ister misiniz")
                ses = mic_to_ses().lower()
                if "evet" in ses:
                    yeni = self.browser.find_element_by_css_selector(".ant-page-header-back-button").click()
                    yeni_bir = self.browser.find_element_by_css_selector(".ant-page-header-back-button").click()
                    time.sleep(2)
                    mhrs.bilgi()
                    mhrs.cevap()
                    mhrs.zaman()
                    mhrs.onay()
                elif "hayır" in ses:
                    text_to_speak("uygulama kapatılıyor")
                    cikis = self.browser.find_element_by_css_selector("button.workspace-buttons:nth-child(4)").click
                    self.browser.close()
  
             

    mhrs = Mhrs()
    mhrs.login()
    mhrs.bilgi()
    mhrs.cevap()
    mhrs.zaman()
    mhrs.onay()


#en başta çalışan yer
while True:
    text = mic_to_text().lower()
    if "randevu" in text:
        if "al" in text:
            text_to_speak("MHRS sayfası açılıyor")
            rand()
    elif "uygulamadan çık" in text:
        text_to_speak("uygulama kapatılıyor")
        break
    else:
        pass
