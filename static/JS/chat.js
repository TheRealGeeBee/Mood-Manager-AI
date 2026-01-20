const socket = io();

function sendMessage() {
    const input = document.getElementById("chat-input");
    const message = input.value.trim();
    if (!message) return;

    addMessage("You", message);
    socket.emit("user_message", { message });

    input.value = "";
}

// Listen for AI messages
socket.on("ai_message", data => {
    addMessage("AI", data.message);
});

// Append message to chat box
function addMessage(sender, text) {
    const box = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.innerHTML = `<b>${sender}:</b> ${text}`;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}
