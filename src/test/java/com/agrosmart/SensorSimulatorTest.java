package com.agrosmart;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

class SensorSimulatorTest {

    @Test
    void lasLecturasDebenEstarDentroDeRangosRealistas() {
        SensorSimulator simulator = new SensorSimulator(42L);

        for (int i = 0; i < 20; i++) {
            TemperatureReading reading = simulator.nextReading();
            assertTrue(reading.getTemperature() >= 2.0 && reading.getTemperature() <= 12.0);
            assertTrue(reading.getHumidity() >= 45.0 && reading.getHumidity() <= 90.0);
        }
    }
}
