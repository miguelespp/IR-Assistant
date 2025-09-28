# Registro y Mitigación de Riesgos - IR-Assistant

## 1. Introducción
Este documento identifica riesgos asociados al desarrollo y operación de IR-Assistant, y define estrategias de mitigación.

## 2. Matriz de Riesgos

| ID  | Riesgo                                     | Probabilidad | Impacto | Nivel | Mitigación                                                                 | Responsable ||-----| --------------------------------------------|--------------|---------|-------|----------------------------------------------------------------------------|-------------|
| R1  | Dependencias con vulnerabilidades          | Alta         | Alto    | Crítico | Ejecutar `pip-audit` y `safety` en cada release; actualizar versiones.     | Miguel      |
| R2  | Pérdida de credenciales en el repo         | Media        | Alto    | Alto   | Uso de `.env` y GitHub Secrets; escaneo con `git-secrets`.                 | Miguel      |
| R3  | Fallo de despliegue en producción          | Baja         | Medio   | Medio  | Documentar despliegue en `DEPLOY.md`; usar contenedores reproducibles.     | Miguel      |
| R4  | Baja cobertura de pruebas                  | Media        | Medio   | Medio  | Añadir `pytest` y reportes de cobertura; objetivo mínimo 60%.              | Miguel      |
| R5  | Uso de datos sensibles en logs             | Baja         | Alto    | Medio  | Revisar logging; evitar incluir tokens/PII; auditoría mensual.             | Miguel      |
| R6  | Falta de documentación en nuevos cambios   | Media        | Bajo    | Bajo   | Uso obligatorio de PR con actualización en `CHANGELOG.md` y `README.md`.   | Miguel      |

## 3. Procedimiento
1. Revisar riesgos antes de cada release.
2. Actualizar estado en esta tabla cuando un riesgo sea mitigado.
3. Reportar nuevos riesgos mediante GitHub Issues con etiqueta `[risk]`.

## 4. Seguimiento
- Revisión de riesgos: mensual.
- Responsable: Miguel Espinoza.
