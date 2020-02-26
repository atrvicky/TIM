'use strict';

MQTTconnect();

let remoteModeOn = false;
let buttonFw = document.getElementById('btn-fw');
let buttonLt = document.getElementById('btn-lt');
let buttonRt = document.getElementById('btn-rt');
let buttonBw = document.getElementById('btn-bw');

let wheelsRadio = document.getElementById('joystickModeWheels');
let rightRadio = document.getElementById('joystickModeRight');
let leftRadio = document.getElementById('joystickModeLeft');

let wheelDivs = document.getElementsByClassName('wheels');
let jsDiv = (document.getElementsByClassName('js'))[0];


wheelsRadio.onchange = (e) => {
    // console.log(e)
    for (const wheel of wheelDivs) {
        wheel.style.display = "flex";
    }    
    jsDiv.style.display = "none"; 
};

leftRadio.onchange = () => {
    for (const wheel of wheelDivs) {
        wheel.style.display = "none";
    }    
    jsDiv.style.display = "flex"; 
};

rightRadio.onchange = () => {
    for (const wheel of wheelDivs) {
        wheel.style.display = "none";
    }    
    jsDiv.style.display = "flex"; 
};

let fwDown = false;
let ltDown = false;
let rtDown = false;
let bwDown = false;
let lastKey = 32;   // space


// mqtt topics
let dcTopic = "dcmt";
let dcFw = "fw";
let dcBw = "bw";
let dcLt = "lt";
let dcRt = "rt";
let dcSt = "st";
let dcSl = "sl";
let dcSr = "sr";

// Event callbacks

let kdwn = (key) => {
    if ((key == 38) && !fwDown) {
        fwDown = true;
        buttonFw.focus();
    } else if ((key == 37) && !ltDown) {
        ltDown = true;
        buttonLt.focus();
    } else if ((key == 39) && !rtDown) {
        rtDown = true;
        buttonRt.focus();
    } else if ((key == 40) && !bwDown) {
        bwDown = true;
        buttonBw.focus();
    }
};

let kup = (key) => {
    if ((key == 38) && fwDown) {
        fwDown = false;
        buttonFw.blur();
    } else if ((key == 37) && ltDown) {
        ltDown = false;
        buttonLt.blur();
    } else if ((key == 39) && rtDown) {
        rtDown = false;
        buttonRt.blur();
    } else if ((key == 40) && bwDown) {
        bwDown = false;
        buttonBw.blur();
    }
};

// global key detector
document.onkeydown = (event) => {
    if (event.which == 32){
        kdwn(lastKey);
    } else {
        kdwn(event.which);
        lastKey = event.which;
    } 
};

document.onkeyup = (event) => {
    if (event.which == 32){
        kup(lastKey);
    } else {
        kup(event.which);
        lastKey = event.which;
    } 
};


//buttonA start
buttonFw.addEventListener('focus', (e) => {
    console.log('fwk.');
    send_message(dcTopic, dcFw);
});
buttonFw.addEventListener('blur', (e) => {
    console.log('fwk');
    send_message(dcTopic, dcSt);
});

buttonFw.addEventListener('mousedown', (e) => {
    console.log('fw.');
    send_message(dcTopic, dcFw);
});
buttonFw.addEventListener('mouseup', (e) => {
    console.log('fw');
    send_message(dcTopic, dcSt);
});
//buttonA end

// buttonB start
buttonLt.addEventListener('focus', (e) => {
    console.log('ltk.');
    send_message(dcTopic, dcLt);
});
buttonLt.addEventListener('blur', (e) => {
    console.log('ltk');
    send_message(dcTopic, dcSt);
});

buttonLt.addEventListener('mousedown', (e) => {
    console.log('lt.');
    send_message(dcTopic, dcLt);
});
buttonLt.addEventListener('mouseup', (e) => {
    console.log('lt');
    send_message(dcTopic, dcSt);
});
// buttonB end

// buttonC start
buttonRt.addEventListener('focus', (e) => {
    console.log('rtk.');
    send_message(dcTopic, dcRt);
});
buttonRt.addEventListener('blur', (e) => {
    console.log('rtk');
    send_message(dcTopic, dcSt);
});

buttonRt.addEventListener('mousedown', (e) => {
    console.log('rt.');
    send_message(dcTopic, dcRt);
});
buttonRt.addEventListener('mouseup', (e) => {
    console.log('rt');
    send_message(dcTopic, dcSt);
});
// buttonC end

// buttonD start
buttonBw.addEventListener('focus', (e) => {
    console.log('bwk.');
    send_message(dcTopic, dcBw);
});
buttonBw.addEventListener('blur', (e) => {
    console.log('bwk');
    send_message(dcTopic, dcSt);
});

buttonBw.addEventListener('mousedown', (e) => {
    console.log('bw.');
    send_message(dcTopic, dcBw);
});
buttonBw.addEventListener('mouseup', (e) => {
    console.log('bw');
    send_message(dcTopic, dcSt);
});
// buttonD end