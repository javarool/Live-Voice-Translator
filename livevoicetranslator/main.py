# livevoicetranslator/main.py
import asyncio
from controllers.main_controller import MainController

def main():
    controller = MainController()
    asyncio.run(controller.run())

if __name__ == '__main__':
    main()
