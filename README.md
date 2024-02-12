# ECG Arduino Project

## About Project

Main target of this project was to create lightweight station to measure ECG signal during workout on treadmill.
Station consists of 2 sensors conected to arudino microcontroller. First sensor is the ECG signal sensor, it is connected to the runnner
by the electrodes. The second sensor is the 3 axis accelerometer that is taped to runners hand. 
Whole sensor data is being recoreded and being sent to the cloud using arudino connected to pc. Data is then being processed.
To make it more interactive, we added dashboard and we made sure you could set dashboard online on cloud, by adding the SQL training database.
Thanks to that you can look at your past trainings and analyse performance.


## Hardware

In project we had used 2 sensors conected to Arduino Uno microcontroller:
 - For ECG signal we have used ECG Sensor - AD8232. We got it cheaply from aliexpress. 
 - For acceleartion values we have used 3-axis accelerometer - ADXL345. 
 - As our main board we used Arudino Uno clone - UNO R3 CH340 from some chinese manufacturer.

 ### Sensor conections:
 
![Conection1](https://github.com/eryk0wski/EKG_Arduino_InterfaceApp/assets/121037666/3e23f92a-dff5-4c8c-9412-5763eb34ea06)

![Conection2](https://github.com/eryk0wski/EKG_Arduino_InterfaceApp/assets/121037666/009e2b69-8761-4a1c-8097-0967fd0e6442)


## Screenshots

Interactive Dashboard

![Image0](https://github.com/eryk0wski/EKG_Arduino_InterfaceApp/assets/121037666/2983f61c-f7e5-4041-9737-5cf2917e462c)

![Image1](https://github.com/eryk0wski/EKG_Arduino_InterfaceApp/assets/121037666/6ae081b4-d1d9-4a46-98de-35d92e75847a)

![Image2](https://github.com/eryk0wski/EKG_Arduino_InterfaceApp/assets/121037666/f36a561d-cb0c-4590-aa71-4d509c55442e)

![Image3](https://github.com/eryk0wski/EKG_Arduino_InterfaceApp/assets/121037666/309a7f8c-8483-4f7a-bd44-2cbe7b5b8b58)



## Project implementation
You can set it yourself e.g. using Heroku. All required files are already included.

## Usage
To run the app locally you need to type in the the cmd in your project folder:

    streamlit run dashboard.py
 In case of blocked port you could change port manually by typing:
		
    streamlit run dashboard.py --server.port 8510

## Instalation
For dashboard to work you need to first install libraries used in the project.
The recomended way to do this is to use `pip`

    pip install pandas
    pip install numpy
    pip install sqlalchemy
    pip install streamlit
    pip install plotly
    pip install psycopg2
    pip install tkinter

 ## Configuration

 ### Arudino set up

At first you need to set up your arduino correctly, conect the sensors like shown in paragraph 'Sensor conection'.
Then it is neccessary to to upload file 'arduino_file.ino' to your board.

### Setting the site up

At first you need to fork this repository. Then create app in Heroku and database conected to it. Copy database info from database provider and put it into files 'RecordTraining.py' and 'dashboard.py'.
From now on you will be working with the database and site dependent up on it.

### Recording training

To record training you must open file 'RecordTraining.py'. Check if the COM port number which is already in the file is same as the port which Arduino connects to your PC, if not change it to correct value.
Before starting the training, tape the electrodes to your body in correct positions and tape accelerometer to your hand. After that being done you are ready to run the the file.
After running the file, you will be met with the window in which you have to put the training name that will be put into database, from then you will refer to this training as this name.
Now you can start training. If you want to stop recording just press stop the code in your IDE.

### Dashboard
Connect to the url that heroku chose for your app. Then in the training name window type the training name that you had chosen before. 

Voilà, now you have your full training data and statistics.
