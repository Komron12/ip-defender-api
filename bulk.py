from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from .utils import fetch_ip_data, format_response
import asyncio

router = APIRouter()

class BulkRequest(BaseModel):
    ips: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "ips": ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
            }
        }

@router.post("/bulk", summary="Bulk IP Lookup (max 50)")
async def bulk_lookup(request: BulkRequest):
    """
    Bir so'rovda 50 tagacha IP manzilni tekshirish.
    Raqobatchilardan asosiy ustunlik!
    """
    ips = request.ips
    
    if len(ips) == 0:
        raise HTTPException(status_code=400, detail="IP list cannot be empty")
    
    if len(ips) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 IPs allowed per request")
    
    # Barcha IP larni parallel tekshirish
    tasks = [fetch_ip_data(ip.strip()) for ip in ips]
    results_raw = await asyncio.gather(*tasks)
    
    results = [format_response(r) for r in results_raw]
    
    # Statistika
    successful = sum(1 for r in results if r.get("success"))
    high_risk = sum(1 for r in results if r.get("success") and r["security"]["risk_level"] == "high")
    
    return {
        "total": len(ips),
        "successful": successful,
        "failed": len(ips) - successful,
        "summary": {
            "high_risk_ips": high_risk,
            "proxies_detected": sum(1 for r in results if r.get("success") and r["security"]["is_proxy"]),
            "hosting_detected": sum(1 for r in results if r.get("success") and r["security"]["is_hosting"]),
        },
        "results": results
    }