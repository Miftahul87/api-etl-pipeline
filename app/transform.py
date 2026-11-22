from dataclasses import dataclass
@dataclass
class TransformResult:
    accepted:list[dict]
    rejected:int
def transform_records(raw_records):
    accepted=[]; rejected=0
    for raw in raw_records:
        if not isinstance(raw,dict):
            rejected+=1; continue
        external_id=raw.get("id") or raw.get("external_id")
        name=raw.get("name") or raw.get("title")
        if external_id is None or not isinstance(name,str) or not name.strip():
            rejected+=1; continue
        amount=raw.get("amount")
        try: amount=float(amount) if amount is not None else None
        except (TypeError,ValueError):
            rejected+=1; continue
        email=raw.get("email")
        accepted.append({
            "external_id":str(external_id).strip(),
            "name":name.strip(),
            "email":email.strip().lower() if isinstance(email,str) and email.strip() else None,
            "amount":amount,
            "source_updated_at":str(raw.get("updated_at")) if raw.get("updated_at") is not None else None,
            "payload":raw,
        })
    return TransformResult(accepted=accepted,rejected=rejected)
