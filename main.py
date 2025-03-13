from All_the_logic.logic import *
import asyncio
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling())
