from fastapi import APIRouter, Query, HTTPException
from .utils import fetch_ip_data, format_response
import httpx

router = APIRouter()

@router.get("/lookup", summary="Single IP Lookup")
async def lookup_ip(
    ip: str = Query(..., description="IP address to lookup", example="8.8.8.8")
):
    """
    Bitta IP manzil haqida to'liq ma'lumot:
    - 📍 Joylashuv (mamlakat, shahar, koordinatlar)
    - 🌐 Tarmoq (ISP, ASN)
    - 🔒 Xavfsizlik (Proxy/VPN/Hosting aniqlash + Risk score)
    """
    # IP formatini tekshirish
    import re
    ip = ip.strip()
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    
    if not (re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip)):
        raise HTTPException(status_code=400, detail="Invalid IP address format")
    
    data = await fetch_ip_data(ip)
    return format_response(data)

@router.get("/myip", summary="Get My IP Info")
async def my_ip(request_ip: str = Query(None, include_in_schema=False)):
    """
    So'rov yuborayotgan foydalanuvchining o'z IP manzili haqida ma'lumot
    """
    # Public IP olish
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            res = await client.get("https://api.ipify.org?format=json")
            ip = res.json().get("ip", "8.8.8.8")
        except:
            ip = "8.8.8.8"
    
    data = await fetch_ip_data(ip)
    return format_response(data)