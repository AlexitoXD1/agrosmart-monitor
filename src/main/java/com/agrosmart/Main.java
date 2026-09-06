package com.agrosmart;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * Punto de entrada del proyecto. Simula un ciclo corto de monitoreo:
 * genera lecturas, las clasifica, genera alertas si corresponde,
 * exporta el historial a CSV y muestra un resumen estadístico.
 */
public class Main {

    private static final int READINGS_TO_SIMULATE = 5;

    public static void main(String[] args) throws IOException, InterruptedException {
        System.out.println("=== AgroSmart Monitor - monitoreo de camara de frio (simulado) ===");

        SensorSimulator sensor = new SensorSimulator();
        AlertReportGenerator alertReportGenerator = new AlertReportGenerator();
        CsvReportExporter csvExporter = new CsvReportExporter();
        List<TemperatureReading> readings = new ArrayList<>();

        for (int i = 1; i <= READINGS_TO_SIMULATE; i++) {
            TemperatureReading reading = sensor.nextReading();
            readings.add(reading);
            SensorStatus status = TemperatureClassifier.classify(reading.getTemperature());

            System.out.printf("Lectura %d/%d -> %s | Estado: %s%n",
                    i, READINGS_TO_SIMULATE, reading, status);

            if (status == SensorStatus.ALERT) {
                Path report = alertReportGenerator.createReport(reading, status);
                System.out.println("  -> Reporte de alerta generado: " + report);
            }

            Thread.sleep(300);
        }

        Path csvPath = csvExporter.exportToCsv(readings, "lecturas_historico.csv");
        System.out.println("  -> Historial exportado a CSV: " + csvPath);

        SensorStatisticsCalculator statsCalculator = new SensorStatisticsCalculator(readings);
        System.out.println();
        System.out.print(statsCalculator.generateSummaryReport());

        System.out.println("=== Fin de la simulacion ===");
    }
}

