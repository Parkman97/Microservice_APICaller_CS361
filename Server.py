import requests
import json
from urllib.parse import quote
import socket
from Data_Parser import dataParser

while True:
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            try: 
                data = conn.recv(10240)
                data = data.decode('utf-8')
                data = data.split(',')
                
                if data[0] == 'Article':
                    link = "https://api.spaceflightnewsapi.net/v4/articles/?"
                else:
                    link = "https://api.spaceflightnewsapi.net/v4/blogs/?"
                
                
                order = [1, 4, 3, 2]

                for x in order:
                    if data[x] != '':
                        if x == 1:
                            link += ('has_launch=' + data[x]) #1 

                        if x == 2:
                            if 'has_launch' not in link:
                                link += ('news_site=' + data[x])
                                
                            else:
                                link += ('&news_site=' + data[x])
                        
                        if x == 3: #3
                            if 'news_site' not in link and 'has_launch' not in link:
                                link += ('published_at_gte=' + data[x])
                        
                            else:
                                link += ('&published_at_gte=' + data[x])

                        if x == 4:
                            if int(data[x]) > 10 or "":  #2
                                data[x] = 10
                            if 'limit' not in link and 'has_launch' not in link and 'published_at_gte' not in link:
                                link += ('limit=' + data[x])
                            
                            else:
                                    link += ('&limit=' + data[x])
                    else:
                        execute_code = False
                
                link = link.replace(" ", "")
                response = requests.get(link)

                if response.status_code == 200:
                    data = response.json()
                    dict_value = dataParser(data)
                    user_encode_data = json.dumps(dict_value).encode('utf-8')
                else:
                    print(f"Error failed to get data: {response.status_code}")
                    user_encode_data = b''  # Empty bytes
                    
                if user_encode_data == b'[]':
                    conn.sendall(b'Link Not Found')
                else:
                    conn.sendall(user_encode_data)
                    

            except IndexError as error:
                print('\nSection: Function to Create Instances of WebDriver\nCulprit: random.choice(ua_strings)\nIndexError: {}\n'.format(error))
                break
            except ConnectionResetError:
                print("Connection reset by peer")
                break
            except Exception as e:
                print(f"Error: {e}")
                break


    