#!/usr/bin/env python3
"""
Script para gerar config.toml a partir de variáveis de ambiente
Útil para deployment no Easypanel e outros ambientes containerizados
"""

import os
import sys
from pathlib import Path


def generate_config():
    """Gera arquivo config.toml a partir de variáveis de ambiente"""
    
    config_dir = Path("/app/config")
    config_file = config_dir / "config.toml"
    
    # Criar diretório se não existir
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Verificar se já existe configuração
    if config_file.exists():
        print(f"⚠️  Arquivo {config_file} já existe. Sobrescrevendo...")
    
    # Obter variáveis de ambiente
    llm_model = os.getenv("LLM_MODEL", "gpt-4o")
    llm_base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    llm_api_key = os.getenv("LLM_API_KEY", "")
    llm_max_tokens = os.getenv("LLM_MAX_TOKENS", "4096")
    llm_temperature = os.getenv("LLM_TEMPERATURE", "0.0")
    llm_api_type = os.getenv("LLM_API_TYPE", "")
    llm_api_version = os.getenv("LLM_API_VERSION", "")
    
    # Vision model
    llm_vision_model = os.getenv("LLM_VISION_MODEL", llm_model)
    llm_vision_base_url = os.getenv("LLM_VISION_BASE_URL", llm_base_url)
    llm_vision_api_key = os.getenv("LLM_VISION_API_KEY", llm_api_key)
    llm_vision_max_tokens = os.getenv("LLM_VISION_MAX_TOKENS", llm_max_tokens)
    llm_vision_temperature = os.getenv("LLM_VISION_TEMPERATURE", llm_temperature)
    
    # Browser
    browser_headless = os.getenv("BROWSER_HEADLESS", "true").lower() == "true"
    browser_disable_security = os.getenv("BROWSER_DISABLE_SECURITY", "true").lower() == "true"
    browser_extra_args = os.getenv("BROWSER_EXTRA_CHROMIUM_ARGS", "")
    browser_chrome_path = os.getenv("BROWSER_CHROME_INSTANCE_PATH", "")
    browser_wss_url = os.getenv("BROWSER_WSS_URL", "")
    browser_cdp_url = os.getenv("BROWSER_CDP_URL", "")
    
    # Browser proxy
    browser_proxy_server = os.getenv("BROWSER_PROXY_SERVER", "")
    browser_proxy_username = os.getenv("BROWSER_PROXY_USERNAME", "")
    browser_proxy_password = os.getenv("BROWSER_PROXY_PASSWORD", "")
    
    # Search
    search_engine = os.getenv("SEARCH_ENGINE", "Google")
    search_fallback = os.getenv("SEARCH_FALLBACK_ENGINES", "DuckDuckGo,Baidu,Bing")
    search_retry_delay = os.getenv("SEARCH_RETRY_DELAY", "60")
    search_max_retries = os.getenv("SEARCH_MAX_RETRIES", "3")
    search_lang = os.getenv("SEARCH_LANG", "en")
    search_country = os.getenv("SEARCH_COUNTRY", "us")
    
    # Sandbox
    sandbox_use = os.getenv("SANDBOX_USE", "false").lower() == "true"
    sandbox_image = os.getenv("SANDBOX_IMAGE", "python:3.12-slim")
    sandbox_work_dir = os.getenv("SANDBOX_WORK_DIR", "/workspace")
    sandbox_memory = os.getenv("SANDBOX_MEMORY_LIMIT", "1g")
    sandbox_cpu = os.getenv("SANDBOX_CPU_LIMIT", "2.0")
    sandbox_timeout = os.getenv("SANDBOX_TIMEOUT", "300")
    sandbox_network = os.getenv("SANDBOX_NETWORK_ENABLED", "true").lower() == "true"
    
    # MCP
    mcp_server_ref = os.getenv("MCP_SERVER_REFERENCE", "app.mcp.server")
    
    # RunFlow
    runflow_data_analysis = os.getenv("RUNFLOW_USE_DATA_ANALYSIS", "false").lower() == "true"
    
    # Validar API key obrigatória
    if not llm_api_key:
        print("❌ ERRO: LLM_API_KEY não foi definida!")
        print("Por favor, defina a variável de ambiente LLM_API_KEY")
        sys.exit(1)
    
    # Gerar conteúdo do config.toml
    config_content = f"""# OpenManus Configuration
# Gerado automaticamente a partir de variáveis de ambiente

# Global LLM configuration
[llm]
model = "{llm_model}"
base_url = "{llm_base_url}"
api_key = "{llm_api_key}"
max_tokens = {llm_max_tokens}
temperature = {llm_temperature}
"""
    
    # Adicionar api_type se definido
    if llm_api_type:
        config_content += f'api_type = "{llm_api_type}"\n'
    
    # Adicionar api_version se definido (Azure)
    if llm_api_version:
        config_content += f'api_version = "{llm_api_version}"\n'
    
    # Vision model
    config_content += f"""
# Optional configuration for specific LLM models
[llm.vision]
model = "{llm_vision_model}"
base_url = "{llm_vision_base_url}"
api_key = "{llm_vision_api_key}"
max_tokens = {llm_vision_max_tokens}
temperature = {llm_vision_temperature}
"""
    
    # Browser configuration
    config_content += f"""
# Browser configuration
[browser]
headless = {str(browser_headless).lower()}
disable_security = {str(browser_disable_security).lower()}
"""
    
    if browser_extra_args:
        config_content += f'extra_chromium_args = ["{browser_extra_args}"]\n'
    if browser_chrome_path:
        config_content += f'chrome_instance_path = "{browser_chrome_path}"\n'
    if browser_wss_url:
        config_content += f'wss_url = "{browser_wss_url}"\n'
    if browser_cdp_url:
        config_content += f'cdp_url = "{browser_cdp_url}"\n'
    
    # Browser proxy
    if browser_proxy_server:
        config_content += f"""
[browser.proxy]
server = "{browser_proxy_server}"
"""
        if browser_proxy_username:
            config_content += f'username = "{browser_proxy_username}"\n'
        if browser_proxy_password:
            config_content += f'password = "{browser_proxy_password}"\n'
    
    # Search configuration
    fallback_list = [f'"{e.strip()}"' for e in search_fallback.split(',')]
    config_content += f"""
# Search settings
[search]
engine = "{search_engine}"
fallback_engines = [{', '.join(fallback_list)}]
retry_delay = {search_retry_delay}
max_retries = {search_max_retries}
lang = "{search_lang}"
country = "{search_country}"
"""
    
    # Sandbox configuration
    if sandbox_use:
        config_content += f"""
# Sandbox configuration
[sandbox]
use_sandbox = {str(sandbox_use).lower()}
image = "{sandbox_image}"
work_dir = "{sandbox_work_dir}"
memory_limit = "{sandbox_memory}"
cpu_limit = {sandbox_cpu}
timeout = {sandbox_timeout}
network_enabled = {str(sandbox_network).lower()}
"""
    
    # MCP configuration
    config_content += f"""
# MCP (Model Context Protocol) configuration
[mcp]
server_reference = "{mcp_server_ref}"
"""
    
    # RunFlow configuration
    config_content += f"""
# RunFlow configuration
[runflow]
use_data_analysis_agent = {str(runflow_data_analysis).lower()}
"""
    
    # Escrever arquivo
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"✅ Arquivo de configuração gerado com sucesso: {config_file}")
    print(f"📝 Modelo LLM: {llm_model}")
    print(f"🔗 Base URL: {llm_base_url}")
    print(f"🔑 API Key: {'*' * (len(llm_api_key) - 4) + llm_api_key[-4:] if len(llm_api_key) > 4 else '***'}")
    
    return True


if __name__ == "__main__":
    try:
        generate_config()
    except Exception as e:
        print(f"❌ Erro ao gerar configuração: {e}")
        sys.exit(1)
