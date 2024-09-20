


import argparse
import asyncio
import logging
from core import async_request_handler, websocket_handler, init_db, save_response_to_file, process_response, schedule_requests, setup_logging, save_response_to_db
import pandas as pd

"""
API key kullanımı için doğru kullanım:

    python3 main.py --url "http://example/example" --async_  --api-key tHs6A8AuYlrLxUhOnnvw8giJDQodEjBH --save-file --db-save

Standart Request kullanımı:

    python3 main.py --url "https://example/exampla" --method get --save-file --format json 

"""


ascii_art = r"""


                     /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\ 
                    ( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )
                    > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ < 
                     /\_/\       _    ____ ___          _      /\_/\ 
                    ( o.o )     / \  |  _ \_ _|___ __ _| |_   ( o.o )
                    > ^ <     / _ \ | |_) | |/ __/ _` | __|   > ^ < 
                     /\_/\    / ___ \|  __/| | (_| (_| | |_    /\_/\ 
                    ( o.o )  /_/   \_\_|  |___\___\__,_|\__|  ( o.o )
                    > ^ <                                     > ^ < 
                     /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\ 
                    ( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )
                    > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ < 

"""

print(ascii_art)

def parse_arguments():
    parser = argparse.ArgumentParser(description="APIcat")
    parser.add_argument('--url', required=True, help="API URL veya WebSocket URI")
    parser.add_argument('--method', default="get", choices=["get", "post", "put", "delete"], help="HTTP yöntemi")
    parser.add_argument('--save-file', action="store_true", help="Yanıtı dosyaya kaydet")
    parser.add_argument('--api-key', help="API anahtarı")
    parser.add_argument('--db-save', action="store_true", help="Yanıtı veritabanına kaydet")
    parser.add_argument('--format', choices=["json", "xml", "csv", "yaml"], default="json", help="Dosya formatı")
    parser.add_argument('--async_', action="store_true", help="Asenkron istekleri etkinleştir")  
    parser.add_argument('--scheduler', action="store_true", help="Zamanlanmış görevleri etkinleştir")
    parser.add_argument('--ws', action="store_true", help="WebSocket bağlantısı kur")
    return parser.parse_args()

def main():
    setup_logging()
    args = parse_arguments()

    conn = init_db() if args.db_save else None

    try:
        if args.ws:
            asyncio.run(websocket_handler(args.url))

        elif args.async_:
            if args.scheduler:
                schedule_requests(args.url, args.method, interval=3600)
                while True:
                    asyncio.sleep(1)
            else:
                response_text = asyncio.run(async_request_handler(args.url, args.method, api_key=args.api_key))
                content_type = 'application/json'
                processed_data = process_response(response_text, content_type)

                if isinstance(processed_data, pd.DataFrame):
                    print(processed_data.head())
                else:
                    print(processed_data)

                if args.save_file:
                    save_response_to_file(response_text, format=args.format)

                if conn:
                    save_response_to_db(conn, args.url, args.method, 200, response_text)

        else:
            import requests
            response = requests.request(method=args.method, url=args.url, headers={"Authorization": f"Bearer {args.api_key}"})
            content_type = response.headers.get('Content-Type', 'text/plain')
            processed_data = process_response(response.text, content_type)

            if isinstance(processed_data, pd.DataFrame):
                print(processed_data.head())
            else:
                print(processed_data)

            if args.save_file:
                save_response_to_file(response.text, format=args.format)

            if conn:
                save_response_to_db(conn, args.url, args.method, response.status_code, response.text)

    except Exception as e:
        logging.error(f"İşlem sırasında hata oluştu: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
