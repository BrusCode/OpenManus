# 🚀 OpenManus - Deployment no Easypanel

## 📦 Arquivos de Configuração Criados

Este repositório contém arquivos otimizados para deployment no **Easypanel**:

| Arquivo | Descrição |
|---------|-----------|
| `Dockerfile.easypanel` | Dockerfile otimizado para produção com Playwright |
| `docker-compose.yml` | Configuração para testes locais |
| `generate_config.py` | Script que gera `config.toml` de variáveis de ambiente |
| `entrypoint.sh` | Script de inicialização do container |
| `.env.example` | Exemplo de variáveis de ambiente |
| `EASYPANEL_ENV_GUIDE.md` | Guia detalhado de configuração de variáveis |
| `DEPLOYMENT_EASYPANEL.md` | Guia completo de deployment |

---

## ⚡ Quick Start

### 1. Configurar no Easypanel

1. **Criar novo App** no Easypanel
2. **Source**: GitHub → `BrusCode/OpenManus`
3. **Build**: Dockerfile → `/Dockerfile.easypanel`
4. **Environment**: Adicionar variáveis (ver abaixo)
5. **Volumes**: Configurar persistência
6. **Deploy**!

### 2. Variáveis de Ambiente Obrigatórias

```bash
LLM_API_KEY=sk-proj-sua-chave-aqui
```

### 3. Variáveis Recomendadas

```bash
LLM_MODEL=gpt-4o
LLM_BASE_URL=https://api.openai.com/v1
LLM_MAX_TOKENS=4096
LLM_TEMPERATURE=0.0
```

---

## 📚 Documentação Completa

- **[DEPLOYMENT_EASYPANEL.md](./DEPLOYMENT_EASYPANEL.md)**: Guia passo a passo completo
- **[EASYPANEL_ENV_GUIDE.md](./EASYPANEL_ENV_GUIDE.md)**: Todas as variáveis de ambiente disponíveis

---

## 🔧 Volumes Recomendados

| Volume | Path no Container |
|--------|-------------------|
| `openmanus-workspace` | `/app/workspace` |
| `openmanus-config` | `/app/config` |
| `openmanus-logs` | `/app/logs` |

---

## 🎯 Comandos de Start

### Manter container rodando (para acesso via shell):
```bash
tail -f /dev/null
```

### Executar tarefa específica:
```bash
python main.py --prompt "Sua tarefa aqui"
```

### Modo Flow (tarefas complexas):
```bash
python run_flow.py
```

---

## 🐳 Teste Local com Docker

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas credenciais
nano .env

# Iniciar com docker-compose
docker-compose up -d

# Acessar shell do container
docker-compose exec openmanus bash

# Executar OpenManus
python main.py
```

---

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/BrusCode/OpenManus/issues)
- **Documentação Original**: [FoundationAgents/OpenManus](https://github.com/FoundationAgents/OpenManus)

---

## 📝 Licença

MIT License - Ver [LICENSE](./LICENSE)
