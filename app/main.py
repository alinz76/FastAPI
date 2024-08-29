# from database import engine
from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import models
from .routes import posts, users, authorize, vote


# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


app.include_router(posts.route)
app.include_router(users.route)
app.include_router(authorize.route)
app.include_router(vote.route)

@app.get('/')
def root():
    return{'message': 'Hey there, welcome to my API!'}