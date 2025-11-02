# 🚀 Guia de Deploy da OpenManus API no Easypanel

**Autor**: Manus AI
**Data**: 01 de Novembro de 2025

## 📋 Visão Geral

Este guia mostra como fazer o deploy da **OpenManus API** no Easypanel, transformando o OpenManus em um serviço web acessível via HTTP REST.

### O que você terá ao final:

- ✅ API REST rodando no Easypanel
- ✅ Documentação interativa (Swagger UI)
- ✅ Endpoints para criar e gerenciar tarefas
- ✅ Download de arquivos gerados
- ✅ Acesso via domínio personalizado

---

## 🎯 Opções de Deployment

Você tem **2 opções** de deployment:

### Opção 1: CLI Interativo (Modo Padrão)

- Acesso via shell do container
- Ideal para uso manual e testes
- **Dockerfile**: `Dockerfile.easypanel`
- **Start Command**: `tail -f /dev/null`

### Opção 2: API REST (Recomendado para Produção)

- Acesso via HTTP REST
- Ideal para integrações e automações
- **Dockerfile**: `Dockerfile.api`
- **Start Command**: `python api_server.py`

Este guia foca na **Opção 2 (API REST)**.

---

## 📦 Passo a Passo

### Passo 1: Preparar Repositório

Os arquivos necessários já foram criados e enviados para o GitHub:

- ✅ `api_server.py` - Servidor FastAPI
- ✅ `Dockerfile.api` - Dockerfile otimizado para API
- ✅ `docker-compose.api.yml` - Para testes locais
- ✅ `API_DOCUMENTATION.md` - Documentação completa da API

### Passo 2: Criar Serviço no Easypanel

1. Acesse seu **Easypanel Dashboard**
2. Vá para **Projects** → Seu Projeto
3. Clique em **+ New** → **App**

### Passo 3: Configurar Source

1. **Provider**: GitHub
2. **Repository**: `BrusCode/OpenManus`
3. **Branch**: `main`

### Passo 4: Configurar Build

1. **Build Type**: Dockerfile
2. **Dockerfile Path**: `/Dockerfile.api`

### Passo 5: Configurar Environment

Adicione as seguintes variáveis de ambiente:

#### Obrigatórias:

| Key | Value |
|-----|-------|
| `LLM_API_KEY` | `sk-proj-sua-chave-aqui` |

#### Recomendadas:

| Key | Value |
|-----|-------|
| `LLM_MODEL` | `gpt-4o` |
| `LLM_BASE_URL` | `https://api.openai.com/v1` |
| `PORT` | `8000` |
| `BROWSER_HEADLESS` | `true` |

### Passo 6: Configurar Volumes

Adicione os volumes para persistência:

| Volume Name | Container Path |
|-------------|----------------|
| `openmanus-workspace` | `/app/workspace` |
| `openmanus-config` | `/app/config` |
| `openmanus-logs` | `/app/logs` |

### Passo 7: Configurar General Settings

1. **Start Command**:
   ```bash
   python api_server.py
   ```

2. **Port**: `8000`

### Passo 8: Configurar Domínio

1. Vá para a aba **Domains**
2. Clique em **Add Domain**
3. Configure:
   - **Domain**: `openmanus-api.seu-dominio.com` (ou subdomínio do Easypanel)
   - **Port**: `8000`
   - **HTTPS**: Habilitado (recomendado)

### Passo 9: Deploy

1. Clique em **Deploy**
2. Aguarde o build e inicialização
3. Verifique os logs para confirmar que a API iniciou:
   ```
   INFO:     Started server process
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

---

## ✅ Verificação

### 1. Testar Health Check

```bash
curl https://openmanus-api.seu-dominio.com/health
```

**Resposta esperada**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

### 2. Acessar Documentação

Abra no navegador:
```
https://openmanus-api.seu-dominio.com/docs
```

Você verá a interface Swagger UI com todos os endpoints disponíveis.

### 3. Criar uma Tarefa de Teste

```bash
curl -X POST https://openmanus-api.seu-dominio.com/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Escreva um poema sobre IA",
    "mode": "direct"
  }'
```

**Resposta**:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "prompt": "Escreva um poema sobre IA",
  ...
}
```

### 4. Consultar Status da Tarefa

```bash
curl https://openmanus-api.seu-dominio.com/tasks/550e8400-e29b-41d4-a716-446655440000
```

---

## 🔧 Configurações Avançadas

### Aumentar Recursos

Se suas tarefas são complexas, aumente os recursos do container:

1. Vá para **Resources**
2. Configure:
   - **CPU**: 2 cores
   - **Memory**: 2GB

### Configurar CORS

Por padrão, a API aceita requisições de qualquer origem. Para restringir:

