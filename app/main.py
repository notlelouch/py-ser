import socket
import threading

directory = "/tmp/data/codecrafters.io/http-server-tester/" 
    

def handle_client(client_socket, directory):
    # Existing code for handling a single client
    request_data = client_socket.recv(1024).decode("utf-8")
    response = handle_request(request_data, directory)
    if response is not None:
        client_socket.send(response.encode("utf-8"))
    client_socket.close()


def handle_request(request_data, directory):
    # Split the request data into lines
    lines = request_data.strip().split("\r\n")

    # Extract the request line
    request_line = lines[0].split()
    
    if len(request_line) != 3:
        response = "HTTP/1.1 400 Bad Request\r\n\r\nInvalid request"
        return response 

    method, path, protocol = request_line

    if not path.startswith("/"):
        response = "HTTP/1.1 404 Not Found\r\n\r\nInvalid path"
        return response

    if method != "GET":
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod not supported"
        return response

    # Initialize a dictionary to store headers
    headers = {}

    # Start from the second line, which is the first header
    for line in lines[1:]:
        if not line:
            # An empty line indicates the end of headers
            break
        # Split the header into name and value
        header_name, header_value = line.split(":", 1)
        headers[header_name] = header_value.strip()

    # Process the request based on the path
    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\nHello, World!"

    elif path.startswith("/echo/"):
        # Get the echo content from the path
        echo_content = path[len("/echo/"):]
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/plain\r\n"
        response += f"Content-Length: {len(echo_content)}\r\n"
        response += "\r\n"  # End of headers
        response += echo_content  # Response content

    elif path.startswith("/user-agent"):
        # Get the echo content from the path
        echo_content = headers["User-Agent"]
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/plain\r\n"
        response += f"Content-Length: {len(echo_content)}\r\n"
        response += "\r\n"  # End of headers
        response += echo_content 

    elif path.startswith("/files/"):
        # Extract the filename from the path
        filename = path[len("/files/"):]

        # Build the full path to the file
        file_path = os.path.join(directory, filename)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_content = file.read()
                response = "HTTP/1.1 200 OK\r\n"
                response += "Content-Type: application/octet-stream\r\n"
                response += f"Content-Length: {len(file_content)}\r\n"
                response += "\r\n"  # End of headers
                response = response.encode("utf-8") + file_content
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\nPage not found"

    return response

def main():
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, client_address = server_socket.accept()# wait for client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
        
if __name__ == "__main__":
    main()
