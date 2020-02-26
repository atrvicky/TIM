"use strict";

let connected_flag = 0;
let mqtt;
let reconnectTimeout = 2000;
let host = "192.168.0.111";
let port = 1995;

let onConnectionLost = () => {
    console.log("connection lost");
    connected_flag = 0;
}

let onFailure = (message) => {
    console.log("Failed");
    setTimeout(MQTTconnect, reconnectTimeout);
}

let onMessageArrived = (r_message) => {
    out_msg = "Message received " + r_message.payloadString + "<br>";
    out_msg = out_msg + "Message received Topic " + r_message.destinationName;
    //console.log("Message received ",r_message.payloadString);
    console.log(out_msg);
}

let onConnected = (recon, url) => {
    console.log(" in onConnected " + reconn);
}

let onConnect = () => {
    // Once a connection has been made, make a subscription and send a message.
    connected_flag = 1
    console.log("Connected to " + host + "on port " + port);
    console.log("on Connect: " + connected_flag);
    //mqtt.subscribe("sensor1");
    //message = new Paho.MQTT.Message("Hello World");
    //message.destinationName = "sensor1";
    //mqtt.send(message);
}

let MQTTconnect = () => {
    console.log("connecting to " + host + " " + port);
    mqtt = new Paho.MQTT.Client(host, port, "clientjsaaa");
    //document.write("connecting to "+ host);
    let options = {
        timeout: 3,
        onSuccess: onConnect,
        onFailure: onFailure,

    };

    mqtt.onConnectionLost = onConnectionLost;
    mqtt.onMessageArrived = onMessageArrived;
    mqtt.onConnected = onConnected;

    mqtt.connect(options);
    return false;
}

let sub_topics = (topic) => {
    if (connected_flag == 0) {
        let out_msg = "Not Connected so can't subscribe"
        console.log(out_msg);
        return false;
    }
    console.log("Subscribing to topic =" + topic);
    mqtt.subscribe(topic);
    return false;
}

let send_message = (topic, message) => {
    if (connected_flag == 0) {
        let out_msg = "Not Connected so can't send"
        console.log(out_msg);
        return false;
    }
    console.log("To be sent: " + msg);

    message = new Paho.MQTT.Message(msg);
    if (topic == "")
        message.destinationName = "test-topic"
    else
        message.destinationName = topic;
    mqtt.send(message);
    return false;
}