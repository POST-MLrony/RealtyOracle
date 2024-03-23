from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

client = APIRouter()
templates = Jinja2Templates(directory="templates")


@client.get("/")
async def index(request: Request):
    return HTMLResponse(open("templates/index.html").read())


@client.get("/nn")
async def sign_in(request: Request):
    return HTMLResponse(open("templates/site/nn.html").read())


@client.get("/spb")
async def sign_out(request: Request):
    return HTMLResponse(open("templates/spb.html").read())


@client.get("/second")
async def sign_out(request: Request):
    return HTMLResponse(open("templates/second.html").read())


@client.get("/msk")
async def lk(request: Request):
    return HTMLResponse(open("templates/msk.html").read())


@client.get("/ekb")
async def train(request: Request):
    return HTMLResponse(open("templates/ekb.html").read())


@client.get("/kazan")
async def predict(request: Request):
    return HTMLResponse(open("templates/kazan.html").read())


@client.get("/novosibirsk")
async def predict(request: Request):
    return HTMLResponse(open("templates/kazan.html").read())
