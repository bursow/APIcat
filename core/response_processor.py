import json
import pandas as pd
import yaml
import logging
from io import StringIO

def process_response(response_text, content_type):
    if 'application/json' in content_type:
        logging.info("Yanıt JSON formatında.")
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            raise Exception("JSON yanıtı işlenemiyor.")

    elif 'application/xml' in content_type or 'text/xml' in content_type:
        logging.info("Yanıt XML formatında.")
        try:
            # Wrap the XML string in a StringIO object
            xml_data = StringIO(response_text)
            df = pd.read_xml(xml_data)
            return df
        except ValueError:
            raise Exception("XML yanıtı işlenemiyor.")
        except Exception as e:
            raise Exception(f"XML yanıtı işlenirken bir hata oluştu: {e}")

    elif 'text/csv' in content_type:
        logging.info("Yanıt CSV formatında.")
        try:
            df = pd.read_csv(StringIO(response_text))
            return df
        except ValueError:
            raise Exception("CSV yanıtı işlenemiyor.")
        except Exception as e:
            raise Exception(f"CSV yanıtı işlenirken bir hata oluştu: {e}")

    elif 'application/x-yaml' in content_type:
        logging.info("Yanıt YAML formatında.")
        try:
            return yaml.safe_load(response_text)
        except yaml.YAMLError:
            raise Exception("YAML yanıtı işlenemiyor.")
        except Exception as e:
            raise Exception(f"YAML yanıtı işlenirken bir hata oluştu: {e}")

    else:
        logging.info("Yanıt metin formatında.")
        return response_text
