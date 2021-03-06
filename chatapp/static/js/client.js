let origin = window.location.origin;
console.info(origin);
let socket = io.connect(origin);

let current_user = $('#current_user').text()

let url = window.location.href.split('/')
let room_id = url[url.length - 1]

if (room_id === 'general') {
  room_id = 10000000
}

$(document).ready(function() {
  $(window).resize(function() {
      let bodyheight = $(window).height();
      $("#messages").height(`${bodyheight*0.75}px`);
  }).resize();
});


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
    if (msg.message && msg['room_id'] === room_id) {
      $('div.message_holder').append('<div id="username"><p id="" style="color:#000" style="margin-bottom: 0;"><strong>'+msg.user_name+'</strong><span class="msg-time">'+formatAMPM(new Date)+'</span></p><p style="margin-bottom: 10px;">'+msg.message+'</p></div>')
      // if (current_user == msg.user_name) {
      //   $( 'div.message_holder' ).append('<div class="chat chat-current"><b style="color:#000" class="left">'+ msg.user_name + '</b><p>'+msg.message+'</p><p class="time-left">'+date+'</p></div>' )
      // } else {
      //   // $( 'div.message_holder' ).append('<div><b style="color:#000">'+msg.user_name+'</b>'+ ": " +msg.message+'</div>' )
      //   $( 'div.message_holder' ).append('<div class="chat chat-darker"><b style="color:#000" class="left">'+ msg.user_name + '</b><p>'+msg.message+'</p><p class="time-left">'+date+'</p></div>' )
      // }
    }
    scrollSmoothToBottom('messages', 500)
})

function scrollSmoothToBottom(id, delay) {
 let div = document.getElementById(id);
 $('#'+id).animate({
    scrollTop: div.scrollHeight - div.clientHeight
 }, delay);
}

function dateNow() {
  let date = new Date();
  let aaaa = date.getFullYear();
  let gg = date.getDate();
  let mm = (date.getMonth() + 1);

  if (gg < 10)
      gg = "0" + gg;

  if (mm < 10)
      mm = "0" + mm;

  let cur_day = aaaa + "-" + mm + "-" + gg;

  let hours = date.getHours()
  let minutes = date.getMinutes()
  let seconds = date.getSeconds();

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

function formatAMPM(date) {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    let strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}
