import network
import socket
from time import sleep
import slow_servo
import machine

ssid='Totalplay-29A6_2.4Gnormal'
password='123456789Tp'

def webpage():
    #Template HTML
    html = f"""
            
            <!DOCTYPE html>
            <html>
            <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">

            </head>
            <body>

            <h1>Brazo de Dibujo Slider</h1>
            
            <p>Servo del hombro.</p>
            <div class="slidecontainer">
              <input type="range" min="0" max="180" value="90" class="slider" id="myRange">
              <p>Valor Inicial: <span id="demo"></span></p>
              <p>Cambiar Valor: <span id="cdemo"></span></p>
            </div>
            <br>

            <p>Servo del codo.</p>
            <div class="slidecontainer">
              <input type="range" min="0" max="180" value="90" class="slider" id="myRange2">
              <p>Valor Inicial: <span id="demo2"></span></p>
              <p>Cambiar Valor: <span id="cdemo2"></span></p>
            </div>
            <br>

            <p>Servo de la pluma.</p>
            <div class="slidecontainer">
              <input type="range" min="0" max="180" value="90" class="slider" id="myRange3">
              <p>Valor Inicial: <span id="demo3"></span></p>
              <p>Cambiar Valor: <span id="cdemo3"></span></p>
            </div>

            <script>
            var slider1 = document.getElementById("myRange");
            var output1 = document.getElementById("demo");
            var coutput1 = document.getElementById("cdemo");
            output1.innerHTML = slider1.value;

            slider1.oninput = function() {{
             output1.innerHTML = this.value;

            }}
            slider1.onchange = function() {{
              coutput1.innerHTML = this.value;
              var xhr1 = new XMLHttpRequest();
              xhr1.open("GET", "/slider?"+this.value, true);
              xhr1.send();
            }}
         
 
            var slider2 = document.getElementById("myRange2");
            var output2 = document.getElementById("demo2");
            var coutput2 = document.getElementById("cdemo2");
            output2.innerHTML = slider2.value;

            slider2.oninput = function() {{
              output2.innerHTML = this.value;

            }}
            slider2.onchange = function() {{
              coutput2.innerHTML = this.value;
              var xhr2 = new XMLHttpRequest();
              xhr2.open("GET", "/slider?"+this.value, true);
              xhr2.send();
            }}
            

            var slider3 = document.getElementById("myRange3");
            var output3 = document.getElementById("demo3");
            var coutput3 = document.getElementById("cdemo3");
            output3.innerHTML = slider3.value;

            slider3.oninput = function() {{
              output3.innerHTML = this.value;

            }}
            slider3.onchange = function() {{
              coutput3.innerHTML = this.value;
              var xhr3 = new XMLHttpRequest();
              xhr3.open("GET", "/slider?"+this.value, true);
              xhr3.send();
            }}
            </script>
            </body>
            </html>
            """
    return str(html)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def serve(connection):
    #Start a web server
    servo1 = slow_servo.Slow_Servo(0)
    servo2 = slow_servo.Slow_Servo(0)	#create servo object on pin 0
    servo3 = slow_servo.Slow_Servo(0)
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print (request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request.find('slider') > -1:
            slider_val = request.split('?')[1]
            print (slider_val)
            servo1.set_angle(slider_val,1000)
            servo2.set_angle(slider_val,1000)
            servo3.set_angle(slider_val,1000)
        html = webpage()
        client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        client.send(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
