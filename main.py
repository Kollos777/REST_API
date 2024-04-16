from REST_API.routes import contact
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI()

app.include_router(contact.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contacts API"}

@app.get("/docs")
def read_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=True
    )
