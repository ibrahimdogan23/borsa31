# Yatırım Metodolojisi: Teknik ve Kantitatif Analiz

*Kaynak Dosya: Yatırım Metodolojisi_ Teknik ve Kantitatif Analiz.pdf*

---

## Sayfa 1

Mühendislik
 
ve
 
Matematik
 
Temelli
 
Bütünleşik
 
Yatırım
 
Metodolojisi:
 
Amerikan
 
ve
 
BIST
 
Piyasalarında
 
Kantitatif
 
Yaklaşımlar
 
Modern
 
finansal
 
piyasalar,
 
rastgele
 
yürüyüş
 
hipotezi
 
ile
 
deterministik
 
yapılar
 
arasında
 
gidip
 
gelen
 
karmaşık
 
dinamik
 
sistemlerdir.
 
Bir
 
mühendis
 
ve
 
matematikçi
 
perspektifiyle,
 
bu
 
piyasalarda
 
sürdürülebilir
 
başarı
 
elde
 
etmek,
 
yalnızca
 
grafik
 
okumayı
 
değil,
 
aynı
 
zamanda
 
verinin
 
altındaki
 
istatistiksel
 
dağılımları,
 
fiyatın
 
oluşumuna
 
neden
 
olan
 
piyasa
 
psikolojisinin
 
mikro-mekaniğini
 
ve
 
modern
 
hesaplama
 
tekniklerini
 
harmanlamayı
 
gerektirir.
 
Bu
 
rapor,
 
Amerikan
 
borsaları
 
(NYSE,
 
NASDAQ)
 
ve
 
Borsa
 
İstanbul
 
(BIST)
 
özelinde,
 
klasik
 
teknik
 
analizden
 
yapay
 
zeka
 
tabanlı
 
tahmin
 
modellerine
 
kadar
 
geniş
 
bir
 
spektrumda
 
akademik
 
ve
 
uygulamalı
 
bir
 
metodoloji
 
sunmaktadır.
 
Klasik
 
ve
 
Modern
 
Teknik
 
Analiz:
 
Fiyatın
 
Mikro-Mekaniği
 
ve
 
Geometrisi
 
Teknik
 
analiz,
 
genellikle
 
geçmiş
 
fiyat
 
hareketlerinin
 
gelecekte
 
tekrarlanacağı
 
varsayımına
 
dayanan
 
bir
 
disiplin
 
olarak
 
görülse
 
de,
 
mühendislik
 
disiplini
 
perspektifinden
 
bu,
 
verinin
 
otokorelasyonu
 
ve
 
insan
 
psikolojisinin
 
yarattığı
 
döngüsel
 
geri
 
besleme
 
mekanizmalarının
 
incelenmesidir.
1
 
Fiyat
 
hareketi
 
(Price
 
Action),
 
bir
 
varlığın
 
arz
 
ve
 
talep
 
dengesindeki
 
değişimlerin
 
en
 
saf
 
haliyle
 
izlenmesi
 
olup,
 
herhangi
 
bir
 
gecikmeli
 
indikatöre
 
ihtiyaç
 
duymadan
 
piyasa
 
katılımcılarının
 
kolektif
 
niyetini
 
ortaya
 
koyar.
1
 
Fiyat
 
Hareketi
 
ve
 
Piyasa
 
Psikolojisinin
 
İlişkisi
 
Fiyat
 
hareketi
 
analizi,
 
piyasanın
 
bir
 
"rastgele
 
yürüyüş"
 
(random
 
walk)
 
olmadığını,
 
aksine
 
kurumsal
 
emir
 
akışları
 
ve
 
likidite
 
arayışı
 
tarafından
 
yönlendirilen
 
yapısal
 
bir
 
süreç
 
olduğunu
 
savunur.
3
 
Bu
 
sürecin
 
temel
 
yapı
 
taşları
 
destek/direnç
 
seviyeleri,
 
arz-talep
 
bölgeleri
 
ve
 
mum
 
çubuğu
 
formasyonlarıdır.
 
Destek
 
ve
 
direnç
 
seviyeleri,
 
sadece
 
geçmişte
 
fiyatın
 
döndüğü
 
çizgiler
 
değildir;
 
bu
 
seviyeler,
 
bekleyen
 
emirlerin
 
(resting
 
orders)
 
ve
 
stop
 
kümelerinin
 
(stop
 
clusters)
 
yoğunlaştığı
 
likidite
 
havuzlarıdır.
3
 
Bir
 
fiyat
 
seviyesi
 
geçmişte
 
güçlü
 
bir
 
talep
 
gördüyse,
 
piyasa
 
katılımcıları
 
o
 
seviyeyi
 
bir
 
"değer"
 
bölgesi
 
olarak
 
hatırlar
 
ve
 
fiyat
 
tekrar
 
oraya
 
geldiğinde
 
benzer
 
bir
 
tepki
 
verme
 
eğilimi
 
gösterir.
4
 
Arz
 
ve
 
talep
 
bölgeleri
 
ise
 
bu
 
kavramın
 
daha
 
geniş
 
bir
 
alan
 
üzerinde
 
tanımlanmış
 
halidir.
 
Özellikle
 
"likidite
 
boşlukları"
 
(liquidity
 
gaps)
 
veya
 
"adil
 
değer
 
boşlukları"
 
(fair
 
value
 
gaps),
 
fiyatın
 
bir
 
yöne
 
doğru
 
hızla
 
ivmelendiği
 
ve
 
karşıt
 
emirlerin
 
yeterince
 
karşılanamadığı
 
alanları
 
temsil
 
eder.
3
 
Bu
 
boşluklar,
 
piyasa
 
verimliliğini
 
sağlama
 
amacıyla
 
genellikle
 
fiyatı
 
kendine
 
çeken
 
bir
 

## Sayfa 2

mıknatıs
 
görevi
 
görür.
3
 
Mum
 
çubuğu
 
formasyonları,
 
bu
 
psikolojik
 
savaşın
 
mikro
 
ölçekteki
 
özetleridir.
 
Örneğin,
 
bir
 
"pin
 
bar"
 
(çekiç
 
veya
 
kayan
 
yıldız),
 
fiyatın
 
belirli
 
bir
 
seviyeyi
 
test
 
ettiğini
 
ancak
 
o
 
seviyede
 
kalıcı
 
olamayacak
 
kadar
 
güçlü
 
bir
 
reddedişle
 
(rejection)
 
karşılaştığını
 
gösterir.
2
 
Boğa
 
