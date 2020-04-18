let socket = io.connect('http://localhost:5000');
console.info('socket connected')

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