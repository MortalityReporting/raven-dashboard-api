from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from api.utils.setup import set_up

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def pass_through(path: str, request: Request):
    client = AsyncClient()
    config = set_up()
    url = f"{config['UPLOAD_FILE_PASSTHROUGH_URL']}/{path}"
    
    req = client.build_request(
        request.method, 
        url,
        headers=request.headers.raw,
        params=request.query_params,
        content=await request.body()
    )
    resp = await client.send(req)
    await client.aclose()

    return Response(resp.content, status_code=resp.status_code, headers=resp.headers)    