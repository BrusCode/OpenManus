# 🌐 OpenManus API - Documentação

**Versão**: 1.0.0
**Autor**: Manus AI

## 📋 Visão Geral

A **OpenManus API** é uma interface REST que permite interagir com o agente OpenManus através de requisições HTTP. Isso possibilita a integração do OpenManus com outras aplicações, automações e serviços web.

### Principais Recursos

- **Execução Assíncrona**: Tarefas são executadas em background
- **Gerenciamento de Tarefas**: Criar, consultar, listar e deletar tarefas
- **Download de Arquivos**: Baixar arquivos gerados pelo agente
- **Documentação Interativa**: Swagger UI e ReDoc integrados
- **CORS Habilitado**: Permite chamadas de diferentes origens

---

## 🚀 Como Usar

### Iniciando o Servidor

#### Método 1: Diretamente com Python

```bash
python api_server.py
```

#### Método 2: Com Uvicorn

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

#### Método 3: No Easypanel

Configure o **Start Command** como:

```bash
python api_server.py
```

Ou:

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### Acessando a Documentação Interativa

Após iniciar o servidor, acesse:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📡 Endpoints

### 1. Root

**GET** `/`

Retorna informações básicas da API.

**Resposta**:
```json
{
  "message": "OpenManus API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 2. Health Check

**GET** `/health`

Verifica o status do serviço.

**Resposta**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

---

### 3. Criar Tarefa

**POST** `/tasks`

Cria uma nova tarefa para o OpenManus executar.

**Body**:
```json
{
  "prompt": "Crie um site simples sobre a história da computação",
  "mode": "direct",
  "metadata": {
    "user_id": "123",
    "priority": "high"
  }
}
```

**Parâmetros**:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `prompt` | string | Sim | Instrução para o agente |
| `mode` | string | Não | Modo de execução: `direct`, `flow`, `mcp` (padrão: `direct`) |
| `metadata` | object | Não | Metadados adicionais |

**Resposta** (201 Created):
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "prompt": "Crie um site simples sobre a história da computação",
  "mode": "direct",
  "created_at": "2025-11-01T12:00:00.000000",
  "started_at": null,
  "completed_at": null,
  "result": null,
  "error": null,
  "files": null
}
```

---

### 4. Consultar Tarefa

**GET** `/tasks/{task_id}`

Consulta o status e resultado de uma tarefa específica.

**Parâmetros**:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `task_id` | string (path) | ID da tarefa |

**Resposta** (200 OK):
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "prompt": "Crie um site simples sobre a história da computação",
  "mode": "direct",
  "created_at": "2025-11-01T12:00:00.000000",
  "started_at": "2025-11-01T12:00:05.000000",
  "completed_at": "2025-11-01T12:05:30.000000",
  "result": "Tarefa concluída com sucesso",
  "error": null,
  "files": [
    "550e8400-e29b-41d4-a716-446655440000/index.html",
    "550e8400-e29b-41d4-a716-446655440000/style.css"
  ]
}
```

**Status da Tarefa**:

| Status | Descrição |
|--------|-----------|
| `pending` | Tarefa criada, aguardando execução |
| `running` | Tarefa em execução |
| `completed` | Tarefa concluída com sucesso |
| `failed` | Tarefa falhou |

---

### 5. Listar Tarefas

**GET** `/tasks`

Lista todas as tarefas.

**Query Parameters**:

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `status_filter` | string | Filtrar por status: `pending`, `running`, `completed`, `failed` |
| `limit` | integer | Número máximo de tarefas (padrão: 100) |

**Exemplo**:
```
GET /tasks?status_filter=completed&limit=10
```

**Resposta** (200 OK):
```json
[
  {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "prompt": "Crie um site simples sobre a história da computação",
    "mode": "direct",
    "created_at": "2025-11-01T12:00:00.000000",
    ...
  }
]
```

---

### 6. Deletar Tarefa

**DELETE** `/tasks/{task_id}`

Remove uma tarefa do sistema.

**Parâmetros**:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `task_id` | string (path) | ID da tarefa |

**Resposta** (204 No Content)

**Nota**: Isso não interrompe tarefas em execução, apenas remove o registro.

---

### 7. Download de Arquivo

**GET** `/tasks/{task_id}/files/{file_path}`

Faz download de um arquivo gerado pela tarefa.

**Parâmetros**:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `task_id` | string (path) | ID da tarefa |
| `file_path` | string (path) | Caminho relativo do arquivo |

**Exemplo**:
```
GET /tasks/550e8400-e29b-41d4-a716-446655440000/files/550e8400-e29b-41d4-a716-446655440000/index.html
```

**Resposta**: Arquivo para download

---

## 💻 Exemplos de Uso

### Python (requests)

```python
import requests
import time

