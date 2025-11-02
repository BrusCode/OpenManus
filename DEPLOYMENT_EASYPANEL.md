# Guia Completo de Deployment do OpenManus no Easypanel

**Autor**: Manus AI
**Data**: 01 de Novembro de 2025

## 1. Introdução

Este documento fornece um guia passo a passo para fazer o deploy da aplicação **OpenManus** no **Easypanel**, utilizando uma configuração otimizada com Docker. O objetivo é criar um serviço robusto, configurável e persistente.

### Arquivos de Configuração Fornecidos:

Para facilitar o processo, os seguintes arquivos foram criados e devem ser enviados para o seu repositório (`BrusCode/OpenManus`):

1.  `Dockerfile.easypanel`: Um Dockerfile otimizado para produção, que instala todas as dependências, incluindo Playwright, e prepara o ambiente.
2.  `docker-compose.yml`: Arquivo de referência para testes locais e para entender a estrutura do serviço.
3.  `generate_config.py`: Script Python que gera o arquivo `config.toml` dinamicamente a partir de variáveis de ambiente, ideal para ambientes de container.
4.  `entrypoint.sh`: Script de inicialização do container que executa o `generate_config.py` antes de iniciar a aplicação principal.
5.  `.env.example`: Arquivo de exemplo com todas as variáveis de ambiente disponíveis.
6.  `EASYPANEL_ENV_GUIDE.md`: Um guia detalhado sobre como configurar cada variável de ambiente.

---

## 2. Pré-requisitos

- Uma instância do Easypanel instalada e funcionando.
- Sua conta do GitHub conectada ao Easypanel.
- Um fork do repositório OpenManus (ex: `BrusCode/OpenManus`).
- Uma chave de API de um provedor de LLM (OpenAI, Anthropic, etc.).

---

## 3. Passo a Passo do Deployment

### Passo 1: Preparar o Repositório GitHub

Antes de iniciar no Easypanel, você precisa garantir que todos os arquivos de configuração que criei estejam no seu repositório.

1.  **Adicione os novos arquivos**: Faça o `git add` e `git commit` dos seguintes arquivos no seu clone local:
    - `Dockerfile.easypanel`
    - `docker-compose.yml`
    - `generate_config.py`
    - `entrypoint.sh`
    - `.env.example`
    - `EASYPANEL_ENV_GUIDE.md`
    - `DEPLOYMENT_EASYPANEL.md` (este guia)

2.  **Envie para o GitHub**:

    ```bash
    git push origin main
    ```

### Passo 2: Criar o Serviço no Easypanel

1.  No seu dashboard do Easypanel, vá para a seção **Projects** e crie um novo projeto ou use um existente.
2.  Dentro do projeto, clique em **+ New** e selecione **App**.

### Passo 3: Configurar a Fonte (Source)

1.  Selecione **Git** como a fonte.
2.  **Provider**: Escolha **GitHub**.
3.  **Repository**: Selecione seu fork, `BrusCode/OpenManus`.
4.  **Branch**: Deixe como `main`.

### Passo 4: Configurar o Build

