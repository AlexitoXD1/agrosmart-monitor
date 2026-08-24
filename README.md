# AgroSmart Monitor (versión demo Java)

Proyecto mínimo en **Java + Maven** para practicar y **demostrar en vivo** un pipeline de **CI/CD con GitHub Actions**, inspirado en el caso "AgroSmart Monitor" (monitoreo de cadena de frío agrícola) de la guía del Proyecto Final del curso.

La parte de **IoT está simulada**: no hace falta ningún sensor físico. `SensorSimulator` genera lecturas de temperatura y humedad aleatorias dentro de rangos realistas, tal como lo hacía `iot_simulator.py` en la guía original (aquí portado a Java).

## ¿Qué hace el proyecto?

1. Simula 5 lecturas de una cámara de frío (temperatura entre 2°C y 12°C, humedad entre 45% y 90%).
2. Clasifica cada lectura según la regla de negocio (`TemperatureClassifier`):
   - `NORMAL`: temperatura ≤ 8°C
   - `WARNING`: temperatura > 8°C y ≤ 10°C
   - `ALERT`: temperatura > 10°C
3. Si una lectura es `ALERT`, genera automáticamente un reporte de texto en la carpeta `reports/` (equivalente al `automation.py` de la guía).
4. Todo esto corre también dentro de un **pipeline de GitHub Actions** (`.github/workflows/ci.yml`) cada vez que se hace `push` o `pull request` a `main`:
   - Descarga el código (checkout)
   - Prepara Java 17
   - Ejecuta las pruebas automatizadas (`mvn test`)
   - Compila y empaqueta (`mvn package`)
   - "Despliega" de forma simulada (copia el `.jar` a una carpeta `staging/`)
   - Publica el `.jar` generado como artefacto descargable de esa ejecución

## Estructura del proyecto

```
agrosmart-monitor/
├── .github/workflows/ci.yml        <- Pipeline de CI/CD
├── pom.xml                         <- Configuración de Maven
├── src/main/java/com/agrosmart/
│   ├── Main.java                   <- Punto de entrada (corre la simulación)
│   ├── TemperatureReading.java     <- Modelo de una lectura
│   ├── SensorSimulator.java        <- Simula el IoT (sin hardware real)
│   ├── SensorStatus.java           <- Enum NORMAL / WARNING / ALERT
│   ├── TemperatureClassifier.java  <- Regla de negocio (la lógica crítica)
│   └── AlertReportGenerator.java   <- Genera el reporte de alerta (RPA)
└── src/test/java/com/agrosmart/
    ├── TemperatureClassifierTest.java  <- Pruebas de la regla de negocio
    └── SensorSimulatorTest.java        <- Pruebas del simulador
```

## Cómo correrlo en tu PC (local)

Requisitos: **Java 17+** y **Maven** instalados.

```bash
java -version
mvn -version
```

Dentro de la carpeta del proyecto:

```bash
# Ejecutar las pruebas automatizadas
mvn test

# Compilar y generar el .jar
mvn package

# Ejecutar la aplicación
java -jar target/agrosmart-monitor.jar
```

Vas a ver algo como:

```
=== AgroSmart Monitor - monitoreo de camara de frio (simulado) ===
Lectura 1/5 -> [2026-08-23 10:00:00] Temp: 6.4°C | Humedad: 61.2% | Estado: NORMAL
Lectura 2/5 -> [2026-08-23 10:00:00] Temp: 11.3°C | Humedad: 58.9% | Estado: ALERT
  -> Reporte de alerta generado: reports/alerta_20260823_100000.txt
...
=== Fin de la simulacion ===
```

## Ideas para modificar en vivo durante la clase

Estas son propuestas pequeñas y seguras para que, en cada sesión, cambies algo, hagas `git push`, y los estudiantes vean el pipeline correr de nuevo en la pestaña **Actions** de GitHub:

1. **Cambiar un umbral de la regla de negocio** en `TemperatureClassifier.java` (por ejemplo, que `WARNING` empiece en 7°C en vez de 8°C) y mostrar cómo las pruebas de `TemperatureClassifierTest.java` siguen pasando (o fallan, si rompes el límite a propósito, para mostrar cómo el pipeline detiene el proceso).
2. **Agregar una prueba nueva** que falle a propósito, hacer `push`, y mostrar en vivo cómo el job "Ejecutar pruebas automatizadas" se pone en rojo y el pipeline no llega a empaquetar ni desplegar.
3. **Aumentar `READINGS_TO_SIMULATE`** en `Main.java` (por ejemplo de 5 a 10) para simular un ciclo de monitoreo más largo.
4. **Cambiar el rango de temperaturas simuladas** en `SensorSimulator.java` para forzar más alertas y ver más reportes generados.
5. **Agregar un paso nuevo al pipeline** en `.github/workflows/ci.yml` (por ejemplo, un paso que imprima la fecha del despliegue) para mostrar que el YAML también se versiona y se puede modificar como cualquier otro archivo.

## Próximos pasos naturales (si quieres ir más allá)

- Conectar un sensor real (o un microcontrolador simulado con Docker) reemplazando `SensorSimulator` por una fuente de datos real — esto conecta directamente con la Sesión 3 del curso (IoT).
- Agregar un paso de "despliegue real" (por ejemplo a un servidor o contenedor) en vez del despliegue simulado actual.
- Agregar un badge de estado del pipeline en este README una vez que el repositorio esté en GitHub.

## Créditos

Basado en el caso de estudio "AgroSmart Monitor" de la Guía de Referencia del Proyecto Integrador del curso *Herramientas de Desarrollo Profesional - TIC* (código 10000096SI), adaptado de Python a Java para fines de práctica de pipelines CI/CD.
