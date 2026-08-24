package com.agrosmart;

import java.util.Random;

/**
 * Simula lo que en un proyecto real vendría de un sensor IoT.
 * Genera datos aleatorios dentro de rangos realistas para una
 * cámara de frío agrícola: temperatura entre 2°C y 12°C,
 * humedad entre 45% y 90%.
 *
 * Cuando más adelante se quiera conectar un sensor real (o un
 * dispositivo simulado más sofisticado, como un ESP32 con MQTT),
 * solo hay que reemplazar esta clase; el resto del proyecto no
 * necesita cambiar.
 */
public class SensorSimulator {

    private final Random random;

    public SensorSimulator() {
        this.random = new Random();
    }

    public SensorSimulator(long seed) {
        this.random = new Random(seed);
    }

    public TemperatureReading nextReading() {
        double temperature = round(2 + random.nextDouble() * 10, 2);   // 2.0 a 12.0 °C
        double humidity = round(45 + random.nextDouble() * 45, 2);     // 45.0 a 90.0 %
        return new TemperatureReading(temperature, humidity);
    }

    private double round(double value, int places) {
        double factor = Math.pow(10, places);
        return Math.round(value * factor) / factor;
    }
}
