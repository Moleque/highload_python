# import asyncio
# import uvloop

# async def main():
#     # Main entry-point.
#     ...

from server import Server

IP = "0.0.0.0"
PORT = 80

CFG_PATH = "/etc/httpd.conf"

if __name__ == "__main__":
    # config = Settings()
    # if (!config.parseConfig(CFG_PATH)):
    #     print("config file not found\nset default setting")

    server = Server(IP, PORT, "/var/www/html", 1)

    


    # uvloop.install()
#     asyncio.run(main())