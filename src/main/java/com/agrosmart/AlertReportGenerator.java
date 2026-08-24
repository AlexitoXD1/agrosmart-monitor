package com.agrosmart;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Componente de automatización (equivalente al "RPA" del proyecto modelo).
 * Antes, un operario revisaba manualmente los datos y avisaba por correo;
 * ahora el sistema detecta la alerta y genera el reporte solo, sin
 * intervención manual.
 */
public class AlertReportGenerator {

    private static final DateTimeFormatter FILE_FORMAT = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss");

    public Path createReport(TemperatureReading reading, SensorStatus status) throws IOException {
        Path reportsDir = Path.of("reports");
        Files.createDirectories(reportsDir);

        String filename = String.format("alerta_%s.txt", LocalDateTime.now().format(FILE_FORMAT));
        Path reportFile = reportsDir.resolve(filename);

        String content = "ALERTA AUTOMATICA - AgroSmart Monitor" + System.lineSeparator()
                + "Estado: " + status + System.lineSeparator()
                + "Lectura: " + reading + System.lineSeparator();

        Files.writeString(reportFile, content);
        return reportFile;
    }
}
