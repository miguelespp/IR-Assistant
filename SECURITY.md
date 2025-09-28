SECURITY.md

Resumen de hallazgos
--------------------
- Se detectó una vulnerabilidad conocida en el paquete `pip` instalado en el entorno de desarrollo: `pip 24.3.1` con ID GHSA-4xh5-x5gv-qwph. Recomendación: actualizar `pip` a la versión `>=25.2`.
- Al ejecutar `pip-audit -r requirements.txt` se produjo un error al intentar instalar paquetes listados en `requirements.txt`. El error indicaba un OSError relacionado con archivos construidos localmente dentro de una dependencia (ruta tipo `/builddir/.../tools/net/ynl`). Esto suele ocurrir cuando `requirements.txt` contiene entradas no estándar (por ejemplo rutas `file://` o paquetes construidos localmente) que el auditor intenta instalar en un entorno temporal.

Acciones recomendadas
---------------------
1) Actualizar pip en tu entorno virtual (evita vulnerabilidad detectada por pip-audit):

   python -m pip install --upgrade "pip>=25.2"

2) Regenerar `requirements.txt` sin las entradas problemáticas (elimina referencias `file://` y `@ file`):

   pip freeze | sed '/file:\/\//d' | sed '/@ file/d' > requirements.txt

   Alternativamente, generar un `requirements.txt` limitado a las dependencias del proyecto:

   pip freeze | grep -E '^(flask|openai|python-dotenv|requests|pandas|openpyxl|pygame|numpy)' > requirements.txt

3) Reinstalar dependencias desde el `requirements.txt` limpio y volver a auditar:

   pip install -r requirements.txt
   pip-audit -r requirements.txt

4) Actualizar dependencias vulnerables cuando haya una versión con el parche disponible. Para `pip` en particular, la mitigación es actualizar la propia herramienta `pip` en el entorno virtual.

Notas sobre seguridad del proyecto
----------------------------------
- No incluyas claves secretas (p. ej. `OPENAI_API_KEY`) en el repositorio. Usa un archivo `.env` que esté en `.gitignore`.
- Considera usar `dependabot` o pipelines CI que ejecuten `pip-audit`/`safety` automáticamente en cada PR.
- Mantén una copia de seguridad del `requirements.txt` anterior (por ejemplo `requirements.txt.bak`) antes de sobrescribirlo.

Comandos reproducibles
----------------------
# Hacer backup del requirements actual
cp requirements.txt requirements.txt.bak

# Regenerar evitando paquetes locales
pip freeze | sed '/file:\/\//d' | sed '/@ file/d' > requirements.txt

# Actualizar pip
python -m pip install --upgrade "pip>=25.2"

# Instalar dependencias y auditar
pip install -r requirements.txt
pip-audit -r requirements.txt

Preguntas frecuentes
-------------------
Q: ¿Por qué pip-audit falló con un OSError?
A: Porque intentó instalar paquetes desde `requirements.txt` que se referencian localmente o dependen de artefactos nativos no disponibles en el entorno temporal que `pip-audit` crea. Filtrar o eliminar esas entradas resuelve el problema.

Q: ¿Debo usar `pip` del sistema o del virtualenv para actualizar?
A: Siempre actualiza `pip` dentro del entorno virtual activo (ejecuta el comando con el virtualenv activado).

Contacto
--------
Si quieres que actualice el archivo `requirements.txt` y ejecute la auditoría desde este entorno, indícamelo y lo hago ahora.