#!/bin/bash
set -e

echo "🚀 Iniciando OpenManus..."

# Gerar configuração a partir de variáveis de ambiente
echo "📝 Gerando arquivo de configuração..."
python /app/generate_config.py

# Verificar se a configuração foi criada com sucesso
if [ ! -f /app/config/config.toml ]; then
    echo "❌ Erro: Arquivo de configuração não foi criado!"
    exit 1
fi

echo "✅ Configuração gerada com sucesso!"

# Criar diretórios necessários
mkdir -p /app/workspace /app/logs

# Exibir informações de inicialização
echo "================================================"
echo "OpenManus - AI Agent Framework"
echo "================================================"
echo "📁 Workspace: /app/workspace"
echo "📋 Config: /app/config/config.toml"
echo "📊 Logs: /app/logs"
echo "================================================"

# Executar comando passado como argumento ou comando padrão
if [ $# -eq 0 ]; then
    echo "⚠️  Nenhum comando especificado. Iniciando shell interativo..."
    exec /bin/bash
else
    echo "▶️  Executando: $@"
    exec "$@"
fi