yönlü
 
bir
 
pin
 
barın
 
alt
 
fitilinin
 
uzun
 
olması,
 
satıcıların
 
fiyatı
 
aşağı
 
çekmeye
 
çalıştığını
 
fakat
 
alıcıların
 
bu
 
satışı
 
agresif
 
bir
 
şekilde
 
karşılayarak
 
kontrolü
 
ele
 
aldığını
 
simgeler.
4
 
Benzer
 
şekilde,
 
"yutan
 
boğa"
 
(engulfing)
 
formasyonu,
 
bir
 
önceki
 
periyodun
 
tüm
 
arzının
 
bir
 
sonraki
 
periyotta
 
gelen
 
talep
 
tarafından
 
tamamen
 
yutulduğunu
 
ve
 
momentumun
 
radikal
 
bir
 
şekilde
 
değiştiğini
 
gösterir.
1
 
Grafik
 
Formasyonlarının
 
İstatistiksel
 
Güvenilirliği
 
Mühendislik
 
yaklaşımı,
 
görsel
 
formasyonların
 
öznel
 
yorumundan
 
ziyade,
 
bu
 
yapıların
 
tarihsel
 
veriler
 
üzerindeki
 
başarı
 
olasılıklarına
 
odaklanmayı
 
gerektirir.
 
Thomas
 
N.
 
Bulkowski’nin
 
binlerce
 
örneklem
 
üzerinde
 
yaptığı
 
çalışmalar,
 
klasik
 
grafik
 
yapılarının
 
(OBO,
 
Fincan-Kulp,
 
Bayrak
 
vb.)
 
tesadüfün
 
ötesinde
 
bir
 
performans
 
sergilediğini
 
ortaya
 
koymaktadır.
7
 
Bulkowski'nin
 
araştırmaları,
 
formasyonların
 
başarı
 
oranlarının
 
piyasa
 
koşullarına
 
ve
 
kırılım
 
yönüne
 
göre
 
dramatik
 
farklılıklar
 
gösterdiğini
 
saptamıştır.
9
 
Özellikle
 
boğa
 
piyasalarında,
 
yukarı
 
yönlü
 
kırılımların
 
başarı
 
oranı
 
ve
 
getiri
 
potansiyeli,
 
ayı
 
piyasalarındaki
 
aşağı
 
yönlü
 
kırılımlardan
 
istatistiksel
 
olarak
 
daha
 
yüksektir.
9
 
Grafik
 
Formasyonu
 
Başarı
 
Oranı
 
(Boğa
 
Piyasası)
 
Ortalama
 
Fiyat
 
Artışı
 
Güvenilirlik
 
Derecesi
 
Ters
 
Omuz
 
Baş
 
Omuz
 
(TOBO)
 
%89
 
%45
 
Çok
 
Yüksek
 
İkili
 
Dip
 
%88
 
%50
 
Yüksek
 
Üçlü
 
Dip
 
%87
 
%45
 
Yüksek
 
Alçalan
 
Üçgen
 
(Yukarı
 
Kırılım)
 
%87
 
%38
 
Yüksek
 
Dikdörtgen
 
Tepe
 
%85
 
%51
 
Orta-Yüksek
 
Baş
 
Omuz
 
Omuz
 
(Tepe)
 
%89
 
N/A
 
(Düşüş)
 
Çok
 
Yüksek
 

## Sayfa 3

10
 
Bu
 
veriler,
 
Omuz
 
Baş
 
Omuz
 
(OBO)
 
ve
 
İkili
 
Dip
 
gibi
 
yapıların
 
sadece
 
görsel
 
birer
 
araç
 
olmadığını,
 
%85-%90
 
aralığında
 
bir
 
öngörü
 
başarısına
 
sahip
 
olabildiğini
 
doğrulamaktadır.
10
 
Ancak
 
dikkat
 
edilmesi
 
gereken
 
husus,
 
piyasa
 
verimliliğinin
 
artmasıyla
 
birlikte
 
bu
 
başarı
 
oranlarının
 
1990'lı
 
yıllardan
 
günümüze
 
doğru
 
bir
 
miktar
 
aşınma
 
göstermiş
 
olmasıdır.
9
 
Örneğin,
 
%20'lik
 
bir
 
fiyat
 
artışı
 
hedefleyen
 
formasyonların
 
başarısızlık
 
oranı,
 
1991
 
yılında
 
%22
 
iken
 
2008
 
yılına
 
gelindiğinde
 
%62'ye
 
çıkmıştır.
9
 
Bu
 
durum,
 
formasyonların
 
tek
 
başına
 
değil,
 
hacim
 
analizi
 
ve
 
indikatör
 
onayıyla
 
birlikte
 
kullanılması
 
gerektiğini
 
(confluence)
 
matematiksel
 
olarak
 
kanıtlamaktadır.
7
 
İndikatör
 
Kombinasyonları
 
ve
 
Confluence
 
Stratejileri
 
İndikatörler,
 
fiyat
 
verisinin
 
belirli
 
matematiksel
 
fonksiyonlardan
 
(ortalama,
 
standart
 
sapma
 
vb.)
 
geçirilerek
 
filtrelenmiş
 
halidir.
 
Mühendislikte
 
"sinyal
 
işleme"
 
(signal
 
processing)
 
disiplinine
 
benzer
 
şekilde,
 
indikatör
 
kullanımındaki
 
amaç,
 
gürültüyü
 
(noise)
 
azaltarak
 
baskın
 
trendi
 
veya
 
dönüş
 
sinyalini
 
tespit
 
etmektir.
14
 
En
 
verimli
 
kullanım
 
senaryolarından
 
biri
 
RSI,
 
MACD
 
ve
 
Bollinger
 
Bantlarının
 
bir
 
arada
 
kullanıldığı
 
bütünleşik
 
yapıdır.
 
Bu
 
kombinasyon,
 
piyasanın
 
farklı
 
boyutlarını
 
(momentum,
 
trend
 
ve
 
oynaklık)
 
aynı
 
anda
 
ölçer.
14
 
1.
 
RSI
 
(Relative
 
Strength
 
Index):
 
Momentumun
 
hızını
 
ve
 
değişimini
 
ölçer.
 
30
 
altı
 
aşırı
 
satım,
 
70
 
üstü
 
aşırı
 
alım
 
bölgesi
 
olarak
 
kabul
 
edilir.
16
 
Ancak
 
en
 
güçlü
 
sinyaller,
 
fiyat
 
ile
 
RSI
 
arasındaki
 
