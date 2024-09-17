# Gelişmiş API İstemcisi

Bu proje, API isteklerini, WebSocket bağlantılarını, asenkron işlemleri ve zamanlanmış görevleri destekleyen kapsamlı bir istemci uygulamasıdır. Ayrıca, yanıtları dosyaya ve veritabanına kaydetme özelliği sunar.

## Özellikler

- HTTP istekleri (GET, POST, PUT, DELETE)
- WebSocket bağlantıları
- Asenkron istekler
- Zamanlanmış görevler
- Yanıtları dosyaya veya veritabanına kaydetme
- Farklı yanıt formatları (JSON, XML, CSV, YAML)

## Gereksinimler

- Python 3.6 veya üzeri
- Gerekli Python paketleri: `argparse`, `asyncio`, `logging`, `pandas`, `requests`, `yaml`

## Kurulum

1. Bu depoyu klonlayın:
    ```bash
    git clone https://github.com/bursow/APIcat
    ```

2. Proje dizinine gidin:
    ```bash
    cd APIcat
    ```

3. Gerekli Python paketlerini yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

## Kullanım

### Komut Satırı Argümanları

- `--url` (Gerekli): API URL veya WebSocket URI
- `--method` (Varsayılan: "get"): HTTP yöntemi (get, post, put, delete)
- `--save-file` (Opsiyonel): Yanıtı dosyaya kaydet
- `--api-key` (Opsiyonel): API anahtarı
- `--db-save` (Opsiyonel): Yanıtı veritabanına kaydet
- `--format` (Varsayılan: "json"): Dosya formatı (json, xml, csv, yaml)
- `--async_` (Opsiyonel): Asenkron istekleri etkinleştir
- `--scheduler` (Opsiyonel): Zamanlanmış görevleri etkinleştir
- `--ws` (Opsiyonel): WebSocket bağlantısı kur

### Örnek Kullanım

- Basit bir GET isteği yapmak ve yanıtı dosyaya kaydetmek:
    ```bash
    python main.py --url https://api.example.com/data --save-file --format json
    ```

- Asenkron olarak API isteği yapmak:
    ```bash
    python main.py --url https://api.example.com/data --async_ --api-key YOUR_API_KEY
    ```

- WebSocket bağlantısı kurmak:
    ```bash
    python main.py --url wss://example.com/socket --ws
    ```

- Zamanlanmış görevleri etkinleştirmek (örneğin, her saat başı):
    ```bash
    python main.py --url https://api.example.com/data --async_ --scheduler
    ```

## Dosya ve Veritabanı Kaydetme

- Yanıtı dosyaya kaydederken kullanılan formatlar: JSON, XML, CSV, YAML
- Yanıt veritabanına kaydedildiğinde, SQLite kullanılır. Veritabanı dosyası `api_responses.db` olarak adlandırılır ve yanıtlar `responses` tablosuna kaydedilir.
