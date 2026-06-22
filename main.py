from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import single, bulk

app = FastAPI(
    title="IP Geolocation & Security API",
    description="""
## 🌍 IP Geolocation & Security API

Professional IP lookup API with security intelligence.

### Features:
- 📍 **Geolocation** — Country, city, coordinates, timezone
- 🌐 **Network Info** — ISP, ASN, reverse DNS
- 🔒 **Security** — VPN/Proxy/Hosting detection
- ⚡ **Risk Score** — 0-100 fraud risk assessment
- 📦 **Bulk Lookup** — Up to 50 IPs per request

### Endpoints:
- `GET /lookup?ip=8.8.8.8` — Single IP lookup
- `GET /myip` — Your own IP info
- `POST /bulk` — Bulk IP lookup
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    }
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerlarni ulash
app.include_router(single.router, tags=["IP Lookup"])
app.include_router(bulk.router, tags=["Bulk Lookup"])

@app.get("/", tags=["Health"])
async def root():
    return {
        "name": "IP Geolocation & Security API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "single_lookup": "/lookup?ip=8.8.8.8",
            "my_ip": "/myip",
            "bulk_lookup": "/bulk"
        }
    }

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}