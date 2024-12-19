import socket
import time
import os
import re
import argparse
import pendulum

server_list = ['irc.server1.com:6667', 'irc.server2.com:6667']
server_index = 0
channel = "#services"
nickname = "fido"
realname = "i fetch MOTD, LUSERS, MAP, and LIST."
data_dir = "./data"
#change this to 0 or bot will die
die = 1

def print_fido():
    print("""

             .       ..
   oec :    @88>   dF
  @88888    %8P   '88bu.             u.
  8"*88%     .    '*88888bu    ...ue888b
  8b.      .@88u    ^"*8888N   888R Y888r
 u888888> ''888E`  beWE "888L  888R I888>
  8888R     888E   888E  888E  888R I888>
  8888P     888E   888E  888E  888R I888>
  *888>     888E   888E   888F u8888cJ888
  4888      888&  .888N..888   "*888*P"
  '888      R888"  `"888*""      'Y"
   88R       ""       ""
   88>
   48       v1
   '8
    """)

# Define a mapping of IRC color codes to HTML colors
IRC_COLORS = {
    '00': 'white', '01': 'black', '02': 'blue', '03': 'green', '04': 'red', '05': 'brown',
    '06': 'purple', '07': 'orange', '08': 'yellow', '09': 'light green', '10': 'cyan',
    '11': 'light cyan', '12': 'light blue', '13': 'pink', '14': 'grey', '15': 'light grey'
}


def remove_unicode(text):
    # Use a regular expression to replace non-ASCII characters and IRC color codes with an empty string
    return re.sub(r'[\x00-\x1F\x80-\xFF]|\x03\d{1,2}', '', text)

def irc_to_html(text):
    # Convert spaces to non-breaking spaces first
    text = text.replace(" ", "&nbsp;")

    # Replace IRC colors with HTML spans
    def replace_color(match):
        color_code = match.group(1)
        html_color = IRC_COLORS.get(color_code.zfill(2), 'black')  # Default to black if not found
        return f'<span style="color: {html_color}">'

    # Handle closing color tags and unwanted characters
    text = re.sub(r'\x03([0-9]{1,2})', replace_color, text)
    text = re.sub(r'\x03', '</span>', text)  # Close the span on color reset
    text = re.sub(r'\x02', '', text)  # Remove the bold control character
    text = text.replace("\n", "<br>")

    return text

