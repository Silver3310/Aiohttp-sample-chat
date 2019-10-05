document.addEventListener("DOMContentLoaded", function(){
    let sock = {};

    try{
        sock = new WebSocket('ws://' + window.location.host + '/ws');
    }
    catch(err) {
        sock = new WebSocket('wss://' + window.location.host + '/ws');
    }

    // show message in div#subscribe
    function showMessage(message) {
        let messageElem = $('#messages'),
            height = 0,
            date = new Date(),
            options = { hour12: false },
            htmlText = '[' + date.toLocaleTimeString('en-US', options) + '] ';

        try{
            let messageObj = JSON.parse(message);
            if (!!messageObj.user && !!messageObj.msg){
                htmlText = htmlText  +
                '<span class="user">' + messageObj.user + '</span>:' + messageObj.msg + '\n';
            } else {
                htmlText = htmlText + message;
            }
        } catch (e){
            htmlText = htmlText + message;
        }
        messageElem.append($('<p>').html(htmlText));

        messageElem.find('p').each(function(i, value){
            height += parseInt($(this).height(), 10);
        });
        messageElem.animate({scrollTop: height});
    }

    function sendMessage(){
        let msg = $('#message');
        sock.send(msg.val());
        msg.val('');
        // JQuery's focus is deprecated for some reason
        document.getElementById("message").focus();
    }

    sock.onopen = function(){
        showMessage('Connection to server started');
    };

    // send message from form
    $('#submit').on('click',function() {
        sendMessage();
    });

    // send messages by pressing the enter button
    document.getElementById('message').addEventListener("keyup", event => {
      if (event.code === "Enter") {
          sendMessage()
      }
    });


    // income message handler
    sock.onmessage = function(event) {
        showMessage(event.data);
    };

    $('#exit').on('click',function(){
        window.location.href = "signout";
    });

    sock.onclose = function(event){
        if(event.wasClean){
            showMessage('Clean connection end');
        }else{
            showMessage('Connection broken');
        }
    };

    sock.onerror = function(error){
        showMessage(error);
    };
});

