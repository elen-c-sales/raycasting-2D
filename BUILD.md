# Guia de Build para GitHub Pages

Este documento contém instruções detalhadas para compilar e publicar o projeto no GitHub Pages usando Pygbag.

## Pré-requisitos

1. **Python 3.9+** instalado
2. **Git** configurado
3. Repositório GitHub criado

## Passo a Passo Completo

### 1. Instalar Pygbag

```bash
pip install pygbag
```

### 2. Build Web

```bash
# Gerar build (main.py já é a versão web)
pygbag --build .
```

**O que acontece:**
- Pygbag converte o código Python para WebAssembly
- Gera o build na pasta `build/web`
- Usa `main.py` como entrada (que já contém asyncio)

### 3. Copiar para Pasta docs

```bash
# Copiar build para pasta docs (GitHub Pages)
xcopy build\web docs /E /I /Y
```

**O que acontece:**
- Pygbag gera o build em `build/web`
- GitHub Pages precisa da pasta `docs/` na raiz
- O comando copia todos os arquivos necessários

### 4. Testar Localmente (Opcional)

```bash
# Iniciar servidor HTTP local
python -m http.server 8000 --directory docs
```

Acesse `http://localhost:8000` no navegador para testar.

### 5. Publicar no GitHub

```bash
# Adicionar arquivos ao Git (docs/ e código)
git add .
git commit -m "Add web build"
git push origin main
```

### 6. Configurar GitHub Pages

1. Vá para **Settings** > **Pages** no repositório
2. Em **Source**, selecione:
   - Branch: `main`
   - Folder: `/docs`
3. Clique em **Save**

Aguarde alguns minutos e acesse:
```
https://elen-c-sales.github.io/raycasting-2D/
```

## Fluxo de Atualização

Sempre que modificar o código:

```bash
# 1. Editar main.py (versão web)

# 2. Rebuild
pygbag --build .

# 3. Copiar para docs
xcopy build\web docs /E /I /Y

# 4. Commit e push
git add docs/
git commit -m "Update build"
git push origin main
```

## Troubleshooting

### Erro: "No module named 'main'"
- Certifique-se de que há um arquivo `main.py` na raiz do projeto
- Verifique se `main.py` contém `import asyncio` e `async def main()`

### Aplicação não carrega no navegador
- Verifique o console do navegador (F12)
- Certifique-se de que está usando `asyncio` no código
- Adicione `await asyncio.sleep(0)` no loop principal

### GitHub Pages mostra 404
- Verifique se a pasta `docs/` foi commitada
- Confirme nas Settings que `/docs` está selecionado como source
- Aguarde alguns minutos para propagação

### Performance baixa na web
- Reduza `RAY_COUNT` (ex: de 180 para 120)
- Diminua `MAX_DIST` se possível
- Otimize o número de obstáculos

## Metadados do Pygbag

O arquivo `main.py` contém metadados especiais no topo:

```python
# /// script
# dependencies = [
#   "pygame-ce",
# ]
# ///
```

Isso informa ao Pygbag para usar **Pygame Community Edition**, que geralmente tem melhor suporte web.

## Checklist Final

- [ ] `main.py` usa `async def main()` e `await asyncio.sleep(0)`
- [ ] Build gerado em `build/web/` sem erros
- [ ] Arquivos copiados para `docs/`
- [ ] Teste local funcionando
- [ ] `.gitignore` configurado (ignora `build/`, não ignora `docs/`)
- [ ] Pasta `docs/` commitada e pushada
- [ ] GitHub Pages ativado apontando para `/docs`
- [ ] URL pública funcionando
- [ ] README.md atualizado com link da demo

---

**Estrutura do Projeto:**
- `main.py` → Versão web (com asyncio, para Pygbag)
- `main_desktop.py` → Versão desktop (sem asyncio, para execução local)
- `build/` → Build temporário (ignorado pelo Git)
- `docs/` → Build final para GitHub Pages (versionado)