uyumsuzluklardan
 
(divergence)
 
elde
 
edilir.
16
 
2.
 
MACD
 
(Moving
 
Average
 
Convergence
 
Divergence):
 
İki
 
hareketli
 
ortalamanın
 
birbirine
 
yaklaşma
 
ve
 
uzaklaşma
 
durumuna
 
göre
 
trend
 
yönünü
 
ve
 
gücünü
 
tayin
 
eder.
16
 
MACD'nin
 
sıfır
 
çizgisi
 
üzerindeki
 
kesişimleri
 
uzun
 
vadeli
 
trend
 
onayları
 
sağlar.
16
 
3.
 
Bollinger
 
Bantları:
 
Fiyatın
 
standart
 
sapmasını
 
kullanarak
 
oynaklığı
 
(volatility)
 
ölçer.
 
Fiyatın
 
alt
 
banda
 
değmesi
 
bir
 
tepki
 
alımı
 
ihtimalini,
 
üst
 
banda
 
değmesi
 
ise
 
bir
 
kar
 
satışı
 
ihtimalini
 
doğurur.
16
 
Bu
 
üç
 
aracın
 
"confluence"
 
(doğrulama)
 
stratejisi
 
şu
 
kurallara
 
dayanır:
 
●
 
Alış
 
Senaryosu:
 
Fiyatın
 
alt
 
Bollinger
 
Bandına
 
değmesi
 
(volatilite
 
sınırı),
 
RSI'ın
 
30'un
 
altına
 
inip
 
tekrar
 
üzerine
 
çıkması
 
(momentum
 
onayı)
 
ve
 
MACD'nin
 
sinyal
 
çizgisini
 
yukarı
 
kesmesi
 
(trend
 
onayı).
14
 
●
 
Satış
 
Senaryosu:
 
Fiyatın
 
üst
 
Bollinger
 
Bandına
 
değmesi,
 
RSI'ın
 
70'in
 
üzerine
 
çıkıp
 
aşağı
 
dönmesi
 
ve
 
MACD'nin
 
aşağı
 
yönlü
 
kesişimi.
14
 
Kısa
 
vadeli
 
(intraday)
 
işlemler
 
için
 
RSI
 
periyodunun
 
14'ten
 
5
 
veya
 
9'a
 
düşürülmesi
 
hassasiyeti
 
artırırken,
 
gürültüyü
 
azaltmak
 
için
 
80/20
 
gibi
 
daha
 
geniş
 
eşik
 
değerlerin
 
kullanılması
 
önerilir.
17
 

## Sayfa 4

Kantitatif
 
ve
 
İstatistiksel
 
Analiz:
 
Veriden
 
Modele
 
Matematiksel
 
bir
 
metodoloji
 
oluştururken,
 
fiyat
 
hareketlerini
 
sadece
 
görsel
 
olarak
 
değil,
 
zaman
 
serisi
 
analizi
 
ve
 
olasılık
 
teorisi
 
üzerinden
 
de
 
tanımlamak
 
esastır.
 
Bu
 
noktada
 
devreye
 
giren
 
istatistiksel
 
arbitraj
 
ve
 
yapay
 
zeka
 
modelleri,
 
yatırımcıya
 
önyargılardan
 
arındırılmış
 
bir
 
karar
 
mekanizması
 
sunar.
 
İstatistiksel
 
Modeller:
 
Mean-Reversion
 
ve
 
Pair
 
Trading
 
"Ortalamaya
 
dönüş"
 
(Mean-reversion),
 
bir
 
finansal
 
varlığın
 
fiyatının
 
zaman
 
içinde
 
tarihsel
 
ortalamasına
 
geri
 
döneceği
 
varsayımına
 
dayanır.
 
Pair
 
Trading
 
(Çift
 
İşlemi)
 
ise
 
bu
 
prensibi
 
iki
 
korele
 
varlık
 
arasındaki
 
ilişkiye
 
uygular.
19
 
Bu
 
stratejinin
 
matematiksel
 
omurgasını
 
Eşbütünleşme
 
(Cointegration)
 
oluşturur.
 
İki
 
varlığın
 
fiyat
 
serisi
 
(log-fiyatlar
 
 
ve
 
)
 
ayrı
 
ayrı
 
durağan
 
olmayabilir
 
(yani
 
birer
 
"random
 
walk"
 
serisidirler).
 
Ancak
 
bu
 
iki
 
serinin
 
öyle
 
bir
 
doğrusal
 
kombinasyonu
 
vardır
 
ki,
 
ortaya
 
çıkan
 
fark
 
serisi
 
(spread)
 
durağandır
 
(stationary).
20
 
Matematiksel
 
olarak
 
spread
 
(
)
 
şu
 
şekilde
 
ifade
 
edilir:
 
 
Burada
 
 
cointegration
 
katsayısını
 
(hedge
 
ratio),
 
 
ise
 
spread'in
 
uzun
 
vadeli
 
ortalamasını
 
temsil
 
eder.
20
 
Eğer
 
bu
 
spread
 
serisi
 
durağan
 
ise,
 
ortalamadan
 
her
 
sapma
 
bir
 
işlem
 
fırsatıdır.
 
Bu
 
sapmanın
 
büyüklüğünü
 
ölçmek
 
için
 
Z-skoru
 
kullanılır:
 
 
.
20
 
Z-Skoru
 
Değeri
 
Aksiyon
 
Teori
 
Z
 
>
 
+2.0
 
Spread'i
 
Sat
 
(Short
 
,
 
Long
 
)
 
Fiyat
 
farkı
 
tarihsel
 
olarak
 
çok
 
açıldı,
 
daralması
 
beklenir.
 
Z
 
<
 
-2.0
 
Spread'i
 
Al
 
(Long
 
,
 
Short
 
Fiyat
 
farkı
 
çok
 
düştü,
 
genişlemesi
 
beklenir.
 


## Sayfa 5

)
 
Z
 
=
 
0
 
Pozisyonu
 
Kapat
 
Spread
 
tarihsel
 
ortalamasına
 
(dengeye)
 
döndü.
 
20
 
Bu
 
modelin
 
başarısı,
 
Augmented
 
Dickey-Fuller
 
(ADF)
 
veya
 
Johansen
 
testleri
 
ile
 
onaylanmış
 
gerçek
 
bir
 
eşbütünleşme
 
ilişkisinin
 
varlığına
 
bağlıdır.
20
 
Sadece
 
yüksek
 
korelasyona
 
güvenmek
 
