import httpx
from app.extract import fetch_all_pages
def test_fetches_multiple_pages():
    calls=[]
    def handler(request):
        page=int(request.url.params["page"]); calls.append(page)
        return httpx.Response(200,json={"items":[{"id":page}],"has_more":page<3})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        rows=fetch_all_pages("https://source.test/data",client=client)
    assert [r["id"] for r in rows]==[1,2,3]
    assert calls==[1,2,3]
