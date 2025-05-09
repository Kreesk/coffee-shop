from .routes import app
from .db import init_db
import uvicorn

@app.on_event("startup")
def startup():
    init_db()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)