yanıltıcı
 
olabilir;
 
çünkü
 
korelasyon
 
kısa
 
vadeli
 
bir
 
ilişkiyi
 
temsil
 
ederken,
 
eşbütünleşme
 
uzun
 
vadeli
 
bir
 
ekonomik
 
bağı
 
(equilibrium)
 
gösterir.
20
 
Yapay
 
Zeka
 
ve
 
ML:
 
Hibrit
 
LSTM
 
ve
 
Random
 
Forest
 
Modelleri
 
Derin
 
öğrenme
 
modelleri,
 
finansal
 
verilerdeki
 
doğrusal
 
olmayan
 
karmaşık
 
ilişkileri
 
yakalamada
 
geleneksel
 
ekonometrik
 
modellerden
 
daha
 
başarılıdır.
 
Özellikle
 
LSTM
 
(Long
 
Short-Term
 
Memory)
 
ağları,
 
zaman
 
serisi
 
verilerindeki
 
uzun
 
ve
 
kısa
 
vadeli
 
bağımlılıkları
 
unutma/hatırlama
 
kapıları
 
sayesinde
 
efektif
 
bir
 
şekilde
 
modeller.
25
 
Ancak
 
tek
 
başına
 
bir
 
sinir
 
ağı
 
(NN),
 
finansal
 
verilerin
 
düşük
 
sinyal-gürültü
 
oranı
 
nedeniyle
 
"overfitting"
 
(aşırı
 
öğrenme)
 
riskine
 
açıktır.
 
Bu
 
riski
 
azaltmak
 
için
 
hibrit
 
modeller
 
geliştirilmiştir.
 
Başarılı
 
bir
 
hibrit
 
model
 
mimarisi,
 
LSTM'i
 
teknik
 
özellikleri
 
(features)
 
çıkarmak
 
için,
 
Random
 
Forest
 
(RF)
 
algoritmasını
 
ise
 
bu
 
özellikleri
 
sınıflandırmak
 
veya
 
regresyon
 
yapmak
 
için
 
kullanır.
27
 
Hibrit
 
modelin
 
girdi
 
kümesi
 
(Feature
 
Set)
 
genellikle
 
şunları
 
kapsar:
 
●
 
Teknik
 
Girdiler:
 
RSI,
 
MACD,
 
Bollinger
 
Bantları,
 
SMA/EMA
 
değerleri.
28
 
●
 
Fiyat
 
Yapısı:
 
Mum
 
çubuğu
 
formasyonlarının
 
sayısal
 
temsilleri.
29
 
●
 
Temel
 
Veriler
 
(Hibrit
 
yaklaşım
 
için):
 
F/K
 
oranı,
 
borç/özsermaye,
 
büyüme
 
oranları.
28
 
Araştırmalar,
 
LSTM
 
modellerinin
 
fiyat
 
yönü
 
tahmininde
 
%54.5
 
gibi
 
istatistiksel
 
bir
 
avantaj
 
sağladığını
 
göstermektedir.
28
 
Ancak
 
bu
 
performans,
 
LSTM
 
çıktılarının
 
(örneğin
 
tahmin
 
edilen
 
AUC
 
veya
 
olasılık
 
değerleri)
 
bir
 
Random
 
Forest
 
modeline
 
girdi
 
olarak
 
verilmesiyle
 
çok
 
daha
 
yüksek
 
seviyelere
 
çıkabilir.
 
482
 
varlık
 
üzerinde
 
yapılan
 
bir
 
çalışmada,
 
hibrit
 
modelin
 
AUC
 
(Area
 
Under
 
the
 
Curve)
 
skoru
 
0.566
 
iken,
 
yüksek
 
güvenilirlik
 
filtreleri
 
uygulandığında
 
bu
 
skorun
 
0.73'e
 
kadar
 
yükseldiği
 
görülmüştür.
28
 
Bu
 
durum,
 
modelin
 
her
 
zaman
 
işlem
 
yapması
 
yerine,
 
sadece
 
tahmin
 
olasılığının
 
yüksek
 
olduğu
 
"rejimleri"
 
seçmesinin
 
önemini
 
vurgular.
28
 
Duygu
 
Analizi
 
(Sentiment):
 
Haber
 
ve
 
Sosyal
 
Medya
 
Korelasyonu
 
Piyasa
 
sadece
 
sayılarla
 
değil,
 
kelimelerle
 
de
 
hareket
 
eder.
 
Doğal
 
Dil
 
İşleme
 
(NLP)
 
teknikleri,
 


## Sayfa 6

haber
 
akışlarını
 
ve
 
sosyal
 
medya
 
(Twitter,
 
Reddit)
 
verilerini
 
kantitatif
 
sinyallere
 
dönüştürebilir.
30
 
Duygu
 
analizi
 
ve
 
piyasa
 
yönü
 
arasındaki
 
korelasyonlar
 
üzerine
 
yapılan
 
çalışmalar
 
şu
 
kritik
 
bulguları
 
ortaya
 
koymaktadır:
 
●
 
Haber
 
Başlıkları
 
ve
 
Getiri:
 
Haber
 
başlıklarından
 
elde
 
edilen
 
duygu
 
skorları,
 
hisse
 
senedi
 
getirileriyle
 
(returns)
 
doğrudan
 
ve
 
istatistiksel
 
olarak
 
anlamlı
 
bir
 
korelasyona
 
sahiptir.
30
 
Negatif
 
haber
 
yoğunluğu
 
genellikle
 
fiyat
 
üzerinde
 
kalıcı
 
bir
 
baskı
 
yaratır.
31
 
●
 
Sosyal
 
Medya
 
ve
 
Oynaklık:
 
Twitter
 
gibi
 
platformlardaki
 
duygu
 
değişimi,
 
fiyattan
 
ziyade
 
"oynaklık"
 
(volatility)
 
ile
 
daha
 
yüksek
 
korelasyon
 
gösterir.
 
Özellikle
 
pozitif
 
duygudaki
 
artışın
 
ertesi
 
günkü
 
oynaklığı
 
azalttığı
 
(-0.7
 
korelasyon)
 
saptanmıştır.
30
 
●
 
Tahmin
 
Başarısı:
 
VADER
 
veya
 
transformer
 
tabanlı
 
(BERT)
 
modeller
 
kullanılarak
 
yapılan
 
duygu
 
analizleri,
 
oynaklık
 
yönünü
 
tahmin
 
etmede
 
%63-%67
 
aralığında
 
bir
 
doğruluk
 
