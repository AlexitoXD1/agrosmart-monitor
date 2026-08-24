package com.agrosmart;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Representa una lectura del sensor de la cámara de frío.
 * En un proyecto real, esto vendría de un sensor físico (por ejemplo,
 * un DHT22 conectado a un ESP32) o de una API de un dispositivo IoT.
 * Aquí lo generamos de forma simulada en {@link SensorSimulator}.
 */
public class TemperatureReading {

    private final LocalDateTime timestamp;
    private final double temperature;
    private final double humidity;

    public TemperatureReading(double temperature, double humidity) {
        this.timestamp = LocalDateTime.now();
        this.temperature = temperature;
        this.humidity = humidity;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public double getTemperature() {
        return temperature;
    }

    public double getHumidity() {
        return humidity;
    }

    public String formattedTimestamp() {
        return timestamp.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
    }

    @Override
    public String toString() {
        return String.format("[%s] Temp: %.1f°C | Humedad: %.1f%%", formattedTimestamp(), temperature, humidity);
    }
}
