with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

chat_css = """
/* ── FULLY AI ANIMATED LIVE CHAT STYLES ── */
.chat-msg {
  animation: chatMsgAnim 0.28s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
  transition: all 0.2s ease;
}

@keyframes chatMsgAnim {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.chat-msg-ai {
  background: linear-gradient(135deg, rgba(0, 230, 118, 0.12), rgba(0, 176, 255, 0.08)) !important;
  border: 1.5px solid rgba(0, 230, 118, 0.4) !important;
  box-shadow: 0 0 16px rgba(0, 230, 118, 0.2) !important;
  border-radius: 12px !important;
}

.chat-msg-vip {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.12), rgba(255, 140, 0, 0.08)) !important;
  border: 1.5px solid rgba(255, 215, 0, 0.4) !important;
  box-shadow: 0 0 16px rgba(255, 215, 0, 0.2) !important;
  border-radius: 12px !important;
}

.chat-msg-user {
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 12px !important;
}

.ai-typing-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: rgba(0, 230, 118, 0.08);
  border: 1px dashed #00e676;
  border-radius: 10px;
  font-size: 11.5px;
  color: #00e676;
  font-weight: 700;
  margin-bottom: 8px;
  animation: chatMsgAnim 0.2s ease;
}

.typing-dot {
  width: 5px;
  height: 5px;
  background: #00e676;
  border-radius: 50%;
  animation: typingBounce 1s infinite alternate;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingBounce {
  from { transform: translateY(0); opacity: 0.4; }
  to { transform: translateY(-4px); opacity: 1; }
}
"""

if ".chat-msg-ai" not in idx:
    idx = idx.replace("</head>", "<style>\n" + chat_css + "\n</style>\n</head>")

# Clean up chat rooms in index.html with clean UTF-8
old_rooms = """      <div class="chat-rooms">
        <button class="room-btn active" id="room-english" data-room="english">? English</button>
        <button class="room-btn" id="room-hindi" data-room="hindi">?? Hindi</button>
        <button class="room-btn" id="room-vip" data-room="vip-chat">? VIP</button>
      </div>"""

new_rooms = """      <div class="chat-rooms">
        <button class="room-btn active" id="room-english" data-room="english">🌐 Global AI Room</button>
        <button class="room-btn" id="room-hindi" data-room="hindi">🇮🇳 India Room</button>
        <button class="room-btn" id="room-vip" data-room="vip-chat">👑 VIP Lounge</button>
      </div>"""

idx = idx.replace(old_rooms, new_rooms)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html chat styles and rooms updated!")