Edite `api_server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-frontend.com"],  # Especifique domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Adicionar Autenticação

Para produção, adicione autenticação com API Keys:

1. Crie um middleware de autenticação
2. Valide header `X-API-Key` em cada requisição
3. Armazene chaves válidas em variáveis de ambiente

---

## 📊 Monitoramento

### Logs da Aplicação

No Easypanel, vá para **Logs** para ver:

- Requisições HTTP
- Criação de tarefas
- Erros e exceções

### Métricas

Monitore:

- **CPU/Memory**: Aba **Resources**
- **Requests**: Logs de acesso
- **Erros**: Logs de erro

---

## 🎯 Casos de Uso

### 1. Integração com Frontend

```javascript
// React/Vue/Angular
const createTask = async (prompt) => {
  const response = await fetch('https://openmanus-api.seu-dominio.com/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, mode: 'direct' })
  });
  return await response.json();
};
```

### 2. Webhook/Automação

```python
# Zapier, Make.com, n8n
import requests

def trigger_openmanus(prompt):
    response = requests.post(
        'https://openmanus-api.seu-dominio.com/tasks',
        json={'prompt': prompt, 'mode': 'flow'}
    )
    return response.json()['task_id']
```

### 3. Chatbot Integration

```python
# Discord Bot, Telegram Bot, Slack Bot
@bot.command()
async def ask_manus(ctx, *, question):
    # Criar tarefa no OpenManus
    response = requests.post(
        'https://openmanus-api.seu-dominio.com/tasks',
        json={'prompt': question}
    )
    task_id = response.json()['task_id']
    
    # Aguardar conclusão
    while True:
        status = requests.get(f'https://openmanus-api.seu-dominio.com/tasks/{task_id}')
        task = status.json()
        if task['status'] == 'completed':
            await ctx.send(task['result'])
            break
        await asyncio.sleep(5)
```

---

## 🆘 Troubleshooting

### API não inicia

**Sintomas**: Container reinicia constantemente

**Soluções**:
1. Verifique logs: procure por erros de Python
2. Confirme que `LLM_API_KEY` está definida
3. Verifique se a porta 8000 está correta

### Erro 502 Bad Gateway

**Sintomas**: Erro ao acessar o domínio

**Soluções**:
1. Verifique se o container está rodando
2. Confirme que a porta está configurada como 8000
3. Aguarde alguns segundos após o deploy

### Tarefas ficam em "pending"

**Sintomas**: Tarefas não são executadas

**Soluções**:
1. Verifique logs da aplicação
2. Confirme que a API key do LLM é válida
3. Verifique se há recursos suficientes (CPU/RAM)

### Arquivos não são salvos

**Sintomas**: `files` retorna vazio

**Soluções**:
1. Verifique se os volumes estão configurados
2. Confirme permissões dos diretórios
3. Verifique logs para erros de I/O

---

## 🔐 Segurança em Produção

### Checklist de Segurança:

- [ ] Implementar autenticação (API Keys ou OAuth)
- [ ] Habilitar HTTPS (via Easypanel)
- [ ] Configurar CORS para domínios específicos
- [ ] Adicionar rate limiting
- [ ] Validar e sanitizar inputs
- [ ] Implementar logging de auditoria
- [ ] Usar secrets para chaves sensíveis
- [ ] Configurar firewall se necessário

---

## 📚 Próximos Passos

1. **Adicionar Autenticação**: Implementar sistema de API keys
2. **WebSockets**: Para updates em tempo real
3. **Persistência**: Migrar de memória para Redis/PostgreSQL
4. **Filas**: Implementar Celery ou RQ para melhor gerenciamento
5. **Webhooks**: Notificar URLs quando tarefas concluírem
6. **Frontend**: Criar interface web para interagir com a API

---

## 📖 Documentação Relacionada

- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - Documentação completa da API
- [DEPLOYMENT_EASYPANEL.md](./DEPLOYMENT_EASYPANEL.md) - Deploy do modo CLI
- [EASYPANEL_ENV_GUIDE.md](./EASYPANEL_ENV_GUIDE.md) - Guia de variáveis de ambiente

---

## ✨ Resultado Final

Após seguir este guia, você terá:

- ✅ OpenManus API rodando no Easypanel
- ✅ Endpoint público acessível via HTTPS
- ✅ Documentação interativa (Swagger UI)
- ✅ Pronto para integrações com outras aplicações
- ✅ Escalável e pronto para produção

**URL da API**: `https://openmanus-api.seu-dominio.com`
**Documentação**: `https://openmanus-api.seu-dominio.com/docs`

---

**Dúvidas?** Consulte a [documentação completa da API](./API_DOCUMENTATION.md) ou os logs do Easypanel para troubleshooting.
