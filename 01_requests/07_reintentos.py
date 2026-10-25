import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("integracion")

reintentos = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)

session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=reintentos))

for status in [200, 404, 503]:
    url = f"https://httpbin.org/status/{status}"
    log.info("Pidiendo %s", url)
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        log.info("OK: %s", r.status_code)
    except requests.exceptions.RetryError:
        log.error("Fallo después de varios reintentos: %s", url)
    except requests.exceptions.HTTPError as e:
        log.error("Error HTTP sin reintento: %s", e)