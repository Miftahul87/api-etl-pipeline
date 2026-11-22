from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from .models import ETLRecord
def upsert_records(db,records):
    if not records: return 0
    dialect=db.bind.dialect.name
    if dialect=="postgresql": stmt=pg_insert(ETLRecord).values(records)
    elif dialect=="sqlite": stmt=sqlite_insert(ETLRecord).values(records)
    else:
        count=0
        for item in records:
            existing=db.scalar(select(ETLRecord).where(ETLRecord.external_id==item["external_id"]))
            if existing:
                for k,v in item.items(): setattr(existing,k,v)
            else: db.add(ETLRecord(**item))
            count+=1
        db.commit(); return count
    update_cols={k:getattr(stmt.excluded,k) for k in ("name","email","amount","source_updated_at","payload","loaded_at")}
    stmt=stmt.on_conflict_do_update(index_elements=["external_id"],set_=update_cols)
    db.execute(stmt); db.commit()
    return len(records)
