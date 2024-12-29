import React, { useState, useEffect } from "react";

const ChatApp = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [socket, setSocket] = useState(null);
  const roomName = "1";  // Or dynamic room name

  useEffect(() => {
    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${roomName}/`);

    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setMessages((prev) => [...prev, data.message]);
    };

    setSocket(ws);

    return () => ws.close();
  }, [roomName]);

  const sendMessage = () => {
    if (socket && newMessage.trim()) {
      socket.send(JSON.stringify({ message: newMessage }));
      setMessages((prev) => [...prev, `You: ${newMessage}`]);
      setNewMessage("");
    }
  };

  return (
    <div>
      <div>
        <h1>Chat Room {roomName}</h1>
        <div>
          {messages.map((msg, idx) => (
            <div key={idx}>{msg}</div>
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
