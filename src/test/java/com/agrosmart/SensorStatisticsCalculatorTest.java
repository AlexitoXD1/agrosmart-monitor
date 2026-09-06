package com.agrosmart;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.Collections;
import java.util.List;

import org.junit.jupiter.api.Test;

class SensorStatisticsCalculatorTest {

    @Test
    void debeCalcularEstadisticasCorrectamente() {
        List<TemperatureReading> readings = List.of(
            new TemperatureReading(5.0, 50.0),  // NORMAL
            new TemperatureReading(9.0, 60.0),  // WARNING
            new TemperatureReading(11.0, 70.0)  // ALERT
        );

        SensorStatisticsCalculator calculator = new SensorStatisticsCalculator(readings);

        assertEquals(3, calculator.getTotalReadings());
        assertEquals(5.0, calculator.getMinTemperature());
        assertEquals(11.0, calculator.getMaxTemperature());
        assertEquals(8.33, calculator.getAverageTemperature());
        assertEquals(60.0, calculator.getAverageHumidity());
        assertEquals(1, calculator.getNormalCount());
        assertEquals(1, calculator.getWarningCount());
        assertEquals(1, calculator.getAlertCount());
    }

    @Test
    void debeLanzarExcepcionSiLaListaEstaVacia() {
        assertThrows(IllegalArgumentException.class, () -> new SensorStatisticsCalculator(Collections.emptyList()));
    }
}
