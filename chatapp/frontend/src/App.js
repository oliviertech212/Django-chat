// import React, { useState, useEffect, useRef } from "react";

// const ChatApp = () => {
//   const [messages, setMessages] = useState([]);
//   const [newMessage, setNewMessage] = useState("");
//   const token = "4fa59484a5eee311a74989a5e42c97b9646e3f00"; // Replace with your token
//   const roomName = "2"; // Dynamic room name
//   const wsUrl = `ws://127.0.0.1:8000/ws/chat/${roomName}/?token=${token}`;
  
//   // Ref to store WebSocket connection
//   const socketRef = useRef(null);

//   useEffect(() => {
//     // Open WebSocket connection once
//     socketRef.current = new WebSocket(wsUrl);

//     socketRef.current.onopen = () => {
//       console.log("Connected to WebSocket server");
//     };

//     socketRef.current.onmessage = (event) => {
//       const data = JSON.parse(event.data);
//       if (data.message) {
//         setMessages((prev) => [...prev, data.message]);
//       }
//     };

//     socketRef.current.onclose = () => {
//       console.log("Disconnected from WebSocket server");
//     };

//     socketRef.current.onerror = (error) => {
//       console.error("WebSocket error:", error);
//     };

//     // Cleanup on unmount
//     return () => {
//       socketRef.current.close();
//     };
//   }, [wsUrl]);

//   const sendMessage = () => {
//     if (newMessage.trim() && socketRef.current) {
//       const messageData = JSON.stringify({ message: newMessage });
//       socketRef.current.send(messageData); // Send message via the existing socket
//       setMessages((prev) => [...prev, `You: ${newMessage}`]);
//       setNewMessage("");
//     }
//   };

//   return (
//     <div>
//       <div>
//         <h1 className="underline text-[green]">Chat Room {roomName}</h1>
//         <div className="text-3xl font-bold">
//           {messages.map((msg, idx) => (
//             <div key={idx}>{msg}</div>
//           ))}
//         </div>
//       </div>
//       <input
//         type="text"
//         value={newMessage}
//         onChange={(e) => setNewMessage(e.target.value)}
//         placeholder="Type a message..."
//       />
//       <button onClick={sendMessage}>Send</button>
//     </div>
//   );
// };

// export default ChatApp;


import React, { useState, useEffect, useRef } from "react";

const ChatApp = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const token = "4fa59484a5eee311a74989a5e42c97b9646e3f00"; // Replace with your token
  const roomName = "2"; // Dynamic room name
  const wsUrl = `ws://127.0.0.1:8000/ws/chat/${roomName}/?token=${token}`;
  
  // Ref to store WebSocket connection
  const socketRef = useRef(null);

  useEffect(() => {
    // Open WebSocket connection once
    socketRef.current = new WebSocket(wsUrl);

    socketRef.current.onopen = () => {
      console.log("Connected to WebSocket server");
    };

    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      console.log("data when connected to the server", data);

      // Handle the previous messages sent by the backend (initial messages)
      if (data.messages) {
        setMessages(data.messages); // Set the initial message list from the backend
      }

      // Handle new incoming messages (when someone else sends a message)
      if (data.message) {
        setMessages((prev) => [...prev, `${data.sender}: ${data.message}`]); // Add new message to the state
      }
    };

    socketRef.current.onclose = () => {
      console.log("Disconnected from WebSocket server");
    };

    socketRef.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    // Cleanup on unmount
    return () => {
      socketRef.current.close();
    };
  }, [wsUrl]);

  const sendMessage = () => {
    if (newMessage.trim() && socketRef.current) {
      const messageData = JSON.stringify({ message: newMessage });
      socketRef.current.send(messageData); // Send message via the existing socket
      setMessages((prev) => [...prev, `You: ${newMessage}`]); // Add message to local state for immediate display
      setNewMessage("");
    }
  };

  return (
    <div>
      <div>
        <h1 className="underline text-[green]">Chat Room {roomName}</h1>
        <div className="text-3xl font-bold">
          {messages.map((msg, idx) => (
            <div key={idx}>
              {/* Render the text of each message */}
              {msg.text || `${msg.sender}: ${msg.message}`}
            </div>
          ))}
        </div>
      </div>
      <input
        type="text"
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
        placeholder="Type a message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default ChatApp;
