import socket
import webbrowser
import datetime
import os


stat200 = """\r\nHTTP /1.1 200 OK\r\nCache-Control: private ; max-age=0\r\nConten-Type: text/html;charset="utf-8"\r\nX_Frame_Options: DENY"""
stat302 = """\r\nHTTP/1.1 302 Redirect\r\nLocation: """
stat404 = """\r\nHTTP /1.1 404 Not Found\r\n"""
img = """HTTP/1.1 200 OK\r\nContent-Type: image/png\r\nContent-Length:"""
img_response1 = f'HTTP/1.1 200 OK\r\nServer: nginx\r\nDate: Sat, 17 Feb 2025 15:58:58 GMT\r\nContent-Length: '
img_response2 = f'\r\nConnection: keep-alive\r\nLast-Modified: Wed, 01 Aug 2018 19:03:40 GMT\r\nAccept-Ranges: bytes\r\n\r\n'
# -------------
ip = "127.0.0.1"
port = 15936

surah_ayat_count = {
    1: 7,2: 286,3: 200,4: 176,5: 120,6: 165,7: 206,8: 75,9: 129,10: 109,11: 123,12: 111,13: 43,14: 52,15: 99,16: 128,17: 111,18: 110,
    19: 98,20: 135,21: 112,22: 78,23: 118,24: 64,25: 77,26: 227,27: 93,28: 88,29: 69,30: 60,31: 34,32: 30,33: 73,34: 54,35: 45,36: 83,
    37: 182,38: 88,39: 75,40: 85,41: 54,42: 53,43: 89,44: 59,45: 37,46: 35,47: 38,48: 29,49: 18,50: 45,51: 60,52: 49,53: 62,54: 55,
    55: 78,56: 96,57: 29,58: 22,59: 24,60: 13,61: 14,62: 11,63: 11,64: 18,65: 12,66: 12,67: 30,68: 52,69: 52,70: 44,71: 28,72: 28,73: 20,
    74: 56,75: 40,76: 31,77: 50,78: 40,79: 46,80: 42,81: 29,82: 19,83: 36,84: 25,85: 22,86: 17,87: 19,88: 26,89: 30,90: 20,91: 15,
    92: 21,93: 11,94: 8,95: 8,96: 19,97: 5,98: 8,99: 8,100: 11,101: 11,102: 8,103: 3,104: 9,105: 5,106: 4,107: 7,108: 3,109: 6,110: 3,
    111: 5,112: 4,113: 5,114: 6
}


Tafser_Path = r'tafser'

def get_tafser(sura , aya):
    global init_prev_aya , init_next_aya
    prev_aya = init_prev_aya = '<h2><strong>------ { نَبدَأٌ علَى بَرَكةِ اللّ\u0670ه } ------</strong></h2>'
    curr_aya = ''
    next_aya = init_next_aya = '<h2><strong>------ { تَمَّ بِحمدِ اللّ\u0670ه } ------</strong></h2>'
    tafaser = {
    'katheer' : '',
    'saadi' : '',
    'qortobi' : '',
    'tabary' : '',
    'baghawy' : '',
    }
    
    for name in tafaser.keys() :
    
        try:
            with open(Tafser_Path+rf'\{name}\sura{(sura if aya-1>0 else sura-1)}\aya{aya-1 if aya-1>0 else surah_ayat_count[sura-1]}.txt' , 'rb') as file :
                content = file.read().decode().split("\n||\n")
                prev_aya = (content[0] if content[0] !='' else prev_aya)
        except IndexError:pass
        except FileNotFoundError:pass
        except KeyError :pass
        
        try:
            with open(Tafser_Path+rf'\{name}\sura{(sura+1 if aya+1>surah_ayat_count[sura] else sura)}\aya{1 if aya+1>surah_ayat_count[sura] else aya+1}.txt' , 'rb') as file :
                content = file.read().decode().split("\n||\n")
                next_aya = (content[0] if content[0] !='' else next_aya)
        except FileNotFoundError:pass
        except IndexError:pass
        except KeyError:pass

        try :
            with open(Tafser_Path+rf'\{name}\sura{sura}\aya{aya}.txt' , 'rb') as file :
                content = file.read().decode().replace('"' , "'").split("\n||\n")
                curr_aya = (content[0] if content[0] !='' else curr_aya)
                tafaser[name] = content[1]
        except Exception as e :
            with open("Error_log.txt" , 'a') as log_file :log_file.write(f'[-] {e}\n\n')
          
    return tafaser , prev_aya , curr_aya , next_aya 


