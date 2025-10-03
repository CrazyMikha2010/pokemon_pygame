from handler import EventHandler


def main():
    """
    Main game loop.
    """
    handler = EventHandler()
    while handler.running:
        handler.handle_input()
        handler.update()


if __name__ == "__main__":
    main()

