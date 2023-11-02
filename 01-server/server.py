import http.server
import socketserver

# Defina a porta que o servidor irá ouvir
port = 8080

# Defina o diretório raiz onde os arquivos estão localizados
directory = "."  # Pode ser ajustado para o diretório correto

# Crie um manipulador para o servidor
handler = http.server.SimpleHTTPRequestHandler

# Inicie o servidor na porta especificada
with socketserver.TCPServer(("", port), handler) as httpd:
    print(f"Servidor rodando na porta {port}")
    # Mude para o diretório correto antes de iniciar o servidor
    httpd.RequestHandlerClass.directory = directory
    # Mantenha o servidor em execução indefinidamente
    httpd.serve_forever()
