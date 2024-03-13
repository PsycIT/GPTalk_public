# ChatGPT Plugin 으로 등록해서 ChatGPT playground에서도 활용 가능하도록 하는 예제 따라해보려 했으나,
# 'GPTs' 라는 GPT 관련 store 오픈하며 plugin 서비스 제공 중단 상태
# '.rag/main.py' 파일은 제외하고 이외 src 참고하면 될 듯

import json
from fastapi import FastAPI, Response
from models import Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, # 실제 서비스에 필요하진 않지만, ChatGPT Plugin을 테스트 할 떄 로컬에 서버 띄우고 사용하기 위해 필요
                    # cors: client와 server 간의 domain이 달라도 요청을 받겠다는 것(default는 받을 수 없음)
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

faq_db = vectordb.load("prompt-faq.csv")


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open('ai-plugin.json', 'r') as f:
        text = f.read()
        return Response(content=text, media_type="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        return Response(content=text, media_type="text/yaml")


@app.post("/query")
async def query(query: Query):
    vector = vectordb.get_embedding(query.query)

    result = vectordb.search(vector, faq_db)

    return {
        'results': result[:query.top_k]
    }