oranına
 
ulaşabilmektedir.
30
 
BIST
 
piyasası
 
özelinde
 
yapılan
 
araştırmalar,
 
COVID-19
 
pandemisi
 
gibi
 
kriz
 
dönemlerinde
 
haber
 
kaynaklı
 
duygu
 
skorlarının
 
endeks
 
yönünü
 
tahmin
 
etmede
 
teknik
 
indikatörleri
 
destekleyen
 
güçlü
 
birer
 
öncü
 
gösterge
 
olduğunu
 
doğrulamaktadır.
33
 
Bireysel
 
Yatırımcı
 
İçin
 
Uygulama
 
ve
 
Altyapı
 
Bir
 
metodolojinin
 
matematiksel
 
olarak
 
güçlü
 
olması
 
yeterli
 
değildir;
 
onun
 
uygulanabilir
 
ve
 
sürdürülebilir
 
bir
 
teknolojik
 
altyapıya
 
sahip
 
olması
 
gerekir.
 
Bireysel
 
bir
 
yatırımcı
 
için
 
hem
 
Amerikan
 
borsaları
 
hem
 
de
 
BIST
 
verilerine
 
erişim,
 
bugün
 
her
 
zamankinden
 
daha
 
kolaydır.
 
Veri
 
ve
 
API
 
Çözümleri
 
Amerikan
 
borsası
 
(NYSE,
 
NASDAQ)
 
için
 
geniş
 
bir
 
API
 
yelpazesi
 
mevcuttur.
 
BIST
 
için
 
ise
 
yerel
 
sağlayıcıların
 
sunduğu
 
profesyonel
 
terminaller
 
öne
 
çıkar.
 
 
Sağlayıcı
 
Kapsam
 
En
 
Uygun
 
Kullanım
 
Alanı
 
Özellikler
 
Alpha
 
Vantage
 
ABD
 
ve
 
Global
 
Kantitatif
 
Analiz
 
&
 
AI
 
Ücretsiz
 
katman,
 
teknik
 
indikatör
 
desteği,
 
AI
 
entegrasyonu.
35
 
Polygon.io
 
ABD
 
Yüksek
 
Frekanslı
 
İşlem
 
(HFT)
 
Ultra
 
düşük
 
gecikme,
 
W ebSocket
 
üzerinden
 
anlık
 

## Sayfa 7

veri.
36
 
Financial
 
Modeling
 
Prep
 
(FMP)
 
ABD
 
ve
 
Avrupa
 
Temel
 
Analiz
 
&
 
Portföy
 
Takibi
 
30
 
yıllık
 
geçmiş
 
veri,
 
mali
 
tablolar,
 
hızlı
 
REST
 
API.
37
 
Matriks
 
IQ
 
BIST
 
Yerel
 
Algoritmik
 
Ticaret
 
Türkiye
 
piyasasına
 
tam
 
entegrasyon,
 
Python
 
desteği,
 
kurumsal
 
veri
 
kalitesi.
39
 
Yahoo
 
Finance
 
(yfinance)
 
Global
 
Backtesting
 
&
 
Prototipleme
 
Ücretsiz,
 
geniş
 
kütüphane
 
desteği,
 
gecikmeli
 
veri.
38
 
35
 
BIST
 
verilerini
 
Python
 
ile
 
çekmek
 
isteyen
 
yatırımcılar
 
için
 
Matriks
 
IQ,
 
REST
 
API
 
ve
 
MQTT/socket
 
protokolleri
 
üzerinden
 
canlı
 
veri
 
akışı
 
sağlar.
39
 
Ayrıca,
 
BIST'teki
 
temettü
 
ve
 
sermaye
 
artırımı
 
gibi
 
veriler
 
için
 
açık
 
kaynaklı
 
Python
 
projeleri
 
(örneğin
 
FastAPI
 
tabanlı
 
mikroservisler)
 
kullanılabilir.
41
 
TradingView
 
Pine
 
Script
 
ise,
 
görsel
 
analiz
 
ile
 
basit
 
algoritmik
 
mantığı
 
birleştirmek
 
için
 
en
 
kullanıcı
 
dostu
 
platformdur;
 
özellikle
 
Bulkowski
 
formasyonlarının
 
otomatik
 
tespiti
 
için
 
hazır
 
script
 
kütüphanelerine
 
sahiptir.
10
 
Matematiksel
 
Risk
 
Yönetimi:
 
Kelly
 
Criterion
 
ve
 
VaR
 
Bir
 
mühendis
 
için
 
risk
 
yönetimi,
 
"maksimum
 
zarar"
 
olasılığını
 
minimize
 
ederken
 
"geometrik
 
büyüme
 
hızını"
 
maksimize
 
etme
 
optimizasyonudur.
 
Bu
 
noktada
 
iki
 
temel
 
model
 
öne
 
çıkar:
 
1.
 
Kelly
 
Criterion
 
(Kelly
 
Kriteri):
 
Uzun
 
vadeli
 
sermaye
 
büyümesini
 
maksimize
 
etmek
 
için
 
her
 
bir
 
işleme
 
yatırılması
 
gereken
 
optimal
 
sermaye
 
oranını
 
belirler.
42
 
 
Burada
 
 
kazanma
 
olasılığı,
 
 
kaybetme
 
olasılığı
 
(
),
 
 
ise
 
risk-ödül
 
oranıdır.
44
 
Yatırım
 
dünyasında
 
daha
 
muhafazakar
 
olan
 
"Half-Kelly"
 
(hesaplanan
 
değerin
 
yarısı)
 
kullanımı,
 
model
 
hatalarına
 
karşı
 
bir
 
emniyet
 
payı
 
bırakmak
 
ve
 
volatiliteyi
 
düşürmek
 
için
 
önerilir.
45
 
2.
 
Value
 
at
 
Risk
 
(VaR
 
-
 
Riske
 
Maruz
 
Değer):
 
Belirli
 
bir
 
güven
 
düzeyinde
 
(örneğin
 
%95)
 
ve
 
belirli
 
bir
 
zaman
 
diliminde
 
(örneğin
 
1
 
gün)
 
portföyün
 
uğrayabileceği
 
maksimum
 
zararı
 
tahmin
 
eder.
48
 


## Sayfa 8

○
 
Parametrik
 
VaR:
 
Getirilerin
 
normal
 
dağıldığını
 
varsayar.
 
Portföyün
 
ortalama
 
getirisi
 
ve
 
standart
 
sapması
 
üzerinden
 