1.  Na seção **Build**, selecione **Dockerfile**.
2.  **Dockerfile Path**: Especifique o caminho para o Dockerfile otimizado:
    - `/Dockerfile.easypanel`

    ![Configuração de Build no Easypanel](https://i.imgur.com/example.png) <!-- Placeholder para imagem -->

### Passo 5: Configurar Variáveis de Ambiente (Environment)

Esta é a etapa mais importante para a configuração do OpenManus.

1.  Vá para a aba **Environment**.
2.  Adicione as variáveis de ambiente necessárias. Consulte o guia `EASYPANEL_ENV_GUIDE.md` para uma lista completa.

    **Variável Obrigatória:**

| Key | Value |
| :-- | :---- |
| `LLM_API_KEY` | `sk-proj-sua-chave-de-api-aqui` |

    **Variáveis Recomendadas:**

| Key | Value |
| :-- | :---- |
| `LLM_MODEL` | `gpt-4o` |
| `LLM_BASE_URL`| `https://api.openai.com/v1` |

3.  Clique em **Save** após adicionar todas as variáveis.

### Passo 6: Configurar o Comando de Start (Start Command)

O `entrypoint.sh` cuidará da configuração inicial. O comando de start definirá o que o OpenManus fará após a inicialização.

1.  Vá para a aba **General**.
2.  No campo **Start Command**, você pode definir a ação padrão. Como o OpenManus é uma ferramenta de CLI, a melhor abordagem é iniciar um shell para interação manual ou executar um comando específico.

    **Opção A (Recomendada para Interação):** Manter o container rodando para acesso via shell.

    ```bash
    tail -f /dev/null
    ```

    **Opção B (Executar tarefa única e parar):**

    ```bash
    python main.py --prompt "Escreva um poema sobre IA"
    ```

### Passo 7: Configurar Volumes Persistentes

Para garantir que seus dados não sejam perdidos entre deployments, configure os volumes.

1.  Vá para a aba **Volumes**.
2.  Adicione os seguintes mapeamentos:

| Host Path (Volume Name) | Container Path |
| :---------------------- | :------------- |
| `openmanus-workspace` | `/app/workspace` |
| `openmanus-config` | `/app/config` |
| `openmanus-logs` | `/app/logs` |

    O Easypanel criará os volumes automaticamente.

### Passo 8: Fazer o Deploy

1.  Após revisar todas as configurações, clique no botão **Deploy**.
2.  Aguarde o Easypanel construir a imagem Docker e iniciar o container. Você pode acompanhar o progresso na aba **Logs**.

---

## 4. Verificação e Uso

### Verificando a Instalação

1.  **Logs de Build**: Verifique se a imagem foi construída sem erros.
2.  **Logs do Container**: Após o deploy, os logs devem mostrar a saída do `entrypoint.sh`, confirmando que o `config.toml` foi gerado com sucesso:

    ```
    🚀 Iniciando OpenManus...
    📝 Gerando arquivo de configuração...
    ✅ Arquivo de configuração gerado com sucesso: /app/config/config.toml
    ...
    ▶️  Executando: tail -f /dev/null
    ```

### Interagindo com o OpenManus

Como o OpenManus é uma ferramenta de linha de comando, a interação se dá através do shell do container.

1.  No seu serviço no Easypanel, vá para a aba **Shell**.
2.  Clique em **Connect**.
3.  Você terá um terminal dentro do container. Agora você pode executar o OpenManus:

    ```bash
    # Iniciar o modo interativo
    python main.py
    ```

4.  O agente solicitará seu prompt, e você poderá interagir com ele diretamente.

    ```
    Enter your prompt: Crie um site simples sobre a história da computação.
    ```

5.  Todos os arquivos gerados pelo agente estarão no diretório `/app/workspace`, que está persistido no volume `openmanus-workspace`.

---

## 5. Próximos Passos

Esta configuração implanta o OpenManus como uma ferramenta de CLI dentro de um container. Para uma integração mais robusta, considere os seguintes passos:

- **Criar uma API Web**: Modifique a aplicação para usar um framework como **FastAPI** ou **Flask** para expor a funcionalidade do agente através de uma API REST.
- **Configurar Domínio**: Na aba **Domains** do Easypanel, aponte um domínio para o serviço, permitindo que você acesse a API web publicamente.
- **Webhooks**: Configure webhooks para iniciar tarefas do OpenManus a partir de eventos externos.

---

## 6. Troubleshooting

- **Erro de Build**: Verifique o `Dockerfile.easypanel` e os logs de build para identificar pacotes faltando ou comandos que falharam.
- **Container não Inicia**: A causa mais comum são variáveis de ambiente ausentes ou incorretas. Verifique a aba **Environment** e os logs do container.
- **Erro de API do LLM**: Confirme que sua `LLM_API_KEY` é válida e que o `LLM_BASE_URL` está correto para o seu provedor.

Com este guia, seu OpenManus estará funcionando perfeitamente no Easypanel!
