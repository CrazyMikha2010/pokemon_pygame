from handler import EventHandler


handler = EventHandler()
while handler.running:
    handler.handle_input()
            
    handler.update()