hesaplanır.
 
Hızlıdır
 
ancak
 
"şişman
 
kuyruk"
 
(fat
 
tail)
 
risklerini
 
göz
 
ardı
 
edebilir.
48
 
○
 
Monte
 
Carlo
 
VaR:
 
Binlerce
 
rastgele
 
fiyat
 
senaryosu
 
oluşturarak
 
bir
 
olasılık
 
dağılımı
 
çıkarır.
 
Doğrusal
 
olmayan
 
riskleri
 
(opsiyonlar
 
vb.)
 
ve
 
karmaşık
 
portföy
 
yapılarını
 
modellemek
 
için
 
en
 
güçlü
 
yöntemdir.
49
 
Algoritmik
 
Filtreleme
 
ve
 
Otomasyon
 
Süreci
 
Teknik
 
analizi
 
ve
 
kantitatif
 
modelleri
 
birleştirerek
 
bir
 
otomasyon
 
pipeline'ı
 
(boru
 
hattı)
 
oluşturmak,
 
insan
 
faktöründen
 
kaynaklanan
 
duygusal
 
hataları
 
elimine
 
eder.
 
İdeal
 
bir
 
algoritmik
 
filtreleme
 
süreci
 
şu
 
aşamalardan
 
oluşur:
 
1.
 
Evren
 
Oluşturma
 
ve
 
Statik
 
Filtreleme:
 
Binlerce
 
hisse
 
arasından
 
hacim,
 
likidite
 
ve
 
volatilite
 
kriterlerine
 
göre
 
işlem
 
yapılabilecek
 
varlıkları
 
seçme
 
(Screener).
16
 
2.
 
Dinamik
 
Teknik
 
Filtreleme
 
(Confluence):
 
Bollinger
 
Squeeze
 
veya
 
RSI
 
uyumsuzluğu
 
gibi
 
"yüksek
 
olasılıklı"
 
teknik
 
kurulumları
 
gerçek
 
zamanlı
 
tespit
 
etme.
16
 
3.
 
İstatistiksel
 
Onay
 
(Regime
 
Detection):
 
Seçilen
 
hissenin
 
mevcut
 
piyasa
 
rejiminin
 
(trend
 
mi
 
yoksa
 
yatay
 
mı?)
 
stratejiye
 
uygunluğunu
 
Z-skoru
 
veya
 
eşbütünleşme
 
testleriyle
 
onaylama.
20
 
4.
 
AI
 
Tahmin
 
ve
 
Duygu
 
Analizi
 
Skoru:
 
Hibrit
 
LSTM-RF
 
modelinden
 
gelen
 
fiyat
 
yönü
 
tahmini
 
ile
 
sosyal
 
medya/haber
 
sentiment
 
skorunun
 
(VADER/BERT)
 
teknik
 
sinyalle
 
aynı
 
yönde
 
olup
 
olmadığını
 
kontrol
 
etme.
28
 
5.
 
Risk
 
Ayarlamalı
 
Emir
 
İletimi:
 
Kelly
 
Kriterine
 
göre
 
pozisyon
 
büyüklüğünü
 
belirleme
 
ve
 
VaR
 
sınırları
 
içinde
 
kalarak
 
API
 
üzerinden
 
(Interactive
 
Brokers
 
veya
 
Matriks
 
IQ)
 
emirleri
 
iletme.
39
 
Sentez
 
ve
 
Sonuç
 
Bu
 
raporun
 
ortaya
 
koyduğu
 
metodoloji,
 
klasik
 
teknik
 
analizin
 
sezgisel
 
gücünü
 
matematiksel
 
disiplin
 
ve
 
modern
 
hesaplama
 
teknikleriyle
 
tahkim
 
etmektedir.
 
Bir
 
mühendis
 
için
 
yatırım,
 
bir
 
"kazanma
 
garantisi"
 
arayışı
 
değil,
 
beklenen
 
değeri
 
pozitif
 
olan
 
bir
 
seriler
 
bütününü
 
yönetmektir.
 
Klasik
 
grafik
 
formasyonlarının
 
%85'i
 
aşan
 
tarihsel
 
başarı
 
oranları,
 
piyasa
 
psikolojisinin
 
tekrarlanabilir
 
olduğunun
 
kanıtıdır;
 
ancak
 
bu
 
formasyonların
 
tek
 
başına
 
kullanımı
 
modern
 
verimli
 
piyasalarda
 
yeterli
 
değildir.
 
İndikatör
 
confluence'ı,
 
bu
 
geometrik
 
yapıları
 
momentum
 
ve
 
oynaklık
 
verisiyle
 
doğrular.
 
Pair
 
trading
 
ve
 
mean-reversion
 
modelleri,
 
bireysel
 
hisse
 
riskinden
 
kaçınarak
 
piyasada
 
var
 
olan
 
göreli
 
değer
 
bozulmalarından
 
(relative
 
mispricing)
 
kar
 
etme
 
imkanı
 
sağlar.
 
Hibrit
 
yapay
 
zeka
 
modelleri
 
(LSTM-Random
 
Forest),
 
geleneksel
 
modellerin
 
kaçırdığı
 
doğrusal
 
olmayan
 
ilişkileri
 
ve
 
rejim
 
değişikliklerini
 
yakalayarak
 
tahmin
 
başarısını
 
AUC
 
0.73
 
gibi
 
profesyonel
 
seviyelere
 
taşıyabilir.
 
Sonuç
 
olarak,
 
Amerikan
 
borsasının
 
derin
 
likiditesi
 
ve
 
BIST'in
 
büyüme
 
potansiyeli,
 
ancak
 
veriye
 
dayalı,
 
riskini
 
matematiksel
 
modellerle
 
(Kelly,
 
VaR)
 
sınırlayan
 
ve
 
karar
 
sürecini
 
algoritmik
 
filtrelerle
 
otomatize
 
eden
 
bir
 
yatırımcı
 
için
 
sürdürülebilir
 
bir
 
getiri
 
kaynağına
 
dönüşebilir.
 
Bu
 

## Sayfa 9

metodolojinin
 
başarısı,
 
sürekli
 
bir
 
backtesting,
 
optimizasyon
 
ve
 
piyasa
 
duyarlılığı
 
(sentiment)
 
takibi
 
ile
 
dinamik
 
olarak
 
güncellenmesine
 
bağlıdır.
 
Alıntılanan
 
çalışmalar
 
1.
 
Decoding
 
Forex:
 
Mastering
 
the
 
Price
 
Action
 
