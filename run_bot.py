import colorama as cl
import asyncio
import logging

from bot import main

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(cl.Fore.RED,'stopped',cl.Fore.RESET)
