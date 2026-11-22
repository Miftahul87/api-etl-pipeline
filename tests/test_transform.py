from app.transform import transform_records
def test_transform_normalizes_and_rejects():
    result=transform_records([
      {"id":1,"name":"  Ada Lovelace ","email":" ADA@EXAMPLE.COM ","amount":"12.5"},
      {"id":2,"name":"  "},
      {"name":"Missing id"},
      {"id":3,"name":"Grace","amount":"not-a-number"},
    ])
    assert len(result.accepted)==1 and result.rejected==3
    row=result.accepted[0]
    assert row["name"]=="Ada Lovelace" and row["email"]=="ada@example.com" and row["amount"]==12.5