Trading
 
Strategy,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://topbrokers.com/forex-strategies/price-action-trading-strategy/
 
2.
 
Short
 
guide
 
to
 
price
 
action
 
trading
 
-
 
Think Markets,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.thinkmarkets.com/en/trading-academy/technical-analysis/short-guid 
e-to-price-action-trading/
 
3.
 
Price
 
action
 
trading:
 
master
 
candlesticks
 
&
 
market
 
structure
 
-
 
Equiti,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.equiti.com/jo-en/news/trading-ideas/what-is-price-action-trading-a 
nd-how-can-you-use-it/
 
4.
 
W hat
 
is
 
Price
 
Action?
 
A
 
Comprehens ive
 
Guide
 
for
 
Traders,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://eplanetbrokers.com/training/price-action
 
5.
 
Chapter
 
4
 
-
 
Price
 
Action
 
Confirmation
 
Technique s
 
-
 
Forex
 
University,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://forex.university/lessons/chapter-4-price-action-confirmation-techniques/
 
6.
 
Price
 
Action
 
Trading
 
for
 
Stock
 
Traders
 
-
 
TrueData,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.truedata.in/blog/what-is-price-action-trading
 
7.
 
Encyclopedia
 
Of
 
Chart
 
Patterns
 
3rd
 
Edition
 
-
 
Sema,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://mirante.sema.ce.gov.br/sites/HomePages/600015/mL0115/enc yclopedia_o 
f_chart---patterns_3rd_edition.pdf
 
8.
 
Encyclopedia
 
Of
 
Chart
 
Patterns
 
2nd
 
Edition
 
W iley
 
Trading ,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.yic.edu.et/_pdfs/uploaded-files/R72QMP/Encyclopedia_Of_Chart_Pat 
terns_2nd_Edition_W iley_Trading.pdf
 
9.
 
Do
 
Chart
 
Patterns
 
Still
 
W ork
 
By
 
Thomas
 
Bulkowski
 
-
 
Sacred
 
Traders,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://sacredtraders.com/do-chart-patterns -still-work-by-thomas-bulkowski/
 
10.
 
Profitable
 
Chart
 
Patterns
 
&
 
Success
 
Rates
 
|
 
PDF
 
|
 
Technical
 
Analysis,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.scribd.com/document/660493367/W ww-Liberatedstocktrader-Co m 
-Chart-Patterns-Reliable-Profitable
 
11.
 
Bulkowski's
 
Chart
 
and
 
Event
 
Pattern
 
Rank
 
-
 
ThePatternSite.com,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://thepatternsite.com/rank.html
 
12.
 
Encyclopedia
 
of
 
Chart
 
Patterns
 
By
 
Thomas
 
N.
 
Bulkowski,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://sacredtraders.com/product/encyclopedia-of-chart-patterns -thomas-n-bu 
lkowski/
 
13.
 
55
 
Trading
 
Chart
 
Patterns
 
for
 
Smarter
 
Market
 
Predictions,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.strike.money/technical-analysis/chart-patterns
 
14.
 
Intraday
 
Trading
 
Using
 
RSI,
 
MACD,
 
and
 
Bollinger
 
Bands,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 

## Sayfa 10

https://www.swastika.co.in/blog/intraday-trading-us ing-rsi-macd-and-bollinger-b 
ands
 
15.
 
RSI,
 
MACD,
 
Bollinger
 
Bands
 
and
 
Volume-Based
 
Hybrid
 
Trading ,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://medium.com/@redsword_23261/rsi-macd-bollinger-bands-and-volume-b 
ased-hybrid-trading-strategy-fb 1ecfd58e1b
 
16.
 
Top
 
Intraday
 
Trading
 
Indicators:
 
Bollinger
 
Bands,
 
Moving
 
Averages
 
...,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://groww.in/blog/intraday-trading-indicators
 
17.
 
Best
 
Rsi
 
Settings
 
for
 
Day
 
Trading
 
-
 
Goat
 
Fund ed
 
Trader,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.goatfundedtrader.com/blog/best-rsi-settings-for-day-trading
 
18.
 
Best
 
Bollinger
 
Bands
 
Trading
 
Strategy
 
You
 
Should
 
Learn,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.stockdaddy.in/blog/bollinger-bands-strategy
 
19.
 
PARAMETERS
 
OPTIMIZATION
 
OF
 
PAIR
 
TRADING
 
ALGORITHM,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://arxiv.org/html/2412.12555v1
 
20.
 
Pairs
 
Trading
 
-
 
The
 
Hong
 
Kong
 
University
 
of
 
Science
 
and
 
Technology,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://palomar.home.ece.ust.hk/MAFS5310_lectur es/slides_pairs_trading.pdf
 
21.
 
Cointegrated
 
Time
 
Series
 
Analysis
 
for
 
Mean
 
Reversion
 
Trading
 
with
 
R,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.quantstart.com/articles/Cointegrated-Time-Series-Analysis-for-Mea 
n-Reversion-Trading-with-R/
 
22.
 
(PDF)
 
A
 
Comprehensive
 
Methodology
 
for
 
Pairs
 
Trading
 
Strategy,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.researchgate.net/publication/392755592_A_Comprehensive_Method 
ology_for_Pairs_Trading_Strategy_and_Performance_Evaluation
 
23.
 
Gold
 
Silver
 
Pair
 
Trading
 
-
 
Mean
 
Reversion
 
Strategy
 
Using
 
Machine ,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://papers.ssrn.com/sol3/Delivery.cfm/5710242.pdf?abstractid=5710242&miri 
d=1
 
24.
 
slides-pairs-trading.pdf
 
-
 
Portfolio
 
Optimization
 
Book,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://portfoliooptimizationbook.com/slides/slides-pairs-trading.pdf
 
25.
 
Implementations
 
of
 
Hybrid
 
Prediction
 
Models
 
for
 
Stock
 
Price,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.scitepress.org/Papers/2024/132707/132707.pdf
 
26.
 
"A
 
Hybrid
 
Lens
 
on
 
Stock
 
Prediction:
 
Exploring
 
LSTM
 
and
 
RNN
 
Models",
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.jetir.org/papers/JETIR250 6195.pdf
 
27.
 
(PDF)
 
Research
 
on
 
Stock
 
Price
 
Prediction
 
Based
 
on
 
LSTM
 
Model,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.researchgate.net/publication/380931042_Research_on_Stock_Price_ 
Prediction_Based_on_LSTM_Model_and_Random_Forest
 
28.
 
