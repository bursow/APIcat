import json
import pandas as pd
import yaml
from io import StringIO
import logging

def save_response_to_file(response_text, file_name="response_output", format="json"):
    try:
        if format == "json":
            data = json.loads(response_text)
            with open(f"{file_name}.json", "w") as f:
                json.dump(data, f, indent=4)
            logging.info(f"Yanıt JSON formatında {file_name}.json dosyasına kaydedildi.")

        elif format == "xml":
            with open(f"{file_name}.xml", "w") as f:
                f.write(response_text)
            logging.info(f"Yanıt XML formatında {file_name}.xml dosyasına kaydedildi.")

        elif format == "csv":
            df = pd.read_csv(StringIO(response_text))
            df.to_csv(f"{file_name}.csv", index=False)
            logging.info(f"Yanıt CSV formatında {file_name}.csv dosyasına kaydedildi.")

        elif format == "yaml":
            data = json.loads(response_text)
            with open(f"{file_name}.yaml", "w") as f:
                yaml.dump(data, f)
            logging.info(f"Yanıt YAML formatında {file_name}.yaml dosyasına kaydedildi.")

        else:
            raise ValueError("Geçersiz dosya formatı.")

    except Exception as e:
        logging.error(f"Yanıt dosyaya kaydedilirken hata oluştu: {e}")
