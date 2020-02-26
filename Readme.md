### Folder Structure

**android/**

&emsp; &emsp; The java and xml files needed for the android app. This also contains the contents required for the animated eye.

**esp/**

&emsp; &emsp; The files to be flased to the ESP module. Change the wifi configurations in `config.py` and run the `boot.py`.

**pi/**

&emsp; &emsp; The python files to be run on the raspberry. The raspberry should also be configured to run the `client.py` in headless mode.


A sample publish command

&emsp;```mosquitto_pub -h BROKER_IP -p BROKER_PORT -t TOPIC -u USERNAME -P PASSWORD -m "MESSAGE"```