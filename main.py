from fastapi import FastAPI
app = FastAPI()
@app.get("/")
# ...
async def root():
    return {"message": "Meu CI/CD com ArgoCD funciona!"} [cite: 67]
# ...
