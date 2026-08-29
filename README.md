# AgroSmart Monitor (demostración en Java)

Proyecto demostrativo desarrollado con **Java y Maven** para implementar un pipeline de **CI/CD (Continuous Integration / Continuous Delivery - Integración Continua / Entrega Continua)** mediante **GitHub Actions**. El caso se basa en AgroSmart Monitor, una plataforma de monitoreo de la cadena de frío agrícola incluida en la guía del Proyecto Final del curso.

El componente de **IoT (Internet of Things - Internet de las Cosas)** se encuentra simulado, por lo que no se requiere un sensor físico. La clase `SensorSimulator` genera lecturas aleatorias de temperatura y humedad dentro de rangos establecidos e implementa en Java una función equivalente a `iot_simulator.py` de la guía de referencia.

## ¿Qué hace el proyecto?

1. Simula cinco lecturas de una cámara de frío, con temperaturas entre 2 °C y 12 °C y niveles de humedad entre 45 % y 90 %.
2. Clasifica cada lectura mediante la regla de negocio implementada en `TemperatureClassifier`:

   * `NORMAL`: temperatura menor o igual que 8 °C.
   * `WARNING`: temperatura mayor que 8 °C y menor o igual que 10 °C.
   * `ALERT`: temperatura mayor que 10 °C.
3. Cuando una lectura obtiene el estado `ALERT`, genera automáticamente un reporte de texto en la carpeta `reports/`. Esta función representa una automatización básica de **RPA (Robotic Process Automation - Automatización Robótica de Procesos)**.
4. Integra un pipeline de GitHub Actions definido en `.github/workflows/ci.yml`, que se activa mediante un `push` o un `pull request` sobre la rama `main`:

   * Descarga el código del repositorio mediante `checkout`.
   * Prepara el entorno de Java 17.
   * Ejecuta las pruebas automatizadas con `mvn test`.
   * Compila y empaqueta la aplicación con `mvn package`.
   * Realiza un despliegue simulado copiando el archivo `.jar` a la carpeta `staging/`.
   * Publica el archivo `.jar` como artefacto descargable de la ejecución.

## Estructura del proyecto

```text
agrosmart-monitor/
├── .github/workflows/ci.yml        <- Pipeline de CI/CD
├── pom.xml                         <- Configuración de Maven
├── src/main/java/com/agrosmart/
│   ├── Main.java                   <- Punto de entrada de la aplicación
│   ├── TemperatureReading.java     <- Modelo de una lectura
│   ├── SensorSimulator.java        <- Simulación del componente IoT
│   ├── SensorStatus.java           <- Estados NORMAL, WARNING y ALERT
│   ├── TemperatureClassifier.java  <- Regla de negocio
│   └── AlertReportGenerator.java   <- Generación automática de reportes
└── src/test/java/com/agrosmart/
    ├── TemperatureClassifierTest.java  <- Pruebas de la regla de negocio
    └── SensorSimulatorTest.java        <- Pruebas del simulador
```

## Ejecución local del proyecto

### Requisitos

* Java 17 o una versión posterior.
* Maven instalado.

Para comprobar las versiones instaladas:

```bash
java -version
mvn -version
```

Dentro de la carpeta principal del proyecto se pueden ejecutar los siguientes comandos:

```bash
# Ejecutar las pruebas automatizadas
mvn test

# Compilar y generar el archivo JAR
mvn package

# Ejecutar la aplicación
java -jar target/agrosmart-monitor.jar
```

`JAR` significa **Java Archive (Archivo Java)** y corresponde al artefacto ejecutable generado durante la construcción del proyecto.

La ejecución mostrará una salida similar a la siguiente:

```text
=== AgroSmart Monitor - monitoreo de camara de frio (simulado) ===
Lectura 1/5 -> [2026-08-23 10:00:00] Temp: 6.4°C | Humedad: 61.2% | Estado: NORMAL
Lectura 2/5 -> [2026-08-23 10:00:00] Temp: 11.3°C | Humedad: 58.9% | Estado: ALERT
  -> Reporte de alerta generado: reports/alerta_20260823_100000.txt
...
=== Fin de la simulacion ===
```

## Actividades prácticas durante la clase

En cada sesión se implementará una modificación, se realizará un `git push` y se observará la nueva ejecución del pipeline en la pestaña **Actions** de GitHub:

1. **Modificar un umbral de la regla de negocio** en `TemperatureClassifier.java`. Por ejemplo, establecer que `WARNING` comience en 7 °C en lugar de 8 °C y comprobar el comportamiento de las pruebas definidas en `TemperatureClassifierTest.java`.
2. **Incorporar temporalmente una prueba que falle**, realizar un `git push` y observar cómo la etapa de pruebas automatizadas cambia a estado fallido e impide continuar con el empaquetado y el despliegue.
3. **Aumentar el valor de `READINGS_TO_SIMULATE`** en `Main.java`, por ejemplo, de 5 a 10, para simular un ciclo de monitoreo más largo.
4. **Modificar el rango de temperaturas simuladas** en `SensorSimulator.java` para generar una mayor cantidad de alertas y reportes.
5. **Agregar un paso al pipeline** en `.github/workflows/ci.yml`, como el registro de la fecha del despliegue, para comprobar que el archivo YAML también se encuentra versionado.

## Posibles extensiones del proyecto

* Conectar un sensor real o un microcontrolador simulado mediante Docker, reemplazando `SensorSimulator` por una fuente de datos externa.
* Incorporar un despliegue real hacia un servidor o contenedor en lugar del despliegue simulado.
* Agregar un distintivo o *badge* con el estado del pipeline en este archivo `README.md`.
* Incorporar nuevas pruebas unitarias y pruebas de integración.
* Implementar el almacenamiento histórico de las lecturas generadas.

## Créditos

Proyecto basado en el caso de estudio AgroSmart Monitor de la Guía de Referencia del Proyecto Integrador del curso *Herramientas de Desarrollo Profesional - TIC* (código 10000096SI) y adaptado de Python a Java para la práctica de pipelines de CI/CD.
