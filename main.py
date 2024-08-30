from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import uvicorn
import os

app = FastAPI()

class AuthBackend(BaseModel):
    kind: str
    model: str
    ak: str = None
    sk: str = None
    region: str = None
    api_key: str = None
    url: str = None

class AnalyzeRequest(BaseModel):
    resource: str = None
    namespace: str = None
    backend: str
    anonymize: bool = False

@app.get("/")
async def healthz():
    return {"message": "ok"}

@app.post("/auth/add")
async def auth(auth_backend: AuthBackend):
    if auth_backend.kind == "bedrock":
        os.environ['AWS_ACCESS_KEY'] = auth_backend.ak
        os.environ['AWS_SECRET_ACCESS_KEY'] = auth_backend.sk
        os.environ['AWS_DEFAULT_REGION'] = auth_backend.region

        command = ["k8sgpt", "auth","add", "--backend", "amazonbedrock", "--model", auth_backend.model, "--providerRegion", auth_backend.region]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return {"message": result.stdout, "code": 0}
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败。错误代码: {e.returncode}")
            print("错误输出:")
            print(e.stderr)
            return {"message": e, "code": 1001}
    return {"message": "ok"}

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    command = ["k8sgpt", "analyze", "--explain"]
    if req.resource is not None:
        command.append(f'--filter={req.resource}')
    if req.namespace is not None:
        command.append(f'--namespace={req.namespace}')
    command.append('--output=json')
    if req.anonymize:
        command.append('--anonymize')
    command.append('--backend')
    command.append(req.backend)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return {'message': result.stdout, "code": 0}
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败。错误代码: {e.returncode}")
        print("错误输出:")
        print(e.stderr)
        return {"message": e, "code": 1002}
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")