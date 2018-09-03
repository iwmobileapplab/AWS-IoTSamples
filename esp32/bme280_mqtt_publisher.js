load('api_timer.js');
load('api_arduino_bme280.js');
load('api_mqtt.js');

// Sensors address (Usually: 0x76 or 0x77)
let sens_addr = 0x76;

// Initialize Adafruit_BME280 library using the I2C interface
let bme = Adafruit_BME280.createI2C(sens_addr);

let TOPIC  = 'BME280';
let qos = 1;

if (bme === undefined) {
    print('Cant find a sensor');
} else {
    // This function reads data from the BME280 sensor every 10 seconds
    Timer.set(10000 /* milliseconds */ , true /* repeat */ , function() {

        let temperature = bme.readTemperature();
        let humidity = bme.readHumidity();
        let pressure = bme.readPressure();
        print('Temperature:', temperature, '*C');
        print('Humidity:', humidity, '%RH');
        print('Pressure:', pressure, 'hPa');

        let message = JSON.stringify({
            "Temperature": temperature,
            "Humidity": humidity,
            "Pressure": pressure
        });
        let ret = MQTT.pub(TOPIC, message, qos);
        print('Published:', ret ? 'yes' : 'no', ', topic:', TOPIC, ', message:', message);
        print();

    }, null);
}

