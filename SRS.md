# Especificación de Requisitos de Software (SRS) - IR-Assistant

## 1. Introducción
Este documento describe los requisitos funcionales y no funcionales de IR-Assistant.

## 2. Requisitos Funcionales
- RF01: El sistema debe permitir recibir consultas de texto vía API HTTP.
- RF02: El sistema debe clasificar la consulta utilizando un modelo pre-entrenado.
- RF03: El sistema debe devolver la respuesta en formato JSON.
- RF04: El sistema debe permitir logs de las interacciones.
- RF05: El sistema debe auditar dependencias para seguridad.

## 3. Requisitos No Funcionales
- RNF01: El sistema debe estar implementado en Python 3.10+.
- RNF02: La API debe responder en menos de 2 segundos para consultas promedio.
- RNF03: El sistema no debe exponer credenciales ni secretos en el código.
- RNF04: El sistema debe pasar pruebas de seguridad (Bandit, pip-audit).
- RNF05: El sistema debe tener cobertura de pruebas mayor al 60%.

## 4. Restricciones
- Uso de dependencias solo desde PyPI.
- Despliegue inicial en entorno local (sin nube productiva).

## 5. Suposiciones
- Los usuarios son investigadores/profesores que prueban consultas de texto.
