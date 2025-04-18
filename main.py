from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.schema import schema
from fastapi.staticfiles import StaticFiles

app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
app.mount("/", StaticFiles(directory="static", html=True), name="static")

