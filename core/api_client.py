import aiohttp
import asyncio
import websockets
import logging
from aiohttp import ClientSession
from .logging_utils import validate_url, add_api_key, handle_rate_limiting


async def async_request_handler(url, method="get", data=None, headers=None, params=None, api_key=None, timeout=10, retries=3, rate_limit_wait=60, content_type="json"):
    if not validate_url(url):
        raise ValueError(f"Geçersiz URL: {url}")

    method = method.lower()

    async with ClientSession() as session:
        for attempt in range(retries):
            try:
                headers = add_api_key(headers, api_key)

                if method == "get":
                    async with session.get(url, headers=headers, params=params, timeout=timeout) as response:
                        r = await response.text()
                        status_code = response.status
                elif method == "post":
                    if content_type == "json":
                        async with session.post(url, headers=headers, json=data, params=params, timeout=timeout) as response:
                            r = await response.text()
                            status_code = response.status
                    elif content_type == "xml":
                        async with session.post(url, headers=headers, data=data, params=params, timeout=timeout) as response:
                            r = await response.text()
                            status_code = response.status
                elif method == "put":
                    async with session.put(url, headers=headers, data=data, params=params, timeout=timeout) as response:
                        r = await response.text()
                        status_code = response.status
                elif method == "delete":
                    async with session.delete(url, headers=headers, params=params, timeout=timeout) as response:
                        r = await response.text()
                        status_code = response.status
                else:
                    raise ValueError(f"Geçersiz HTTP yöntemi: {method}")

                if status_code == 200:
                    return r
                elif status_code == 429:
                    handle_rate_limiting(rate_limit_wait)
                elif status_code == 404:
                    raise Exception("Sayfa bulunamadı (404)")
                elif status_code == 500:
                    raise Exception("Sunucu hatası (500)")
                else:
                    raise Exception(f"Beklenmedik durum kodu: {status_code}")

            except (aiohttp.ClientTimeout, aiohttp.ClientError) as e:
                logging.error(f"{method.upper()} isteği sırasında hata oluştu: {e}")
                if attempt < retries - 1:
                    logging.info(f"Yeniden deneme ({attempt+1}/{retries})...")
                    await asyncio.sleep(2)
                else:
                    raise Exception(f"İstek başarısız oldu: {e}")


async def websocket_handler(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                logging.info(f"WebSocket mesajı alındı: {message}")
            except websockets.ConnectionClosed as e:
                logging.error(f"WebSocket bağlantısı kapandı: {e}")
                break
