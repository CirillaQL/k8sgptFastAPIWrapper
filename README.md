# k8sgptFastAPIWrapper
A project that wraps the k8sgpt tool using FastAPI

## Build
1. Build
`docker build -t k8sgpt-fastapi:latest .`
2. Run
`docker run -p 8000:8000 --name=k8sgpt-fastapi -d k8sgpt-fastapi:latest`

## How to use
1. set backend
POST localhost:8000/auth/add 
{
    "kind": "bedrock",
    "ak": "ak",
    "sk": "sk",
    "region": "region",
    "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
}

2.analyze
POST localhost:8000/analyze
{
    "namespace": "namespace",
    "backend": "amazonbedrock",
    "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
}