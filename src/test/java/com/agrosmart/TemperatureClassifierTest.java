package com.agrosmart;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Estas son las pruebas que el pipeline ejecuta en cada cambio.
 * Si alguna falla, el job de "Ejecutar pruebas automatizadas" se
 * pone en rojo y el pipeline NO continua hacia el empaquetado ni el
 * despliegue simulado.
 */
class TemperatureClassifierTest {

    @Test
    void debeClasificarComoNormalHasta8Grados() {
        assertEquals(SensorStatus.NORMAL, TemperatureClassifier.classify(6.0));
        assertEquals(SensorStatus.NORMAL, TemperatureClassifier.classify(8.0));
    }

    @Test
    void debeClasificarComoAdvertenciaEntre8y10Grados() {
        assertEquals(SensorStatus.WARNING, TemperatureClassifier.classify(9.0));
        assertEquals(SensorStatus.WARNING, TemperatureClassifier.classify(10.0));
    }

    @Test
    void debeClasificarComoAlertaSobre10Grados() {
        assertEquals(SensorStatus.NORMAL, TemperatureClassifier.classify(10.1));
        assertEquals(SensorStatus.ALERT, TemperatureClassifier.classify(15.0));
    }
}
