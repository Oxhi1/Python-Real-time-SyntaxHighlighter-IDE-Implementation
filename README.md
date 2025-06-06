# Python-Real-time-SyntaxHighlighter-IDE-Implementation

# Real-Time Grammar-Based Syntax Highlighter with GUI

Bu proje, Python dilinde yazılmış, gerçek zamanlı çalışan bir sözdizimi (syntax) vurgulayıcıdır. Kullanıcı arayüzü sayesinde yazılan kod anında analiz edilir, hatalı yapılar görsel olarak belirtilir ve parse edilebilirliği kontrol edilir.

🎥 Video Nasıl çalıştığına buradan bakabilirsiniz ---->>>  https://youtu.be/XkgBruGCkwQ

Parse kısımları ayrı bir blokta yazılmamıştır main.py dosyasına dahildir.

## Özellikler

- ✅ **Lexical Analyzer:** Regex tabanlı tokenizer
- ✅ **Syntax Analyzer:** Recursive descent (top-down parser)
- ✅ **Gerçek Zamanlı Vurgulama:** 5+ token tipi (keyword, identifier, number, string, operator, delimiter, comment)
- ✅ **GUI (tkinter):** Kullanıcı dostu arayüz
- ✅ **Parse Kontrolü:** Hatalı kodlarda uyarı
- ❌ **Syntax highlighting kütüphaneleri** kullanılmadı (yasak!)

## 🛠 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.7+
- Tkinter (Python ile birlikte gelir)
  
✍️ Kod Örneği
Doğru çalışan bir örnek:

def foo(x):
    if x > 5:
        return x + 1

Parse hatası üreten örnek:
def foo(x)
    return x +

## KOD BAZLI AÇIKLAMA
🔹 tokenize(code) – Lexical Analyzer
Amaç:
Kullanıcının yazdığı kodu satır satır okuyarak, her parçayı (token) tanımlar. Bu token'lar daha sonra parser tarafından analiz edilecektir.

## Token Türleri:

KEYWORD: if, else, while, def, return

IDENTIFIER: Değişken ya da fonksiyon isimleri

NUMBER: Sayısal ifadeler

STRING: Tırnak içindeki string'ler

OPERATOR: +, -, ==, >= gibi operatörler

DELIMITER: :, (, ) gibi ayraçlar

COMMENT: # ile başlayan satır sonu yorumları

NEWLINE: Satır geçişi

## Nasıl çalışır?

Kod satır satır gezilir

Her karaktere bakılır

Regex kullanılarak string, sayı, identifier, yorum gibi yapılar ayrıştırılır

Uyumlu token bulunduğunda listeye eklenir

🔹 Parser Sınıfı – Top-Down Recursive Descent Parser
##Amaç:
Token’ları gramatik kurallara göre analiz eder. Kurallar önceden belirlenmiştir ve parser bu kurallara göre her ifadeyi adım adım çözümlemeye çalışır.

##Yapı:

self.tokens: Token listesi

self.pos: Şu anda hangi token’da olduğunu takip eder

Ana Fonksiyonlar:

🔸 parse()
Parse işlemini başlatır. İlk olarak bir "statement list" (kod bloğu) analiz edilir.

🔸 parse_stmt_list()
Birden fazla satırdan oluşan kod bloklarını işler (if ve def gibi yapılar için önemlidir).

🔸 parse_stmt()
Tek bir satırı parse eder. Desteklenen yapılar:

if, while, def, return, atama (x = 5), yorum satırı

🔸 parse_param_list()
Fonksiyon tanımı içindeki parametreleri işler.

🔸 parse_expr(), parse_arith_expr(), parse_comparison(), parse_term(), parse_factor()
Aritmetik ifadeleri sıralı olarak işler. Operatör önceliklerine göre gruplar:

Parantez

Çarpma-bölme

Toplama-çıkarma

## Karşılaştırma operatörleri

🔸 expect() ve match()
Token’ın beklenen tipte olup olmadığını kontrol eder.

expect: Değilse hata fırlatır (zorunlu)

match: Uygunsa ilerler, değilse pas geçer (isteğe bağlı)

🔹 SyntaxHighlighter Sınıfı (GUI Sınıfı – tkinter)
## Amaç:
Kullanıcıya görsel olarak yazdığı kodu renklendirmek ve anlık olarak hataları göstermek.

## Yapı:

Text alanı: Kodun yazıldığı yer

Label: Parse hatalarını gösteren etiket

Button: Kullanıcı manuel parse kontrolü yapmak isterse

Renk Kodlaması (token_colors):

Anahtar kelimeler mavi

String'ler yeşil

Sayılar turuncu

Operatörler kırmızı

Yorumlar gri

Hatalı token'lar pembe arka planlı

## Fonksiyonlar:

🔸 on_change(event)
Kullanıcı yazdıkça tetiklenir. Highlight işlemini 100ms gecikmeli başlatır.

🔸 highlight()
tokenize fonksiyonunu çağırır

GUI’de tüm token'ları uygun renkle boyar

Parser ile kod parse edilir; hata varsa GUI'de gösterilir

🔸 check_parse()
“Parse Kontrolü” butonuna basıldığında çalışır

Parser sınıfı üzerinden kod parse edilir, hata varsa kullanıcıya gösterilir









Geliştirici
Ad Soyad: Abdullah Çelik


