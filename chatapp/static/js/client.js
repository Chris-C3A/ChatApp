var origin = window.location.origin;
console.info(origin);
// let socket = io.connect('http://' + document.domain + ':' + location.port);
let socket = io.connect(origin);
console.info('socket connected kis emak')

socket.on( 'connect', () => {
    console.info('socket on connect')
    // socket.emit( 'my event', {
    //     data: 'User Connected'
    // })
    let form = $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault()
        let user_input = $( 'input.message' ).val()
        socket.emit( 'my event', {
        message : user_input
        })
        $( 'input.message' ).val( '' ).focus()
    })
})

socket.on( 'my response', ( msg ) => {
    console.log( msg )
    $( 'div.message_holder' ).append('<div><b style="color:#000">'+msg.user_name+'</b>'+ ": " +msg.message+'</div>' )
})