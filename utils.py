import httpx
import asyncio

async def fetch_ip_data(ip: str) -> dict:
    """ip-api.com dan bepul ma'lumot olish"""
    fields = "status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                f"http://ip-api.com/json/{ip}",
                params={"fields": fields}
            )
            data = response.json()
            return data
        except Exception as e:
            return {"status": "fail", "message": str(e), "query": ip}

def calculate_risk_score(data: dict) -> int:
    """VPN/Proxy/Hosting asosida risk score hisoblash"""
    score = 0
    if data.get("proxy"):
        score += 40
    if data.get("hosting"):
        score += 30
    if data.get("mobile"):
        score += 10
    if data.get("status") == "fail":
        score += 50
    return min(score, 100)

def format_response(data: dict) -> dict:
    """Javobni chiroyli formatga o'tkazish"""
    if data.get("status") == "fail":
        return {
            "success": False,
            "error": data.get("message", "Invalid IP"),
            "ip": data.get("query")
        }
    
    risk_score = calculate_risk_score(data)
    
    return {
        "success": True,
        "ip": data.get("query"),
        "location": {
            "country": data.get("country"),
            "country_code": data.get("countryCode"),
            "region": data.get("regionName"),
            "region_code": data.get("region"),
            "city": data.get("city"),
            "zip": data.get("zip"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "timezone": data.get("timezone"),
        },
        "network": {
            "isp": data.get("isp"),
            "org": data.get("org"),
            "as": data.get("as"),
            "as_name": data.get("asname"),
            "reverse_dns": data.get("reverse"),
        },
        "security": {
            "is_proxy": data.get("proxy", False),
            "is_vpn": data.get("proxy", False),
            "is_hosting": data.get("hosting", False),
            "is_mobile": data.get("mobile", False),
            "risk_score": risk_score,
            "risk_level": "high" if risk_score >= 60 else "medium" if risk_score >= 30 else "low"
        }
    }