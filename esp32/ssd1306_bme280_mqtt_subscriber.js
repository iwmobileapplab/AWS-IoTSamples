load('api_timer.js');
load('api_arduino_ssd1306.js');
load('api_mqtt.js');

let TOPIC = 'BME280';
let obj;
let temperature = 0;
let humidity = 0;
let pressure = 0;

// Initialize Adafruit_SSD1306 library (I2C)
let disp = Adafruit_SSD1306.create_i2c(4 /* RST GPIO */ , Adafruit_SSD1306.RES_128_64);
// Initialize the display.
disp.begin(Adafruit_SSD1306.SWITCHCAPVCC, 0x3C, true /* reset */ );
disp.display();

let showStr = function(disp, str) {
    disp.clearDisplay();
    disp.setTextSize(1);
    disp.setTextColor(Adafruit_SSD1306.WHITE);
    disp.setCursor(disp.width() / 5, disp.height() / 5);
    disp.write(str);
    disp.display();
};

showStr(disp, "Initializing...");

MQTT.sub(TOPIC, function(conn, TOPIC, msg) {
    print('Topic: ', TOPIC, 'message:', msg);
    obj = JSON.parse(msg);
    temperature = obj.Temperature;
    humidity = obj.Humidity;
    pressure = obj.Pressure;

    showStr(disp, "\n" +
        "Temp.    " + JSON.stringify(temperature) + "\n" +
        "Humidity " + JSON.stringify(humidity) + "\n" +
        "Pressure " + JSON.stringify(pressure) + "");
}, null);