def create_html_file(filepath, content, timestamp):
    with open(filepath, "w") as html_file:
        html_file.write(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>IRC Data</title>
            <style>
                body {{
                    font-family: 'Courier New', Courier, monospace;
                    white-space: pre-wrap;  /* preserves whitespace and line breaks */
                }}
                span {{
                    white-space: nowrap;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
            <body>🐶 This was fetched on {timestamp}<br><br>{content}
            </body>
        </html>
        """)


def irc_connect(server, port):
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))
    return irc

def send_command(irc, command):
    irc.send(f"{command}\r\n".encode('utf-8'))

def receive_data(irc):
    buffer = ""
    while True:
        data = irc.recv(1024).decode('utf-8', errors='ignore')  # Ignore errors
        buffer += data
        lines = buffer.split("\r\n")
        buffer = lines.pop()
        for line in lines:
            yield line

def main(connection_duration):
    global server_index
    global nickname
    global oldnick
    global channel
    global oldchan
    print("=================================================================")
    print_fido()
    print("=================================================================")
    print(f"Server List: {server_list[0]}")
    for each in server_list[1:]:
        print(f"             {each}")
    print(f"Server Index: {server_index}")
    print(f"Channel: {channel}")
    print(f"Nickname: {nickname}")
    print(f"Realname: {realname}")
    print(f"Data Directory: {data_dir}")
    print("=================================================================")
    irc = None  # Initialize irc outside the loop to access in except block
    oldchan = channel
    oldnick = nickname
    try:
        while True:
            server, port = server_list[server_index].split(':')
            port = int(port)

            print(f"Connecting to {server}:{port}")
            irc = irc_connect(server, port)
            send_command(irc, f"NICK {nickname}")
            send_command(irc, f"USER {nickname} 0 * :{realname}")

            motd_fetched = False
            lusers_fetched = False
            map_fetched = False
            list_fetched = False

            # Clear existing files
            motd_path = os.path.join(data_dir, f"{server}.motd")
            lusers_path = os.path.join(data_dir, f"{server}.lusers")
            map_path = os.path.join(data_dir, f"{server}.map")
            list_path = os.path.join(data_dir, f"{server}.list")
            motd_html_path = os.path.join(data_dir, f"{server}.motd.html")
            lusers_html_path = os.path.join(data_dir, f"{server}.lusers.html")
            map_html_path = os.path.join(data_dir, f"{server}.map.html")
            list_html_path = os.path.join(data_dir, f"{server}.list.html")

            with open(motd_path, "w"), open(motd_html_path, "w"):
                pass
            with open(lusers_path, "w"), open(lusers_html_path, "w"):
                pass
            with open(map_path, "w"), open(map_html_path, "w"):
                pass
            with open(list_path, "w"), open(list_html_path, "w"):
                pass

            motd_html_content = ""
            lusers_html_content = ""
            map_html_content = ""
            list_html_content = "<table><tr><th>Channel</th><th>Users</th><th>Topic</th></tr>"
            timestamp = pendulum.now().in_tz('America/New_York').format('dddd, MMM Do h:mm A zz')
            with open(motd_path, "w") as f:
                f.write(f"🦴 This was fetched on {timestamp}\n")
                f.write("\n")
            with open(lusers_path, "w") as f:
                f.write(f"🦴 This was fetched on {timestamp}\n")
                f.write("\n")
            with open(map_path, "w") as f:
                f.write(f"🦴 This was fetched on {timestamp}\n")
                f.write("\n")
            with open(list_path, "w") as f:
                f.write(f"🦴 This was fetched on {timestamp}\n")
                f.write("\n")
            for line in receive_data(irc):
                print(line)

                if "372" in line:  # MOTD line
                    motd_line = line.split(":", 2)[2]
                    with open(motd_path, "a") as f:
                        f.write(motd_line + "\n")
                    motd_html_content += irc_to_html(motd_line) + "<br>"
                    motd_fetched = True

                if "251" in line or "252" in line or "253" in line or "254" in line or "255" in line or "265" in line or "266" in line:  # LUSERS info
                    lusers_line = line.split(nickname)[1]
                    if "Current" in lusers_line:
                        lusers_line = lusers_line.split(':')[1]
                    else:
                        lusers_line = lusers_line.split(':')
                        lusers_line = ''.join(lusers_line)
                        lusers_line = lusers_line.replace(" ", "", 1)
                    with open(lusers_path, "a") as f:
                        f.write(lusers_line + "\n")
                    lusers_html_content += irc_to_html(lusers_line) + "<br>"
                    lusers_fetched = True

                if "376" in line:  # End of MOTD command
                    break  # Exit the loop once all data is fetched

            # Fetch server map data
            send_command(irc, "MAP")
            map_html_content = ""
            for line in receive_data(irc):
                print(line)
                if "007" in line or "017" in line:  # End of /MAP (depends on the IRCd numeric)
                    map_fetched = True
                    break
                elif "015" in line or "016" in line:  # Map data lines
                    parts = line.split(":", 2)
                    if len(parts) > 2:
                        map_line = parts[2]
                        with open(map_path, "a") as f:
                            f.write(map_line + "\n")
                        map_html_content += irc_to_html(map_line) + "<br>"

            # Fetch channel list
            send_command(irc, "LIST *")
            for line in receive_data(irc):
                print(line)
                if "323" in line:  # End of /LIST
                    list_fetched = True
                    break
                elif "322" in line:  # LIST data line
                    parts = line.split(f"{nickname} ", 1)[1]
                    channel_info = parts.split(" ", 2)
                    channel = channel_info[0]
                    users = channel_info[1]
                    topic = channel_info[2].split(":", 1)[1] if ":" in channel_info[2] else ""

                    # Write to text file
                    with open(list_path, "a") as f:
                        f.write(f"{channel}\t{users}\t{topic}\n")

                    # Write to HTML file
                    list_html_content += f"<tr><td>{channel}</td><td>{users}</td><td>{irc_to_html(topic)}</td></tr>"


            # Create HTML files
            create_html_file(motd_html_path, motd_html_content, timestamp)
            create_html_file(lusers_html_path, lusers_html_content, timestamp)
            create_html_file(map_html_path, map_html_content, timestamp)
            create_html_file(list_html_path, list_html_content, timestamp)

            # Some IRCd's might force me to join so lets reset the channel
            channel = oldchan
            # Join the channel and announce results
            time.sleep(10)  # Wait 10 seconds before joining the channel
            send_command(irc, f"JOIN {channel}")

            time.sleep(5)  # Wait 5 seconds before sending messages
            if motd_fetched:
                send_command(irc, f"PRIVMSG {channel} :MOTD fetched successfully for {server}")
                print(f"MOTD fetched successfully for {server}")
            else:
                send_command(irc, f"PRIVMSG {channel} :MOTD was not fetched for {server}")
                print(f"MOTD was not fetched for {server}")

            if lusers_fetched:
                send_command(irc, f"PRIVMSG {channel} :LUSERS fetched successfully for {server}")
                print(f"LUSERS fetched successfully for {server}")
            else:
                send_command(irc, f"PRIVMSG {channel} :LUSERS was not fetched for {server}")
                print(f"LUSERS was not fetched for {server}")

            if map_fetched:
                send_command(irc, f"PRIVMSG {channel} :MAP fetched successfully for {server}")
                print(f"MAP fetched successfully for {server}")
            else:
                send_command(irc, f"PRIVMSG {channel} :MAP was not fetched for {server}")
                print(f"MAP was not fetched for {server}")

            if list_fetched:
                send_command(irc, f"PRIVMSG {channel} :LIST fetched successfully for {server}")
                print(f"LIST fetched successfully for {server}")
            else:
                send_command(irc, f"PRIVMSG {channel} :LIST was not fetched for {server}")
                print(f"LIST was not fetched for {server}")

            send_command(irc, f"PRIVMSG {channel} :Staying connected to {server} until next server hop")
            print(f"Staying connected to {server} for 1 hour")

            # Set mode +b
            send_command(irc, f"MODE {nickname} +b")
            send_command(irc, f"PRIVMSG {channel} :I have set myself +b")
            print(f"I have set myself +b")

            time.sleep(connection_duration)  # Stay connected for 1 hour

            new_server_index = (server_index + 1) % len(server_list)
            next_server = server_list[new_server_index]
            send_command(irc, f"QUIT :hop to {next_server}")
            irc.close()
            server_index = new_server_index

    except KeyboardInterrupt:
        # Gracefully quit IRC and close the socket on KeyboardInterrupt
        if irc:
            send_command(irc, "QUIT :Shutting down gracefully")
            send_command(irc, f"PRIVMSG {channel} :A cat stepped on my keyboard, bark bark!")
            irc.close()
        print("Gracefully shutting down")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=realname)
    parser.add_argument('--time', type=int, help='Duration to stay connected in seconds.')
    args = parser.parse_args()

    if not args.time:
        print("=================================================================")
        print_fido()
        print("=================================================================")
        parser.print_help()
        print("=================================================================")
        exit(1)

    if die == 1:
        print("=================================================================")
        print_fido()
        print("=================================================================")
        print("           EDIT THE PYTHON CODE, I WAS TOLD TO DIE!               ")
        print("=================================================================")
        exit(1)

    connection_duration = args.time
    main(connection_duration)
