package com.agrosmart;

import java.util.List;

/**
 * Calculadora de estadísticas de monitoreo IoT.
 * Procesa una lista de lecturas de sensores y genera métricas agregadas
 * como temperaturas promedio, máximas, mínimas y conteo por nivel de alerta.
 */
public class SensorStatisticsCalculator {

    private final List<TemperatureReading> readings;
    private double minTemperature;
    private double maxTemperature;
    private double averageTemperature;
    private double averageHumidity;
    private int normalCount;
    private int warningCount;
    private int alertCount;

    public SensorStatisticsCalculator(List<TemperatureReading> readings) {
        if (readings == null || readings.isEmpty()) {
            throw new IllegalArgumentException("La lista de lecturas no puede estar vacía.");
        }
        this.readings = readings;
        calculate();
    }

    private void calculate() {
        double sumTemp = 0.0;
        double sumHum = 0.0;
        minTemperature = Double.MAX_VALUE;
        maxTemperature = Double.MIN_VALUE;
        normalCount = 0;
        warningCount = 0;
        alertCount = 0;

        for (TemperatureReading r : readings) {
            double temp = r.getTemperature();
            double hum = r.getHumidity();

            sumTemp += temp;
            sumHum += hum;

            if (temp < minTemperature) {
                minTemperature = temp;
            }
            if (temp > maxTemperature) {
                maxTemperature = temp;
            }

            SensorStatus status = TemperatureClassifier.classify(temp);
            switch (status) {
                case NORMAL -> normalCount++;
                case WARNING -> warningCount++;
                case ALERT -> alertCount++;
            }
        }

        int total = readings.size();
        this.averageTemperature = round(sumTemp / total, 2);
        this.averageHumidity = round(sumHum / total, 2);
        this.minTemperature = round(minTemperature, 2);
        this.maxTemperature = round(maxTemperature, 2);
    }

    public double getMinTemperature() {
        return minTemperature;
    }

    public double getMaxTemperature() {
        return maxTemperature;
    }

    public double getAverageTemperature() {
        return averageTemperature;
    }

    public double getAverageHumidity() {
        return averageHumidity;
    }

    public int getNormalCount() {
        return normalCount;
    }

    public int getWarningCount() {
        return warningCount;
    }

    public int getAlertCount() {
        return alertCount;
    }

    public int getTotalReadings() {
        return readings.size();
    }

    public String generateSummaryReport() {
        StringBuilder sb = new StringBuilder();
        sb.append("=== Resumen Estadístico de Monitoreo ===").append(System.lineSeparator());
        sb.append(String.format("Total de lecturas procesadas : %d%n", getTotalReadings()));
        sb.append(String.format("Temperatura Promedio         : %.2f°C%n", averageTemperature));
        sb.append(String.format("Temperatura Mínima           : %.2f°C%n", minTemperature));
        sb.append(String.format("Temperatura Máxima           : %.2f°C%n", maxTemperature));
        sb.append(String.format("Humedad Promedio             : %.2f%%%n", averageHumidity));
        sb.append(String.format("Distribución de Estados      : NORMAL: %d | WARNING: %d | ALERT: %d%n",
                normalCount, warningCount, alertCount));
        return sb.toString();
    }

    private double round(double value, int places) {
        double factor = Math.pow(10, places);
        return Math.round(value * factor) / factor;
    }
}
