# 🛡️ Multi-Agent Prompt Harness

Este repositorio contiene un **Arnés de Prompts Multi-Agente** avanzado y profesional diseñado para estructurar el comportamiento, flujo de trabajo y capacidades de agentes de Inteligencia Artificial (tales como **OpenCode**, **Claude Code**, **Roo Code**, o **Cursor**).

El arnés implementa una arquitectura rigurosa orientada a la separación de roles, validación mediante TDD estricto y gestión concurrente de múltiples perfiles de desarrollo (C embebido, Python, y JavaScript) que se pueden instalar, remover o adaptar de forma dinámica.

---

## 🚀 Inicio Rápido (First Run)

Para arrancar el arnés y configurar tu herramienta de desarrollo favorita:

1. **Clona el repositorio** en tu espacio de trabajo.
2. **Ejecuta el script bootstrap** en la raíz:
   ```bash
   python3 adapt_harness.py
   ```
   *Nota: La primera vez que lo ejecutes, el script detectará la ausencia de dependencias locales, creará automáticamente un entorno virtual seguro bajo `.harness/adaptation/.venv/` e instalará los requerimientos en segundo plano de manera 100% transparente.*

---

## 🎨 Menú Interactivo en Terminal

Si ejecutas `python3 adapt_harness.py` sin argumentos, se desplegará una interfaz visual premium e interactiva:

```
==========================================================
🛡️  Harness Adaptation & Profile Manager - Interactive Menu
==========================================================
  1. ⚙️  Compilar/Transpilar Arnés a formato OpenCode (opencode)
  2. 📥  Instalar / Actualizar un Perfil en .opencode/ (install)
  3. 🧹  Remover un Perfil de .opencode/ (remove)
  4. 🤖  Adaptar Arnés para Claude Code / Roo Code (claude)
  5. 💻  Adaptar Arnés para Cursor (cursor)
  6. 🔄  Sincronizar catálogo AGENTS.md (sync)
  7. ❌  Salir
==========================================================
```

### Opciones Disponibles:
* **Compilar para OpenCode (1)**: Transpila las plantillas origen bajo la carpeta `.harness/` al formato y estructura nativa de OpenCode (`.opencode/`).
* **Instalar Perfil (2)**: Permite elegir dinámicamente qué perfil de desarrollo (`python-developer`, `embedded-c-developer`, `javascript-developer`) deseas instalar como sobrecapa en tu entorno de desarrollo.
* **Remover Perfil (3)**: Elimina de forma limpia y selectiva un perfil y todas sus habilidades/directivas específicas para evitar fugas de contexto en el agente de IA.
* **Adaptar para Claude Code / Roo Code / Cursor (4 y 5)**: Genera los archivos pointer correspondientes (`.clinerules` o `.cursorrules`) y sincroniza el manifiesto.
* **Sincronizar Catálogo (6)**: Re-indexa de forma dinámica todos los agentes, roles y habilidades disponibles y actualiza el archivo maestro [`AGENTS.md`](file:///Users/hazaeltrejo/Documents/harness_template/AGENTS.md).

---

## 💻 Uso directo por Línea de Comandos (CLI)

Si prefieres la terminal o estás automatizando flujos en un CI/CD, puedes usar argumentos de línea de comandos directamente:

* **Compilar todo el arnés para OpenCode**:
  ```bash
  python3 adapt_harness.py opencode
  ```
* **Instalar un perfil específico**:
  ```bash
  python3 adapt_harness.py install python-developer
  ```
* **Remover un perfil específico**:
  ```bash
  python3 adapt_harness.py remove python-developer
  ```
* **Adaptar arnés a Claude Code / Cursor**:
  ```bash
  python3 adapt_harness.py claude
  python3 adapt_harness.py cursor
  ```
* **Sincronizar catálogo de agentes**:
  ```bash
  python3 adapt_harness.py sync
  ```

---

## 📂 Estructura del Repositorio

- [**`.harness/`**](file:///Users/hazaeltrejo/Documents/harness_template/.harness/): **La Fuente de Verdad**. Contiene las plantillas de roles, habilidades principales y perfiles que mantienes en tu repositorio. *(Ver el [README de `.harness/`](file:///Users/hazaeltrejo/Documents/harness_template/.harness/README.md) para más detalles).*
- [**`adapt_harness.py`**](file:///Users/hazaeltrejo/Documents/harness_template/adapt_harness.py): Cargador y bootstrap autogestionado del entorno virtual de Python.
- [**`AGENTS.md`**](file:///Users/hazaeltrejo/Documents/harness_template/AGENTS.md): Catálogo y manifiesto central dinámico que lee e indexa los agentes y habilidades reales de tu espacio de trabajo para dar contexto de alto nivel al Orquestador.
- **`.opencode/`** *(Generado)*: Carpeta del arnés transpilado y listo para que la use el agente local en formato OpenCode.
- **`.clinerules` / `.cursorrules`** *(Generado)*: Archivos de directivas/pointer listos para alimentar a Claude Code, Roo Code o Cursor.
