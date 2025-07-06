#!/bin/bash
"""
Script para testar URLs das banquetas via curl
"""

echo "=== TESTANDO URLs DAS BANQUETAS ==="
echo

# URLs para testar
urls=(
    "http://localhost:8000/produtos/1/"
    "http://localhost:8000/produtos/3/"
    "http://localhost:8000/produtos/8/"
    "http://localhost:8000/produtos/17/"
    "http://localhost:8000/produtos/"
)

for url in "${urls[@]}"; do
    echo "Testando: $url"
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$status" = "200" ]; then
        echo "✅ Status: $status - OK"
    elif [ "$status" = "302" ]; then
        echo "🔄 Status: $status - Redirecionamento (pode ser login)"
    else
        echo "❌ Status: $status - Erro"
    fi
    echo
done

echo "=== TESTE CONCLUÍDO ==="
