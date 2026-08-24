package com.agrosmart;

/**
 * Regla de negocio del caso AgroSmart Monitor.
 *
 * NORMAL:      temperatura hasta 8°C (inclusive)
 * WARNING:     más de 8°C y hasta 10°C
 * ALERT:       más de 10°C
 *
 * Estos valores son solo para fines didácticos del pipeline;
 * no representan una recomendación sanitaria real.
 *
 * Esta es la lógica crítica del proyecto: la que debe estar
 * protegida por pruebas automatizadas y por el pipeline CI/CD.
 */
public class TemperatureClassifier {

    private TemperatureClassifier() {
        // clase de utilidad, no se instancia
    }

    public static SensorStatus classify(double temperature) {
        if (temperature <= 8.0) {
            return SensorStatus.NORMAL;
        }
        if (temperature <= 10.0) {
            return SensorStatus.WARNING;
        }
        return SensorStatus.ALERT;
    }
}
