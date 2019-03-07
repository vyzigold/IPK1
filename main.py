import socket
import json
import sys


# Connects to server, requests data, waits for the response and returns
# status code and json with data
def get_data(api_key, city):
    request = "GET /data/2.5/weather?q=" +\
            city +\
            "&units=metric&APPID=" +\
            api_key +\
            " HTTP/1.1\r\n" +\
            "Host: api.openweathermap.org\r\n" +\
            "Connection: close\r\n\r\n"

    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as message:
        soc = None

    try:
        soc.connect(("api.openweathermap.org", 80))
    except socket.error as message:
        soc.close()
        soc = None

    if soc is None:
        sys.stderr.write("Error: Could not connect to server api.openweathermap.org\n")
        exit(1)

    try:
        soc.sendall(bytes(request, 'utf-8'))
        response = str(soc.recv(4096), 'utf-8').splitlines()
    except socket.error as message:
        soc.close()
        sys.stderr.write("Error: Could not communicate with server\n")
        exit(1)

    soc.close()

    status_code = response[0].split(" ")[1]
    data = response[11]
    return (int(status_code), data)


# Prints the data from dictionary correctly
def print_data(data):
        print(data["name"])
        print(data["weather"][0]["description"])
        print("temp:", data["main"]["temp"], "C")
        print("humidity:", str(data["main"]["humidity"]) + "%")
        print("pressure:", data["main"]["pressure"], "hPa")
        print("wind speed:", data["wind"]["speed"], "m/s")
        try:
            print("wind degrees:", data["wind"]["deg"], "degrees")
        except:
            print("wind degrees: None")


def main():
    if sys.argv[1] == "not_set":
        sys.stderr.write("Error: Missing the api key argument.")
        exit(1)
    if sys.argv[2] == "not_set":
        sys.stderr.write("Error: Missind the city argument")
        exit(1)

    status_code, data_json = get_data(sys.argv[1], sys.argv[2])

    if status_code >= 200 and status_code < 300:
        data = json.loads(data_json)
        print_data(data)

    elif status_code >= 400 and status_code < 500:
        print("Error:", status_code)
        try:
            data = json.loads(data_json)
            print(data["message"])
        except:
            pass

    elif status_code >= 500 and status_code < 600:
        print("Error:", status_code, "\nTry it later.")

    else:
        print("Unknown error.")

if __name__ == "__main__":
    main()
