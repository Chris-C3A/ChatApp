var origin = window.location.origin;
console.info(origin);
let socket = io.connect(origin);

socket.on( 'connect', () => {
    let form = $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault()
        let user_input = $( 'input#message' ).val()
        socket.emit( 'my event', {
            message : user_input
        })
        $( 'input#message' ).val( '' ).focus()
    })
})

socket.on( 'my response', ( msg ) => {
    console.log( msg );
    if (msg.joined) {
      $( 'div.message_holder' ).append('<div><i style="color:#000">'+msg.user_name+'</i>' + ' joined the chat' + '</div>' )
    }
    if (msg.message) {
      $( 'div.message_holder' ).append('<div><b style="color:#000">'+msg.user_name+'</b>'+ ": " +msg.message+'</div>' )
    }
})
