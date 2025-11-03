# 🧪 Guia de Teste via CLI - OpenManus no Easypanel

**Autor**: Manus AI
**Data**: 03 de Novembro de 2025

## 🎉 Parabéns! O Build foi Concluído com Sucesso!

Agora vamos testar o OpenManus via CLI (Command Line Interface) antes de ativar a API web.

---

## 📋 Pré-requisitos

- ✅ Container rodando no Easypanel
- ✅ Variáveis de ambiente configuradas
- ✅ Build concluído com sucesso

---

## 🔧 Passo 1: Acessar o Shell do Container

### No Easypanel:

1. Vá para o seu serviço **OpenManus**
2. Clique na aba **Shell** ou **Terminal**
3. Você verá um terminal interativo conectado ao container

**Alternativa via CLI local** (se tiver acesso SSH ao servidor):
```bash
docker exec -it <container-id> bash
```

---

## 🧪 Passo 2: Verificar Instalação

### 2.1. Verificar Python e Dependências

```bash
# Verificar versão do Python
python --version
# Deve retornar: Python 3.12.x

# Verificar se o OpenManus está instalado
ls -la /app/
# Deve listar: main.py, run_flow.py, api_server.py, etc.

# Verificar configuração
cat /app/config/config.toml
# Deve mostrar as configurações geradas
```

### 2.2. Verificar Playwright

```bash
# Verificar se o Chromium foi instalado
playwright --version
# Deve retornar a versão do Playwright

# Listar browsers instalados
ls -la /root/.cache/ms-playwright/
# Deve mostrar: chromium-xxxx/
```

---

## 🚀 Passo 3: Executar Testes Simples

### Teste 1: Tarefa Simples (Modo Direto)

```bash
cd /app
python main.py "Escreva um poema curto sobre inteligência artificial"
```

**O que esperar**:
- O agente vai processar a requisição
- Vai gerar o poema
- Salvar em `/app/workspace/`

**Tempo estimado**: 10-30 segundos

### Teste 2: Tarefa com Busca na Web

```bash
python main.py "Pesquise as últimas notícias sobre IA no Brasil e faça um resumo"
```

**O que esperar**:
- O agente vai usar o Google Search
- Vai buscar informações
- Vai criar um resumo
- Salvar em `/app/workspace/`

**Tempo estimado**: 30-60 segundos

### Teste 3: Tarefa Complexa (Modo Flow)

```bash
python run_flow.py "Crie um relatório sobre as tendências de IA em 2025 com gráficos"
```

**O que esperar**:
- O agente vai planejar as etapas
- Vai pesquisar informações
- Vai criar gráficos (se o agente de análise de dados estiver ativo)
- Vai gerar um relatório HTML
- Salvar em `/app/workspace/`

**Tempo estimado**: 2-5 minutos

---

## 📂 Passo 4: Verificar Resultados

### 4.1. Listar Arquivos Gerados

```bash
# Ver estrutura do workspace
ls -la /app/workspace/

# Ver conteúdo de um arquivo específico
cat /app/workspace/<nome-do-arquivo>

# Para arquivos HTML, você pode baixá-los via Easypanel
```

### 4.2. Baixar Arquivos via Easypanel

**Opção 1: Via Shell**
```bash
# Copiar arquivo para um local acessível
cp /app/workspace/resultado.html /app/logs/resultado.html
```

Depois, acesse via **Logs** ou **Files** no Easypanel.

**Opção 2: Via API (se já estiver rodando)**
```bash
curl http://localhost:8000/tasks/<task_id>/files/<file_path>
```

---

## 🔍 Passo 5: Verificar Logs

### 5.1. Logs da Aplicação

```bash
# Ver logs em tempo real
tail -f /app/logs/*.log

# Ver últimas 50 linhas
tail -n 50 /app/logs/*.log
```

### 5.2. Logs do Easypanel

No Easypanel, vá para a aba **Logs** para ver:
- Logs de inicialização
- Logs de execução
- Erros (se houver)

---

## 🧪 Testes Avançados

