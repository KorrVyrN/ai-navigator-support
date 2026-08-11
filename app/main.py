from fastapi import FastAPI

app = FastAPI(
    title="AI Navigator",
    description="AI-powered platform for predictive incident detection",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "name": "AI Navigator",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
