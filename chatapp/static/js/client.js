var origin = window.location.origin;
console.info(origin);
let socket = io.connect(origin);

let current_user = $('#current_user').text()

let url = window.location.href.split('/')
let room_id = url[url.length - 1]

socket.on( 'connect', () => {
    let form = $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault()
        let user_input = $( 'input#message' ).val()
        socket.emit( 'my event', {
            message : user_input,
            room_id: room_id
        })
        $( 'input#message' ).val( '' ).focus()
    })
})

socket.on( 'chat'+room_id.toString(), ( msg ) => {
    let date = dateNow()
    console.log( msg );
    if (msg.joined) {
      $( 'div.message_holder' ).append('<div><i style="color:#000">'+msg.user_name+'</i>' + ' joined the chat' + '</div>' )
    }
    if (msg.message && msg['room_id'] == room_id) {
      if (current_user == msg.user_name) {
        $( 'div.message_holder' ).append('<div class="chat chat-current"><b style="color:#000" class="left">'+ msg.user_name + '</b><p>'+msg.message+'</p><p class="time-left">'+date+'</p></div>' )
      } else {
        // $( 'div.message_holder' ).append('<div><b style="color:#000">'+msg.user_name+'</b>'+ ": " +msg.message+'</div>' )
        $( 'div.message_holder' ).append('<div class="chat chat-darker"><b style="color:#000" class="left">'+ msg.user_name + '</b><p>'+msg.message+'</p><p class="time-left">'+date+'</p></div>' )
      }
    }
    scrollSmoothToBottom('messages', 500)
})

function scrollSmoothToBottom(id, delay) {
 var div = document.getElementById(id);
 $('#'+id).animate({
    scrollTop: div.scrollHeight - div.clientHeight
 }, delay);
}

function dateNow() {
  var date = new Date();
  var aaaa = date.getFullYear();
  var gg = date.getDate();
  var mm = (date.getMonth() + 1);

  if (gg < 10)
      gg = "0" + gg;

  if (mm < 10)
      mm = "0" + mm;

  var cur_day = aaaa + "-" + mm + "-" + gg;

  var hours = date.getHours()
  var minutes = date.getMinutes()
  var seconds = date.getSeconds();

  if (hours < 10)
      hours = "0" + hours;

  if (minutes < 10)
      minutes = "0" + minutes;

  if (seconds < 10)
      seconds = "0" + seconds;

  return cur_day + " " + hours + ":" + minutes;
}

window.onload = async function() {
  scrollSmoothToBottom("messages", 200)
}
