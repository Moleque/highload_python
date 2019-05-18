class Settings:

    def __init__(self):
        self.cpu = 4
        self.thread = 256
        self.root = '/var/www/html'

    #  парсинг конфигурационного файла
    def parseConfig(path):
        with open(path) as file:


int parseConfig(const std::string path, struct Settings* config) {
    std::ifstream file(path);
    if (!file.is_open()) {
        return -1;
    }

    std::string line;
    while (getline(file, line)) {
        std::istringstream stream(line);
        std::string field, value;
        stream >> field >> value;
        
        if (field == "cpu_limit") {
            config->cpu = std::atol(value.c_str());
        } else if (field == "thread_limit") {
            config->thread = std::atol(value.c_str());            
        } else if (field == "document_root") {
            config->root = value;            
        }
    }
    
    return 0;
}