def prepare_html_file(tafaser , prev_aya , curr_aya , next_aya , sura , aya):
    with open(r'html\index.html' , 'rb') as file :
        content = file.read().decode()
        place_holder = ['TAFSER_IBN_KATHEER'  , 'TAFSER_AL_SAADI'  , 'TAFSER_AL_KURTUBI' , 'TAFSER_AL_TABARI' , 'TAFSER_AL_BAGAWI']
        for index , tafser in enumerate(tafaser.values()):
            content = content.replace(place_holder[index] , tafser)
        
        content = content.replace('PREV_AYA' , prev_aya)
        content = content.replace('CURRENT_AYA' , curr_aya)
        content = content.replace('NEXT_AYA' , next_aya)

        content = content.replace('SURA_NUMBER' , str(sura))
        content = content.replace('AYA_NUMBER' , str(aya))

        content = content.replace('SERVER_PORT' , str(port))
        content = content.replace('SERVER_IP' , str(ip))
        
        content = content.replace('NEXT_LINK_AYA' , ('' if next_aya==init_next_aya else (f'http://{ip}:{port}/sura{sura}-aya{aya+1}' if aya+1<=surah_ayat_count[sura] else f'http://{ip}:{port}/sura{sura+1}-aya{1}') ))
        content = content.replace('PREV_LINK_AYA' , ('' if prev_aya==init_prev_aya else (f'http://{ip}:{port}/sura{sura}-aya{aya-1}' if aya-1>0 else f'http://{ip}:{port}/sura{sura-1}-aya{surah_ayat_count[sura-1]}') ))

    return content


def get_favicon():
    with open('favicon.ico' , 'rb') as file :
        return file.read()

def get_default():
    try:
        with open('last.txt','r') as file :
            return file.read()
    except FileNotFoundError :
        return 'sura1-aya1'

def handle_request(request):
    path = request.split()[1]
    default = get_default()
    
    if path == '/styles.css' :return stat404
    if '-' not in path :
        return stat302+f'http://{ip}:{port}/{default}'
    
    sura_part , aya_part = path[1:].split('-')
    sura_number = int(sura_part[4:])
    aya_number = int(aya_part[3:])

    if sura_part[:4] != 'sura' or len(sura_part)<5  or aya_part[:3] != 'aya' or len(aya_part)<4:
        return stat302+f'http://{ip}:{port}/{default}'
    
    if sura_number>114 or sura_number<1 or aya_number<1 or aya_number>surah_ayat_count[sura_number]:
        return stat302+f'http://{ip}:{port}/{default}'
    
    tafaser , prev_aya , curr_aya , next_aya = get_tafser(sura_number , aya_number)
    response = prepare_html_file(tafaser , prev_aya , curr_aya , next_aya, sura_number , aya_number)
    with open("last.txt" , 'w') as file : file.write(f'sura{sura_number}-aya{aya_number}')
    return stat200+f"\r\n\r\n{response}"




def start_server(host , port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.bind((host, port))
            server_socket.listen(1)
        except Exception as e:
            with open("Error_log.txt" , 'a') as log_file :log_file.write(f'[-] {e}\n')
            exit()
        with open('pid.txt' , 'w') as file :file.write(str(os.getpid()))

        webbrowser.open("http://"+host+f":{port}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                request = client_socket.recv(1024).decode('utf-8')
                # print(request[:20])

                if request.split()[1] =='/favicon.ico' :
                    favicon = get_favicon()
                    client_socket.sendall((img_response1+str(len(favicon))+img_response2).encode())
                    client_socket.sendall(favicon)
                    continue
                
                response = handle_request(request)
                client_socket.sendall(response.encode('utf-8'))
            if False :
                with open("log.txt" , 'a') as log_file :log_file.write(f'[+] {datetime.datetime.now()} | {client_address} | {request.split()[:2]} | '+ response.split("\r\n")[1]+'\n' )


if __name__ == "__main__":
    start_server(ip , port)
