from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.controller_ai import router
# Créer une instance de FastAPI
app = FastAPI()

# Définir les origines autorisées (par exemple, votre frontend)
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
