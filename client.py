import tkinter as tk
from tkinter import messagebox
import websockets
import asyncio
import threading

class ChatApp:
    def __init__(self, root, websocket_url="ws://localhost:6789"):
        self.root = root
        self.websocket_url = websocket_url
        self.root.title("WebSocket Chat")

        # Create the GUI components
        self.chat_box = tk.Text(self.root, height=20, width=50, state=tk.DISABLED)
        self.chat_box.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack(padx=10, pady=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        self.client_socket = None
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_event_loop, daemon=True).start()

    def start_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())

    async def connect(self):
        try:
            self.client_socket = await websockets.connect(self.websocket_url)
            await self.receive_messages()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")
            self.root.quit()

    async def receive_messages(self):
        try:
            async for message in self.client_socket:
                self.display_message(message)
        except:
            pass

    def send_message(self):
        message = self.message_entry.get()
        if message:
            asyncio.run(self.client_socket.send(message))
            self.display_message(f"You: {message}")
            self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, message + "\n")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.yview(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
