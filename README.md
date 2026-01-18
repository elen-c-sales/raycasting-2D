# Raycasting - Estudo de Iluminação 2D

Implementação técnica de **raycasting 2D** aplicado à iluminação dinâmica, desenvolvido com **Python** e **Pygame** para fins de estudo e exploração do conceito.

## Características Técnicas

- **Raycasting em tempo real** com 180 raios e 65° de campo de visão
- **Iluminação dinâmica** usando intersecção de linhas (ray-line intersection)
- **Sistema de portas interativas** que afetam a propagação da luz
- **Detecção de colisão** precisa com paredes e obstáculos
- **Movimento suave** com interpolação de ângulo e controle WASD
- **Mapa complexo** no estilo mansão com múltiplos cômodos

## Conceitos Explorados

Este projeto demonstra várias técnicas fundamentais:

1. **Raycasting**: Algoritmo clássico usado em Wolfenstein 3D e Doom
2. **Geometria Vetorial**: Cálculo de intersecção entre linhas
3. **Otimização**: Trade-off entre qualidade visual (360 raios) e performance (180 raios)
4. **Renderização com Polígonos**: Conversão de pontos de colisão em área iluminada

## Controles

- **WASD** ou **Setas**: Movimentação
- **Mouse**: Direciona a visão/cone de luz
- **ENTER**: Interagir com portas próximas

## Como Executar

### Versão Desktop (Python)

```bash
# Instalar dependências
pip install pygame

# Executar versão desktop
python main_desktop.py
```

### Versão Web

```bash
# Instalar Pygbag
pip install pygbag

# Build para web (gera pasta build/web)
pygbag --build .

# Copiar para docs (GitHub Pages)
xcopy build\web docs /E /I /Y

# Testar localmente
python -m http.server 8000 --directory docs
```

Acesse `http://localhost:8000` no navegador para testar.

**Documentação detalhada**: Consulte [BUILD.md](BUILD.md) para instruções completas de build e deploy.

## Demo Online

**[Testar no Navegador](https://elen-c-sales.github.io/raycasting-2D/)**

## Objetivos de Aprendizado

Este projeto serve como estudo de:
- Algoritmos de raycasting para iluminação 2D
- Otimização de performance em Python/Pygame
- Matemática aplicada (geometria vetorial)
- Portabilidade de aplicações Pygame para web com Pygbag

## Stack Técnico

- **Python 3.x**
- **Pygame / Pygame-CE** (Community Edition)
- **Pygbag** (para build web via WebAssembly)
- **GitHub Pages** (hospedagem estática)

## Referências

Baseado em conceitos de raycasting aplicados à iluminação 2D, técnica fundamental em:
- Wolfenstein 3D (id Software, 1992)
- Monaco: What's Yours Is Mine (Pocketwatch Games, 2013)
- Don't Starve (Klei Entertainment, 2013)

## Estrutura do Projeto

```
main.py           → Versão web (com asyncio para Pygbag)
main_desktop.py   → Versão desktop (execução local)
build/            → Artefatos de build (ignorado pelo Git)
docs/             → Build final para GitHub Pages
```

## Licença

Este projeto é open source e está disponível para fins educacionais.

---

**Desenvolvido por [Elen C Sales](https://github.com/elen-c-sales)**
