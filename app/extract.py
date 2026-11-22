import time
import httpx
from .config import settings
class ExtractionError(RuntimeError): pass
def fetch_all_pages(base_url=None,client=None):
    url=base_url or settings.source_api_url
    owned=client is None
    client=client or httpx.Client(timeout=settings.http_timeout_seconds)
    all_records=[]
    try:
        for page in range(1,settings.source_max_pages+1):
            params={"page":page,"page_size":settings.source_page_size}
            last_error=None
            for attempt in range(settings.max_retries+1):
                try:
                    response=client.get(url,params=params)
                    response.raise_for_status()
                    body=response.json()
                    items=body.get("items")
                    if not isinstance(items,list): raise ExtractionError("Source response must contain an 'items' array.")
                    all_records.extend(items)
                    has_more=body.get("has_more",False)
                    if not has_more: return all_records
                    last_error=None
                    break
                except (httpx.HTTPError,ValueError,ExtractionError) as exc:
                    last_error=exc
                    if attempt < settings.max_retries:
                        time.sleep(settings.retry_backoff_seconds*(2**attempt))
            if last_error: raise ExtractionError(f"Page {page} failed after retries: {last_error}") from last_error
        raise ExtractionError(f"Reached SOURCE_MAX_PAGES={settings.source_max_pages} before source pagination completed.")
    finally:
        if owned: client.close()
