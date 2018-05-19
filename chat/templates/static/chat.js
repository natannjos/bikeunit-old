
$(function() {
    // When we're using HTTPS, use WSS too.
    var roomName = {{ room_name_json }};

    var chatsock = new WebSocket(
        'ws://' + window.location.host +
        '/ws/chat/' + roomName + '/');
    
    
    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat-log")
        var ele = $('<tr></tr>')

        ele.append(
            $("<td></td>").text(data.timestamp)
        )
        ele.append(
            $("<td></td>").text(data.handle)
        )
        ele.append(
            $("<td></td>").text(data.message)
        )
        
        chat.append(ele)
    };

    $("#chat-message-submit").on("submit", function(event) {
      var message = { 
        user: $("#user").val(), 
        message: $("#chat-message-input").val()
     };

      chatsock.send(JSON.stringify(message));
      $("#message")
        .val("")
        .focus();
      return false;
    });
});