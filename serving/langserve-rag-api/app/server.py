from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from app.chains import llm_chain, json_chain, json_limerick_chain, salesman_chain

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

add_routes(
    app,
    llm_chain,
    path='/llm'
)

add_routes(
    app,
    json_chain,
    path='/json'
)

add_routes(
    app,
    json_limerick_chain,
    path='/limerick'
)


add_routes(
    app,
    salesman_chain,
    path='/salesman'
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
