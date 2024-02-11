from flask import Flask, jsonify
import adafruit_dht
import board
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

# Initialize DHT11 sensor
dht_sensor = adafruit_dht.DHT11(board.D4)

# Endpoint to get sensor data
@app.route('/sensor_data')
def get_sensor_data():
    try:
        # Read temperature and humidity from DHT11
        temperature_c = dht_sensor.temperature
        humidity = dht_sensor.humidity

        # Read gas concentration from MQ137
        gas_concentration = read_mq137_sensor()

        # Save data to MySQL database
        save_to_database(temperature_c, humidity, gas_concentration)

        return jsonify({
            'temperature': temperature_c,
            'humidity': humidity,
            'gas_concentration': gas_concentration
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def read_mq137_sensor():
    # Code to read gas sensor data goes here
    # Replace this with actual code to read data from MQ137
    return 0

def save_to_database(temperature, humidity, gas_concentration):
    cursor = db.cursor()
    sql = "INSERT INTO sensor_data (temperature, humidity, gas_concentration) VALUES (%s, %s, %s)"
    val = (temperature, humidity, gas_concentration)
    cursor.execute(sql, val)
    db.commit()

if __name__ == '__main__':
    app.run(debug=True)
