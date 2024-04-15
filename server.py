import socket
import json
import google.generativeai as genai
import sys
import secret
# Replace with your actual API key
API_KEY = "AIzaSyCiI4o6AI0EFnx5L6T-Yj0gSJTaj8550us"

def generate_response(prompt):
  """
  Sends a prompt to the Gemini model and returns the generated response.
  """
  genai.configure(api_key=secret.api_key)
  Geminimodel = genai.GenerativeModel('gemini-pro')
  generated_essay = Geminimodel.generate_content(prompt).text
  return generated_essay

def start_server(host='0.0.0.0', port=2024):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server is listening on {host}:{port}...")

        try:
            while True:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    print(f"Connected by {addr}")
                    data_buffer = ""
                    while True:
                        data = client_socket.recv(1024).decode('utf-8')
                        if not data:
                            break
                        data_buffer += data
                        if '\n' in data_buffer:
                            # Split on the first newline; there might be leftover data
                            message, data_buffer = data_buffer.split('\n', 1)
                            print(f"Received message: {message}")

                            # Generate response using Gemini
                            response = generate_response(message)

                            # Send the generated response back to the client
                            client_socket.sendall((response + '\n').encode('utf-8'))
                            print(f"Sent generated response to {addr}.")

        except KeyboardInterrupt:
            print("Server is shutting down...")
            server_socket.close()
            sys.exit(0)

if __name__ == "__main__":
    start_server()