### Teste 4: Automação de Navegador

```bash
python main.py "Acesse o site wikipedia.org e extraia informações sobre Python"
```

**O que esperar**:
- O Playwright vai abrir o Chromium
- Vai navegar até o site
- Vai extrair informações
- Vai salvar o resultado

### Teste 5: Análise de Dados

```bash
python run_flow.py "Crie um gráfico de barras com dados fictícios de vendas mensais"
```

**O que esperar**:
- O agente vai gerar dados fictícios
- Vai criar um gráfico usando matplotlib
- Vai salvar como imagem PNG

### Teste 6: Web Scraping

```bash
python main.py "Faça scraping do site example.com e extraia todos os links"
```

**O que esperar**:
- O Crawl4ai vai fazer o scraping
- Vai extrair os links
- Vai salvar em um arquivo

---

## ⚠️ Troubleshooting

### Erro: "No module named 'app'"

**Causa**: Não está no diretório correto.

**Solução**:
```bash
cd /app
python main.py "seu prompt aqui"
```

### Erro: "API key not found"

**Causa**: Variável de ambiente `LLM_API_KEY` não está configurada.

**Solução**:
```bash
# Verificar variáveis de ambiente
env | grep LLM

# Se não aparecer, adicione no Easypanel (aba Environment)
```

### Erro: "Browser not found"

**Causa**: Playwright não foi instalado corretamente.

**Solução**:
```bash
# Reinstalar Playwright
playwright install chromium
```

### Tarefa demora muito

**Causa**: Tarefas complexas podem levar tempo.

**Solução**:
- Aguarde pacientemente
- Verifique os logs: `tail -f /app/logs/*.log`
- Para tarefas muito longas, considere usar a API com execução em background

---

## 📊 Exemplos de Prompts para Testar

### Simples (< 30s)
```bash
python main.py "Explique o que é machine learning em 3 frases"
python main.py "Liste 5 linguagens de programação populares"
python main.py "Crie uma lista de tarefas para aprender Python"
```

### Médios (30s - 2min)
```bash
python main.py "Pesquise sobre o framework FastAPI e crie um resumo"
python main.py "Crie um código Python para calcular números de Fibonacci"
python main.py "Extraia informações sobre IA do site example.com"
```

### Complexos (2-5min)
```bash
python run_flow.py "Crie um relatório completo sobre tendências de IA com gráficos"
python run_flow.py "Analise dados de vendas e crie visualizações"
python run_flow.py "Pesquise sobre 5 empresas de IA e crie uma comparação"
```

---

## ✅ Checklist de Validação

Antes de prosseguir para a API web, verifique:

- [ ] Container está rodando
- [ ] Python 3.12 está instalado
- [ ] Playwright/Chromium está funcionando
- [ ] Variáveis de ambiente estão configuradas
- [ ] Teste simples executou com sucesso
- [ ] Teste com busca web funcionou
- [ ] Arquivos foram salvos em `/app/workspace/`
- [ ] Logs estão sendo gerados corretamente

---

## 🚀 Próximo Passo: Ativar API Web

Após validar que tudo funciona via CLI, você pode ativar a API web:

1. **Mudar o Start Command** no Easypanel:
   ```bash
   python api_server.py
   ```

2. **Redeploy** o serviço

3. **Acessar a API**:
   - Health check: `https://seu-dominio/health`
   - Documentação: `https://seu-dominio/docs`

---

## 📚 Referências

- **Documentação do OpenManus**: `/app/README.md`
- **Exemplos**: `/app/examples/`
- **Configuração**: `/app/config/config.toml`

---

## 💡 Dicas

1. **Use o modo Flow** (`run_flow.py`) para tarefas complexas
2. **Use o modo Direto** (`main.py`) para tarefas simples e rápidas
3. **Verifique sempre os logs** para entender o que o agente está fazendo
4. **Comece com prompts simples** para validar a instalação
5. **Salve os resultados importantes** antes de fazer redeploy

---

**Pronto para testar?** Acesse o shell do container no Easypanel e comece com um teste simples! 🎉
