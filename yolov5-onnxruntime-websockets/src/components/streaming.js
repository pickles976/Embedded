import React from "react";

const Streamer = (props) => {

    let imageRef = props.props.imageRef
    let loadfn = props.props.loadfn
    let socket = {}

    const contactServer = () => {
    
        let ip = document.getElementById("ip").value

        console.log(`Connecting websocket server at IP: ${ip}`)

        socket = new WebSocket(`ws://${ip}:8000`)

        socket.addEventListener('open', function (event) {
            socket.send('Connection Established')
        })

        // Load image
        socket.addEventListener('message', function (event) {
            console.log(event.data);
            const url = URL.createObjectURL(event.data)
            imageRef.current.src = url
            loadfn(url)
        })
    
    }

    return ( 
        <>
            <label htmlFor="ip">Server Local IP:  </label>
            <input type="text" id="ip" name="ip"/>
            <button onClick={contactServer}>Connect</button><br></br>
        </>
    )
}

export default Streamer