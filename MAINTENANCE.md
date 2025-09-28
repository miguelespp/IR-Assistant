# Plan de Mantenimiento - IR-Assistant

## 1. Objetivo
Definir el proceso de mantenimiento posterior a la entrega del sistema.

## 2. Tipos de Mantenimiento
- Correctivo: Resolver bugs reportados.
- Adaptativo: Actualizar dependencias según nuevas versiones.
- Perfectivo: Mejorar rendimiento y cobertura de pruebas.
- Preventivo: Revisar seguridad periódicamente con bandit y pip-audit.

## 3. Procedimiento
1. Reportar incidencias en GitHub Issues con etiqueta [bug] o [security].
2. Crear rama `fix/issue-#`.
3. Hacer Pull Request con referencia al issue.
4. Revisar cambios y fusionar a `main`.
5. Publicar versión parcheada (ej. v1.0.1).

## 4. Periodicidad
- Auditoría de dependencias: mensual.
- Revisión de seguridad: cada release.
- Limpieza de código y refactorización: cada 2 meses.