Integration
 
of
 
LSTM
 
Networks
 
in
 
Rand om
 
Forest
 
Algorithms
 
for
 
Stock
 
...,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.mdpi.com/2571-9394/7/3/49
 
29.
 
A
 
Hybrid
 
Relational
 
Approach
 
Toward
 
Stock
 
Price
 
Prediction
 
and,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.computer.org/csdl/journal/ai/2024/11/10543183/1XorlLOYuic
 
30.
 
A
 
sentiment
 
analysis
 
approach
 
to
 
the
 
prediction
 
of
 
market
 
...
 
-
 
Frontiers,
 
erişim
 

## Sayfa 11

tarihi
 
Şubat
 
20,
 
2026,
 
https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2022 
.836809/full
 
31.
 
Real-Time
 
Stock
 
Trend
 
Prediction
 
via
 
Sentiment
 
Ana lysis
 
of
 
News,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID3753015_code3542370.pdf?ab 
stractid=3753015&mirid=1
 
32.
 
Studies
 
of
 
Sentiment
 
Analysis
 
for
 
Stock
 
Market
 
Prediction
 
using,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://saspublishers.com/media/articles/SJET_131_56-65.pdf
 
33.
 
Predicting
 
BIST
 
100
 
Index
 
Movement
 
by
 
us ing
 
Sentiment
 
Scores,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.researchgate.net/publication/364977334_Predicting_BIST_100_Index 
_Movement_by_using_Sentiment_Scores_and_Technical_Indicators_during_the_C 
OVID-19_Pandemic
 
34.
 
Rule
 
Based
 
Sentiment
 
Analysis
 
W ith
 
Python
 
for
 
Turkey's
 
Stock
 
Market,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://medium.com/analytics-vidhya/rule-based-sentiment-analysis-with-python 
-for-turkeys-stock-market-839f85d7daaf
 
35.
 
Best
 
Stock
 
Market
 
Data
 
APIs
 
For
 
Algorithmic
 
Traders
 
(2025
 
Edition),
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://hackernoon.com/best-stock-market-data-apis-for-algorithmic-traders-2 
025-edition
 
36.
 
12
 
Best
 
Financial
 
Market
 
APIs
 
for
 
Real-Time
 
Data
 
in
 
2025,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://blog.apilayer.com/12-best-financial-market-apis-for-real-time-data-in-20 
25/
 
37.
 
Best
 
Real-Time
 
Stock
 
Market
 
Data
 
APIs
 
in
 
2026
 
|
 
Co...
 
|
 
FMP,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://site.financialmodelingprep.com/education/other/best-realtime-stock-mark 
et-data-apis-in-
 
38.
 
Best
 
Free
 
Finance
 
APIs
 
for
 
Stock
 
&
 
Crypto
 
Market
 
Data
 
in
 
2025,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://noteapiconnector.com/best-free-finance-apis
 
39.
 
Veri
 
ve
 
İçerik
 
Sağlayıcı
 
Servisler
 
|
 
Matriks,
 
erişim
 
tarihi
 
Şub at
 
20,
 
2026,
 
https://www.matriksdata.com/website/egitim/sikca-sorulan-sorular/veri-ve-icerik- 
saglayici-servisler-sss
 
40.
 
Top
 
5
 
Stock
 
Data
 
Providers
 
of
 
2026:
 
Featur es,
 
Pricing
 
&
 
More,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://brightdata.com/blog/web-data/best-stock-data-providers
 
41.
 
borsa-istanbul
 
·
 
GitHub
 
Topics,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://github.com/topics/borsa-istanbul
 
42.
 
DYNAMIC
 
KELLY
 
CRITERION
 
-BASED
 
PORTFOLIO
 
LEVERAGE,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://trepo.tuni.fi/bitstream/10024/228489/2/AntilaTapio.pdf
 
43.
 
How
 
to
 
Use
 
the
 
Kelly
 
Criterion
 
to
 
Avoid
 
Portfolio-Killing
 
Mistakes,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://astuteinvestorscalculus.com/the-kelly-criterion/
 
44.
 
Kelly
 
Criterion
 
vs
 
Fixed
 
Fractional:
 
W hich
 
Risk
 
Model
 
Maximizes,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 

## Sayfa 12

https://medium.com/@tmapendembe_28659/kelly-criterion-vs-fixed-fractional-w 
hich-risk-model-maximizes-long-term-growth-972ecb606e6c
 
45.
 
Kelly
 
criterion
 
-
 
W ikipedia,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://en.wikipedia.org/wiki/Kelly_criterion
 
46.
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://astuteinvestorscalculus.com/the-kelly-criterion/#:~:text=Kelly%20weight% 
20%3D%20Expected%20Return%20%2F%20Variance,Kelly%20or%20even%20q 
uarter%2DKelly.
 
47.
 
Practical
 
Implementation
 
of
 
the
 
Kelly
 
Criterion:
 
Optimal
 
Growth
 
Rate,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.frontiersin.org/journals/applied-mathematics-and-statistics/articles/1 
0.3389/fams.2020.577050/full
 
48.
 
the
 
importance
 
of
 
value
 
at
 
risk
 
method
 
-
 
ASECU,
 
erişim
 
tarihi
 
Şub at
 
20,
 
2026,
 
https://www.asecu.gr/files/RomaniaProceedings/64.pdf
 
49.
 
Understanding
 
Value
 
at
 
Risk
 
(VaR)
 
-
 
Crystal
 
Capital
 
Partners,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.crystalfunds.com/insights/understanding-value-at-risk
 
50.
 
Value
 
at
 
Risk
 
(VAR)
 
-
 
Definition,
 
Methods,
 
Free
 
Excel
 
W orkout ,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.fe.training/free-resources/fina ncial-markets/value-at-risk-var/
 
51.
 
(PDF)
 
Comparative
 
Analysis:
 
Value
 
at
 
Risk
 
(VaR)
 
with
 
Parametric,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://www.researchgate.net/publication/387742821_Comparative_Analysis_Valu 
e_at_Risk_VaR_with_Parametric_Method_Monte_Carlo_Simulation_and_Historical 
_Simulation_of_Mining_Companies_in_ Indonesia
 
52.
 
Sentiment
 
Analysis
 
with
 
Ticker
 
News
 
API
 
Ins ights
 
-
 
Massive,
 
erişim
 
tarihi
 
Şubat
 
20,
 
2026,
 
https://massive.com/blog/sentiment-analysis-with-ticker-ne ws-api-insights
 

