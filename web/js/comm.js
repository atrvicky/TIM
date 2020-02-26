"use strict";

let ws;
let url = "ws://192.168.4.1:8266/"
let gamepadEnabled = true;
let joystickSizePercent = 0.25;
let joystickL;
let joystickR;
let remoteDiv = document.getElementById("remote-div");


$(() => {
    $('[data-toggle="tooltip"]').tooltip()
})

let popError = (msg) => {
    $('#error-msg').html(msg);

    $('#errorModal').modal({
        'show': true
    });
}

let showRemote = () => {
    let isRemoteVisible = remoteDiv.style.display != "none";
    remoteDiv.style.display = isRemoteVisible ? "none" : "block";
    blocklyDiv.style.display = isRemoteVisible ? "block" : "none";
    $('#mode-indicator').text(isRemoteVisible ? 'Design Mode' : 'Remote Mode');
    onresize();
};

let createJoysticks = () => {
    // try to destroy any existing instances of the joystick
    try{
        if (joystickL != null){
            joystickL.destroy();
            joystickR.destroy();
        }
    } catch (err) {
        console.log(err);
    }

    let leftJsWrapper = document.getElementById('left-joystick');
    let rightJsWrapper = document.getElementById('right-joystick');

    let joystickTop = 90 * window.innerHeight / 320;
    joystickTop += 'px';
    let joystickLeft = window.innerWidth * 0.23;
    joystickLeft += 'px';
    
    let joystickSize = window.innerWidth * joystickSizePercent
    
    joystickL = nipplejs.create({
        zone: leftJsWrapper,
        mode: 'static',
        color: 'red',
        position: { left: joystickLeft, top: joystickTop },
        size: joystickSize
    });
    
    joystickR = nipplejs.create({
        zone: rightJsWrapper,
        mode: 'static',
        color: 'red',
        position: { left: joystickLeft, top: joystickTop },
        size: joystickSize
    });
    
    // set the joystick listeners
    // nippleA start
    joystickL.on('dir', (evt, data) => {
        let dir = data.direction.angle;
        console.log('l_' + dir);
        console.log(data)
    });
    // nippleA end

    // nippleB start
    joystickR.on('dir', (evt, data) => {       
        let dir = data.direction.angle;
        console.log('r_' + dir);
    });
    // nippleB end

    // adjust the button sizes
    let btnFw = document.getElementById('btn-fw');
    let btnLt = document.getElementById('btn-lt');
    let btnRt = document.getElementById('btn-rt');
    let btnBw = document.getElementById('btn-bw');

    btnFw.className = window.innerWidth < 1020 ? "btn btn-danger btn-sm" : "btn btn-danger btn-lg";
    btnLt.className = window.innerWidth < 1020 ? "btn btn-danger btn-sm" : "btn btn-danger btn-lg";
    btnRt.className = window.innerWidth < 1020 ? "btn btn-danger btn-sm" : "btn btn-danger btn-lg";
    btnBw.className = window.innerWidth < 1020 ? "btn btn-danger btn-sm" : "btn btn-danger btn-lg";
};

createJoysticks();