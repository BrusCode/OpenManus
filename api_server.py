#!/usr/bin/env python3
"""
OpenManus API Server
API REST para interagir com o OpenManus via HTTP
"""

import asyncio
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field

from app.agent.manus import Manus
from app.logger import logger

# Configuração da API
app = FastAPI(
    title="OpenManus API",
    description="API REST para interagir com o OpenManus AI Agent",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Armazenamento em memória de tarefas (em produção, use Redis ou banco de dados)
tasks: Dict[str, Dict[str, Any]] = {}

# Diretório de workspace
WORKSPACE_DIR = Path("/app/workspace")
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)


# ============================================
# Modelos Pydantic
# ============================================

class TaskRequest(BaseModel):
    """Requisição para criar uma nova tarefa"""
    prompt: str = Field(..., description="Prompt/instrução para o agente", min_length=1)
    mode: str = Field(default="direct", description="Modo de execução: 'direct', 'flow', ou 'mcp'")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadados adicionais")


class TaskResponse(BaseModel):
    """Resposta com informações da tarefa"""
    task_id: str = Field(..., description="ID único da tarefa")
    status: str = Field(..., description="Status da tarefa: 'pending', 'running', 'completed', 'failed'")
    prompt: str = Field(..., description="Prompt da tarefa")
    mode: str = Field(..., description="Modo de execução")
    created_at: str = Field(..., description="Data/hora de criação")
    started_at: Optional[str] = Field(None, description="Data/hora de início")
    completed_at: Optional[str] = Field(None, description="Data/hora de conclusão")
    result: Optional[str] = Field(None, description="Resultado da tarefa")
    error: Optional[str] = Field(None, description="Mensagem de erro, se houver")
    files: Optional[List[str]] = Field(None, description="Lista de arquivos gerados")


class HealthResponse(BaseModel):
    """Resposta do health check"""
    status: str = Field(..., description="Status do serviço")
    version: str = Field(..., description="Versão da API")
    timestamp: str = Field(..., description="Timestamp atual")


# ============================================
# Funções auxiliares
# ============================================

async def execute_task(task_id: str, prompt: str, mode: str):
    """Executa uma tarefa do OpenManus em background"""
    try:
        # Atualizar status
        tasks[task_id]["status"] = "running"
        tasks[task_id]["started_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Iniciando tarefa {task_id} no modo {mode}")
        
        # Criar agente
        agent = await Manus.create()
        
        try:
            # Executar tarefa
            await agent.run(prompt)
            
            # Listar arquivos gerados no workspace
            task_workspace = WORKSPACE_DIR / task_id
            files = []
            if task_workspace.exists():
                files = [str(f.relative_to(WORKSPACE_DIR)) for f in task_workspace.rglob("*") if f.is_file()]
            
            # Atualizar status de sucesso
            tasks[task_id]["status"] = "completed"
            tasks[task_id]["completed_at"] = datetime.utcnow().isoformat()
            tasks[task_id]["result"] = "Tarefa concluída com sucesso"
            tasks[task_id]["files"] = files
            
            logger.info(f"Tarefa {task_id} concluída com sucesso")
            
        finally:
            # Limpar recursos do agente
            await agent.cleanup()
            
    except Exception as e:
        logger.error(f"Erro ao executar tarefa {task_id}: {str(e)}")
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["completed_at"] = datetime.utcnow().isoformat()
        tasks[task_id]["error"] = str(e)


# ============================================
# Endpoints da API
# ============================================

@app.get("/", response_model=Dict[str, str])
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "OpenManus API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check do serviço"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_request: TaskRequest, background_tasks: BackgroundTasks):
    """
    Cria uma nova tarefa para o OpenManus executar
    
    A tarefa será executada em background e você pode consultar o status usando o task_id retornado.
    """
    # Gerar ID único
    task_id = str(uuid.uuid4())
    
    # Criar entrada da tarefa
    task_data = {
        "task_id": task_id,
        "status": "pending",
        "prompt": task_request.prompt,
        "mode": task_request.mode,
        "created_at": datetime.utcnow().isoformat(),
        "started_at": None,
        "completed_at": None,
        "result": None,
        "error": None,
        "files": None,
        "metadata": task_request.metadata or {}
    }
    
    tasks[task_id] = task_data
    
    # Adicionar tarefa ao background
    background_tasks.add_task(execute_task, task_id, task_request.prompt, task_request.mode)
    
    logger.info(f"Tarefa {task_id} criada e adicionada à fila")
    
    return TaskResponse(**task_data)


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """
    Consulta o status e resultado de uma tarefa
    """
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa {task_id} não encontrada"
        )
    
    return TaskResponse(**tasks[task_id])


@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    status_filter: Optional[str] = None,
    limit: int = 100
):
    """
    Lista todas as tarefas
    
    - **status_filter**: Filtrar por status (pending, running, completed, failed)
    - **limit**: Número máximo de tarefas a retornar
    """
    task_list = list(tasks.values())
    
    # Filtrar por status se especificado
    if status_filter:
        task_list = [t for t in task_list if t["status"] == status_filter]
    
    # Ordenar por data de criação (mais recente primeiro)
    task_list.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Limitar resultados
    task_list = task_list[:limit]
    
    return [TaskResponse(**t) for t in task_list]


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    """
    Remove uma tarefa do sistema
    
    Nota: Isso não interrompe tarefas em execução, apenas remove o registro.
    """
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa {task_id} não encontrada"
        )
    
    del tasks[task_id]
    logger.info(f"Tarefa {task_id} removida")
    
    return None


@app.get("/tasks/{task_id}/files/{file_path:path}")
async def download_file(task_id: str, file_path: str):
    """
    Faz download de um arquivo gerado pela tarefa
    """
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa {task_id} não encontrada"
        )
    
    # Construir caminho completo do arquivo
    full_path = WORKSPACE_DIR / file_path
    
    # Verificar se o arquivo existe
    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Arquivo {file_path} não encontrado"
        )
    
    # Verificar se o arquivo pertence à tarefa
    if not str(full_path).startswith(str(WORKSPACE_DIR / task_id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao arquivo"
        )
    
    return FileResponse(
        path=full_path,
        filename=full_path.name,
        media_type="application/octet-stream"
    )


# ============================================
# Inicialização
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    # Obter porta da variável de ambiente ou usar 8000 como padrão
    port = int(os.getenv("PORT", 8000))
    
    # Iniciar servidor
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
