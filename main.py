from settings.config import Settings
# from server.server import Server

IP = "0.0.0.0"
PORT = 80

CFG_PATH = "/etc/httpd.conf"

if __name__ == "__main__":
    config = Settings()
    if not config.parseConfig(CFG_PATH):
        print("config file not found\nset default setting")

    print(config.cpu, config.thread, config.root)
    # server = Server(IP, PORT, config.root, config.cpu)