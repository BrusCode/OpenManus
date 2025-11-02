# Guia de Variáveis de Ambiente para Easypanel

Este documento lista todas as variáveis de ambiente necessárias para configurar o OpenManus no Easypanel.

## 📋 Variáveis Obrigatórias

Estas variáveis **DEVEM** ser configuradas para o OpenManus funcionar:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `LLM_API_KEY` | Chave de API do provedor de LLM | `sk-proj-abc123...` |

## 🔧 Variáveis Recomendadas

Estas variáveis são recomendadas para personalizar o comportamento:

| Variável | Descrição | Valor Padrão | Exemplo |
|----------|-----------|--------------|---------|
| `LLM_MODEL` | Modelo de LLM a ser usado | `gpt-4o` | `gpt-4o`, `claude-3-7-sonnet-20250219` |
| `LLM_BASE_URL` | URL base da API do LLM | `https://api.openai.com/v1` | `https://api.openai.com/v1` |
| `LLM_MAX_TOKENS` | Máximo de tokens na resposta | `4096` | `4096`, `8192` |
| `LLM_TEMPERATURE` | Controla aleatoriedade (0.0-1.0) | `0.0` | `0.0` (determinístico), `0.7` (criativo) |

## 🎨 Variáveis Opcionais

### Modelo de Visão

Para tarefas que envolvem processamento de imagens:

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `LLM_VISION_MODEL` | Modelo de visão | Mesmo do `LLM_MODEL` |
| `LLM_VISION_API_KEY` | Chave de API para visão | Mesmo do `LLM_API_KEY` |
| `LLM_VISION_BASE_URL` | URL base para visão | Mesmo do `LLM_BASE_URL` |

### Configuração de Navegador

Para automação web com Playwright:

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `BROWSER_HEADLESS` | Executar sem interface gráfica | `true` |
| `BROWSER_DISABLE_SECURITY` | Desabilitar segurança do navegador | `true` |

### Motor de Busca

Configuração para buscas na web:

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `SEARCH_ENGINE` | Motor de busca principal | `Google` |
| `SEARCH_LANG` | Código de idioma | `en` |
| `SEARCH_COUNTRY` | Código de país | `us` |

### Sandbox

Para execução isolada de código:

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `SANDBOX_USE` | Habilitar sandbox | `false` |
| `SANDBOX_MEMORY_LIMIT` | Limite de memória | `1g` |
| `SANDBOX_CPU_LIMIT` | Limite de CPU | `2.0` |

### Agentes Especializados

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `RUNFLOW_USE_DATA_ANALYSIS` | Habilitar agente de análise de dados | `false` |

## 🔐 Configuração de Provedores Específicos

### OpenAI (Padrão)

```
LLM_API_KEY=sk-proj-your-key-here
LLM_MODEL=gpt-4o
LLM_BASE_URL=https://api.openai.com/v1
```

### Anthropic (Claude)

```
LLM_API_KEY=sk-ant-your-key-here
LLM_MODEL=claude-3-7-sonnet-20250219
LLM_BASE_URL=https://api.anthropic.com/v1
```

### Azure OpenAI

```
LLM_API_TYPE=azure
LLM_API_KEY=your-azure-key
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment-id
LLM_API_VERSION=2024-08-01-preview
```

### AWS Bedrock

```
LLM_API_TYPE=aws
LLM_API_KEY=bear
LLM_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
LLM_BASE_URL=bedrock-runtime.us-west-2.amazonaws.com
```

### Ollama (Local)

```
LLM_API_TYPE=ollama
LLM_API_KEY=ollama
LLM_MODEL=llama3.2
LLM_BASE_URL=http://localhost:11434/v1
```

## 📝 Como Configurar no Easypanel

1. Acesse seu projeto no Easypanel
2. Vá para a aba **Environment**
3. Adicione as variáveis uma por uma
4. Clique em **Save** após adicionar todas
5. Faça o **Deploy** da aplicação

## ⚠️ Notas Importantes

- **Nunca** exponha suas chaves de API publicamente
- Use variáveis de ambiente para todas as credenciais sensíveis
- O arquivo `.env` é apenas para desenvolvimento local
- No Easypanel, configure as variáveis através da interface web
- Valores booleanos devem ser `true` ou `false` (minúsculas)

## 🔍 Verificação

Após o deploy, verifique os logs do container para confirmar que a configuração foi gerada corretamente:

```
✅ Arquivo de configuração gerado com sucesso: /app/config/config.toml
📝 Modelo LLM: gpt-4o
🔗 Base URL: https://api.openai.com/v1
🔑 API Key: ****abc123
```

## 🆘 Troubleshooting

### Erro: "LLM_API_KEY não foi definida"

**Solução**: Adicione a variável `LLM_API_KEY` nas configurações de ambiente do Easypanel.

### Erro: "Failed to connect to API"

**Solução**: Verifique se `LLM_BASE_URL` está correto e se sua chave de API é válida.

### Container não inicia

**Solução**: Verifique os logs do container no Easypanel para identificar o erro específico.
