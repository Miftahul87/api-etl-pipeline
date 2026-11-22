from fastapi import APIRouter,Query
router=APIRouter()
MOCK_DATA=[
 {"id":f"cust-{i:03d}","name":f"Customer {i}","email":f" CUSTOMER{i}@EXAMPLE.COM ","amount":round(i*12.5,2),"updated_at":"2026-01-15T10:00:00Z"}
 for i in range(1,26)
]
# A malformed record is intentionally included to demonstrate reject handling.
MOCK_DATA.insert(7,{"id":"bad-008","name":" ","email":"invalid"})
@router.get("/mock-source")
def mock_source(page:int=Query(1,ge=1),page_size:int=Query(10,ge=1,le=100)):
    start=(page-1)*page_size; items=MOCK_DATA[start:start+page_size]
    return {"items":items,"page":page,"page_size":page_size,"has_more":start+page_size<len(MOCK_DATA)}