# URL base da API
BASE_URL = "http://localhost:8000"

# 1. Criar tarefa
response = requests.post(
    f"{BASE_URL}/tasks",
    json={
        "prompt": "Analise os dados de vendas e crie um gráfico",
        "mode": "direct"
    }
)
task = response.json()
task_id = task["task_id"]
print(f"Tarefa criada: {task_id}")

# 2. Aguardar conclusão
while True:
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    task = response.json()
    
    if task["status"] in ["completed", "failed"]:
        break
    
    print(f"Status: {task['status']}")
    time.sleep(5)

# 3. Verificar resultado
if task["status"] == "completed":
    print(f"Resultado: {task['result']}")
    print(f"Arquivos: {task['files']}")
else:
    print(f"Erro: {task['error']}")
```

### cURL

```bash
# Criar tarefa
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crie um resumo sobre IA",
    "mode": "direct"
  }'

# Consultar tarefa
curl http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000

# Listar tarefas concluídas
curl "http://localhost:8000/tasks?status_filter=completed&limit=5"

# Download de arquivo
curl -O http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000/files/550e8400-e29b-41d4-a716-446655440000/output.txt
```

### JavaScript (fetch)

```javascript
// Criar tarefa
const response = await fetch('http://localhost:8000/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    prompt: 'Crie uma apresentação sobre machine learning',
    mode: 'flow'
  })
});

const task = await response.json();
console.log('Tarefa criada:', task.task_id);

// Consultar status
const statusResponse = await fetch(`http://localhost:8000/tasks/${task.task_id}`);
const taskStatus = await statusResponse.json();
console.log('Status:', taskStatus.status);
```

---

## 🔧 Configuração no Easypanel

### 1. Atualizar Start Command

No Easypanel, configure o **Start Command** para iniciar a API:

```bash
python api_server.py
```

### 2. Configurar Domínio

1. Vá para a aba **Domains**
2. Adicione um domínio (ex: `openmanus-api.seu-dominio.com`)
3. Configure o **Port** como `8000`

### 3. Variáveis de Ambiente

Adicione as mesmas variáveis de ambiente do deployment padrão:

```
LLM_API_KEY=sk-proj-sua-chave-aqui
LLM_MODEL=gpt-4o
PORT=8000
```

### 4. Deploy

Faça o deploy e acesse:

- API: `https://openmanus-api.seu-dominio.com`
- Docs: `https://openmanus-api.seu-dominio.com/docs`

---

## 🔒 Segurança

### Considerações Importantes

1. **Autenticação**: A API atual não possui autenticação. Em produção, implemente:
   - API Keys
   - OAuth 2.0
   - JWT Tokens

2. **Rate Limiting**: Implemente limitação de taxa para evitar abuso

3. **CORS**: Configure origens permitidas em produção:
   ```python
   allow_origins=["https://seu-frontend.com"]
   ```

4. **HTTPS**: Sempre use HTTPS em produção

5. **Validação**: A API valida inputs, mas adicione validações extras conforme necessário

---

## 📊 Monitoramento

### Logs

Os logs da API são gerenciados pelo Loguru e incluem:

- Criação de tarefas
- Início e conclusão de execuções
- Erros e exceções

### Métricas Recomendadas

- Número de tarefas criadas
- Taxa de sucesso/falha
- Tempo médio de execução
- Uso de recursos (CPU, memória)

---

## 🆘 Troubleshooting

### Erro: "Tarefa não encontrada"

**Causa**: O task_id não existe ou foi deletado.

**Solução**: Verifique se o task_id está correto.

### Erro: "Arquivo não encontrado"

**Causa**: O arquivo não foi gerado pela tarefa ou o caminho está incorreto.

**Solução**: Liste os arquivos da tarefa primeiro usando o endpoint `/tasks/{task_id}`.

### API não inicia

**Causa**: Porta 8000 já está em uso ou variáveis de ambiente faltando.

**Solução**: 
- Mude a porta: `PORT=8001 python api_server.py`
- Verifique `LLM_API_KEY`

---

## 🚀 Próximos Passos

1. **Adicionar Autenticação**: Implementar sistema de API keys
2. **WebSockets**: Para atualizações em tempo real do status
3. **Persistência**: Usar Redis ou banco de dados para armazenar tarefas
4. **Filas**: Implementar sistema de filas (Celery, RQ) para melhor gerenciamento
5. **Webhooks**: Notificar URLs externas quando tarefas concluírem

---

## 📚 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenManus GitHub](https://github.com/FoundationAgents/OpenManus)
- [Pydantic Documentation](https://docs.pydantic.dev/)
