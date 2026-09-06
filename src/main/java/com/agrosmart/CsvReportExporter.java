package com.agrosmart;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/**
 * Exportador de reportes en formato CSV (Comma-Separated Values).
 * Guarda las lecturas del sensor en la carpeta reports/ para su
 * posterior análisis en Excel o herramientas BI.
 */
public class CsvReportExporter {

    public Path exportToCsv(List<TemperatureReading> readings, String filename) throws IOException {
        Path reportsDir = Path.of("reports");
        Files.createDirectories(reportsDir);

        Path csvFile = reportsDir.resolve(filename);

        StringBuilder sb = new StringBuilder();
        sb.append("fecha_hora,temperatura_c,humedad_pct,estado").append(System.lineSeparator());

        for (TemperatureReading r : readings) {
            SensorStatus status = TemperatureClassifier.classify(r.getTemperature());
            sb.append(String.format("%s,%.2f,%.2f,%s%n",
                    r.formattedTimestamp(),
                    r.getTemperature(),
                    r.getHumidity(),
                    status));
        }

        Files.writeString(csvFile, sb.toString());
        return csvFile;
    }
}
