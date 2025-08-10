import logging
import sys
import traceback
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from database import database, engine, metadata
from models import urls, clicks, generate_short_code
import datetime
from dateutil import parser  # pip install python-dateutil

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

metadata.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return "http://" + url
    return url

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    query = urls.select()
    all_urls = await database.fetch_all(query)
    return templates.TemplateResponse("index.html", {"request": request, "urls": all_urls})

@app.post("/shorten", response_class=HTMLResponse)
async def shorten_url(request: Request, original_url: str = Form(...)):
    original_url = normalize_url(original_url)

    query = urls.select().where(urls.c.original_url == original_url)
    existing_url = await database.fetch_one(query)

    if existing_url:
        short_code = existing_url["short_code"]
    else:
        short_code = generate_short_code()
        expire_at = datetime.datetime.utcnow() + datetime.timedelta(days=30)  # 30 days expiry
        query = urls.insert().values(
            original_url=original_url,
            short_code=short_code,
            created_at=datetime.datetime.utcnow(),
            expire_at=expire_at,
        )
        await database.execute(query)
    
    return templates.TemplateResponse("shorten.html", {"request": request, "short_code": short_code, "original_url": original_url})

@app.get("/{short_code}")
async def redirect_to_url(short_code: str, request: Request):
    query = urls.select().where(urls.c.short_code == short_code)
    url_obj = await database.fetch_one(query)

    if url_obj:
        expire_at_raw = url_obj["expire_at"]
        if expire_at_raw:
            expire_at = expire_at_raw
            if isinstance(expire_at_raw, str):
                expire_at = parser.parse(expire_at_raw)
            if expire_at < datetime.datetime.utcnow():
                raise HTTPException(status_code=410, detail="URL expired")

        click_query = clicks.insert().values(
            url_id=url_obj["id"],
            timestamp=datetime.datetime.utcnow(),
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
        )
        await database.execute(click_query)

        return RedirectResponse(url_obj["original_url"])

    raise HTTPException(status_code=404, detail="URL not found")


@app.get("/analytics/{short_code}", response_class=HTMLResponse)
async def analytics(request: Request, short_code: str):
    query = urls.select().where(urls.c.short_code == short_code)
    url_obj = await database.fetch_one(query)

    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")

    click_query = clicks.select().where(clicks.c.url_id == url_obj["id"]).order_by(clicks.c.timestamp.desc())
    click_records = await database.fetch_all(click_query)

    total_clicks = len(click_records)

    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "url_obj": url_obj,
        "clicks": click_records,
        "total_clicks": total_clicks
    })
