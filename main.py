import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say
from flask import Flask, request, jsonify
import asyncio

#EMOTES BY PARAHEX X CODEX

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# VariabLes dyli 
#------------------------------------------#
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
api_queue = asyncio.Queue()
main_event_loop = None  # Initialize globally
#------------------------------------------#

# Account configurations for different regions
ACCOUNTS = {
    'IND': {'uid': '4253797706', 'password': 'BY_GRIZLY-MAAHCDX54-GRIZLY'},
    'PK': {'uid': '4253802886', 'password': 'BY_GRIZLY-FQPGUDHXY-GRIZLY'},
    'BR': {'uid': '4253808271', 'password': 'BY_GRIZLY-TEV1ML6A4-GRIZLY'},
    'BD': {'uid': '4253807582', 'password': 'BY_GRIZLY-YDDBLLUUJ-GRIZLY'},
    'ID': {'uid': '4253811980', 'password': 'BY_GRIZLY-GOX0Y2XNZ-GRIZLY'},
    'SG': {'uid': '4219103781', 'password': 'BY_GRIZLY-PRM93ZSHQ-GRIZLY'},
    'YE': {'uid': '4219103782', 'password': 'BY_GRIZLY-PRM93ZSHQ-GRIZLY'}
}

# Default account
DEFAULT_ACCOUNT = {'uid': '4219103776', 'password': 'BY_GRIZLY-PRM93ZSHQ-GRIZLY'}

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB50"}

# Flask app for API
app = Flask(__name__)

def add_api_command(command):
    """Safely add command to API queue from any thread"""
    global main_event_loop
    if main_event_loop and main_event_loop.is_running():
        asyncio.run_coroutine_threadsafe(api_queue.put(command), main_event_loop)
        return True
    else:
        print("Warning: Main event loop not available, command not queued")
        return False

# ---- Random Colores ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.114.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0OUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: 
        if whisper_writer and not whisper_writer.is_closing():
            whisper_writer.write(PacKeT) 
            await whisper_writer.drain()
    elif TypE == 'OnLine': 
        if online_writer and not online_writer.is_closing():
            online_writer.write(PacKeT) 
            await online_writer.drain()
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)' 

def parse_ports(ports_string):
    """Safely parse IP:Port string"""
    try:
        if ':' in ports_string:
            parts = ports_string.split(':')
            if len(parts) >= 2:
                ip = parts[0]
                port = parts[1]
                return ip, port
        # Fallback if format is unexpected
        return "127.0.0.1", "8080"
    except Exception as e:
        print(f"Error parsing ports: {e}")
        return "127.0.0.1", "8080"
           
async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer , spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , XX , uid , Spy,data2, Chat_Leave, main_event_loop
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            
            print(f"✅ Online TCP Connected to {ip}:{port}")
            
            # Process API commands from queue
            asyncio.create_task(process_api_commands(key, iv))
            
            while True:
                data2 = await reader.read(9999)
                if not data2: break
                
                if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                    try:
                        print(data2.hex()[10:])
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        print(packet)
                        packet = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)

                        message = f'[B][C]{get_random_color()}\n- WeLComE To Emote Bot ! '
                        P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)

                    except:
                        pass

            online_writer.close() 
            await online_writer.wait_closed() 
            online_writer = None

        except Exception as e: 
            print(f"❌ ErroR With {ip}:{port} - {e}") 
            online_writer = None
        await asyncio.sleep(reconnect_delay)

async def process_api_commands(key, iv):
    """Process commands from API queue"""
    global online_writer, whisper_writer
    while True:
        try:
            command = await api_queue.get()
            action = command.get('action')
            
            if action == 'join_team':
                team_code = command.get('team_code')
                region = command.get('region', '')
                
                if team_code and online_writer and not online_writer.is_closing():
                    # Join the team
                    join_packet = await GenJoinSquadsPacket(team_code, key, iv)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                    await asyncio.sleep(2)
                    
                    print(f"✅ Successfully joined team: {team_code}")
                    
            elif action == 'send_emote':
                emote_id = command.get('emote_id')
                target_uids = command.get('target_uids', [])
                region = command.get('region', '')
                
                if emote_id and target_uids and online_writer and not online_writer.is_closing():
                    for uid in target_uids:
                        try:
                            emote_packet = await Emote_k(int(uid), int(emote_id), key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
                            await asyncio.sleep(0.5)
                            print(f"✅ Sent emote {emote_id} to UID: {uid}")
                        except Exception as e:
                            print(f"❌ Error sending emote to {uid}: {e}")
                    
                    # Auto leave after 5 seconds
                    print("⏳ Waiting 5 seconds before auto-leaving...")
                    await asyncio.sleep(5)
                    if online_writer and not online_writer.is_closing():
                        leave_packet = await ExiT(None, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
                        print("✅ Auto-left team after emote")
                    
            elif action == 'leave_team':
                if online_writer and not online_writer.is_closing():
                    leave_packet = await ExiT(None, key, iv)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
                    print("✅ Left the current team")
                    
            api_queue.task_done()
            
        except Exception as e:
            print(f"❌ Error processing API command: {e}")
            await asyncio.sleep(1)
                            
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave, main_event_loop
    
    print(f"🔗 Connecting Chat TCP to {ip}:{port} for region: {region}")

    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            
            print("✅ Chat TCP Connected Successfully!")
            ready_event.set()
            
            # Remove clan authentication requirement
            print(' - No Clan/Friend List Requirements!')
            
            while True:
                data = await reader.read(9999)
                if not data: break
                
                # You can keep the chat message handling if needed
                if data.hex().startswith("120000"):
                    try:
                        msg = await DeCode_PackEt(data.hex()[10:])
                        chatdata = json.loads(msg)
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        if response:
                            uid = response.Data.uid
                            chat_id = response.Data.Chat_ID
                            XX = response.Data.chat_type
                            inPuTMsG = response.Data.msg.lower()
                            
                            # Keep basic chat functionality
                            if inPuTMsG in ("hi" , "hello" , "fen" , "salam"):
                                message = 'Hello Im API Controlled Bot\nUse Web API to control me!'
                                P = await SEndMsG(response.Data.chat_type , message , uid , chat_id , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                    except:
                        pass
                            
            whisper_writer.close() 
            await whisper_writer.wait_closed() 
            whisper_writer = None
                    
        except Exception as e: 
            print(f"❌ ErroR {ip}:{port} - {e}") 
            whisper_writer = None
        await asyncio.sleep(reconnect_delay)

# Flask API Routes
@app.route('/emote', methods=['GET'])
def handle_emote():
    """Handle emote commands via API"""
    try:
        team_code = request.args.get('teamcode')
        emote_id = request.args.get('emote_id')
        server = request.args.get('server', '')
        target_uids = request.args.get('uids', '')
        key = request.args.get('key', 'DEFAULT')
        
        if not team_code or not emote_id:
            return jsonify({'status': 'error', 'message': 'Missing teamcode or emote_id'}), 400
        
        # Get account based on key
        account = ACCOUNTS.get(key.upper(), DEFAULT_ACCOUNT)
        
        # Parse target UIDs
        uids_list = []
        if target_uids:
            uids_list = [uid.strip() for uid in target_uids.split(',') if uid.strip()]
        
        # Add commands to queue
        commands_added = []
        
        # Join team command
        join_success = add_api_command({
            'action': 'join_team',
            'team_code': team_code,
            'region': server
        })
        if join_success:
            commands_added.append('join_team')
        
        # Wait a bit then send emote
        if uids_list:
            # Add delay before sending emote
            def delayed_emote():
                time.sleep(3)  # Wait 3 seconds for join to complete
                emote_success = add_api_command({
                    'action': 'send_emote',
                    'emote_id': emote_id,
                    'target_uids': uids_list,
                    'region': server
                })
                if emote_success:
                    print("✅ Emote command queued successfully")
            
            # Start delayed emote in background
            threading.Thread(target=delayed_emote, daemon=True).start()
        
        return jsonify({
            'status': 'success', 
            'message': f'Command queued: Join {team_code}, send emote {emote_id}, and auto-leave after 5 seconds',
            'targets': uids_list,
            'account_used': key.upper() if key.upper() in ACCOUNTS else 'DEFAULT',
            'commands_queued': commands_added
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/status', methods=['GET'])
def handle_status():
    """Check bot status"""
    global online_writer, whisper_writer, main_event_loop
    
    # Use thread-safe way to check status
    def get_status():
        return {
            'online_connected': online_writer is not None and not online_writer.is_closing(),
            'chat_connected': whisper_writer is not None and not whisper_writer.is_closing(),
            'queue_size': api_queue.qsize() if api_queue else 0,
            'available_keys': list(ACCOUNTS.keys()),
            'event_loop_available': main_event_loop is not None and main_event_loop.is_running()
        }
    
    status_data = get_status()
    return jsonify({'status': 'success', 'data': status_data}), 200

async def MaiiiinE(account_key='DEFAULT'):
    global main_event_loop, current_key, current_iv, current_region
    
    # Set main event loop
    main_event_loop = asyncio.get_event_loop()
    
    # Get account credentials based on key
    account = ACCOUNTS.get(account_key, DEFAULT_ACCOUNT)
    Uid, Pw = account['uid'], account['password']
    
    print(f"🔑 Using account for region: {account_key} | UID: {Uid}")

    open_id , access_token = await GeNeRaTeAccEss(Uid , Pw)
    if not open_id or not access_token: 
        print("❌ ErroR - InvaLid AccounT") 
        return None
    
    PyL = await EncRypTMajoRLoGin(open_id , access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: 
        print("❌ TarGeT AccounT => BannEd / NoT ReGisTeReD ! ") 
        return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    print(f"🌐 Login URL: {UrL}")
    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    # Store current session info
    current_key = key
    current_iv = iv
    current_region = region
    
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: 
        print("❌ ErroR - GeTinG PorTs From LoGin DaTa !") 
        return None
        
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    
    # Safely parse ports
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    
    print(f"📍 Online Ports: {OnLinePorTs}")
    print(f"📍 Chat Ports: {ChaTPorTs}")
    
    OnLineiP , OnLineporT = parse_ports(OnLinePorTs)
    ChaTiP , ChaTporT = parse_ports(ChaTPorTs)
    
    acc_name = LoGinDaTaUncRypTinG.AccountName
    
    print(f"🔐 Token: {ToKen}")
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region))
     
    await ready_event.wait()
    await asyncio.sleep(1)
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))
    
    os.system('clear')
    print(render('REDZED', colors=['white', 'green'], align='center'))
    print('')
    print(f"🤖 BoT STarTinG And OnLine on TarGet : {TarGeT} | BOT NAME : {acc_name}\n")
    print(f"🌍 Region Key: {account_key}")
    print(f"✅ BoT sTaTus > GooD | OnLinE !")
    print(f"🚀 API Server Running on http://localhost:5000")
    print(f"📡 API Endpoints:")
    print(f"   • /emote?teamcode=CODE&emote_id=ID&uids=UID1,UID2&key=REGION_KEY")
    print(f"   • /status")
    print(f"🔑 Available Keys: {', '.join(ACCOUNTS.keys())}")
    print(f"🔄 Event Loop: {'✅ Running' if main_event_loop and main_event_loop.is_running() else '❌ Not Running'}")
    
    await asyncio.gather(task1 , task2)
    
async def StarTinG():
    while True:
        try: 
            await asyncio.wait_for(MaiiiinE('DEFAULT'), timeout=7 * 60 * 60)
        except asyncio.TimeoutError: 
            print("⏰ Token ExpiRed ! , ResTartinG")
        except Exception as e: 
            print(f"❌ ErroR TcP - {e} => ResTarTinG ...")
            import traceback
            traceback.print_exc()
        await asyncio.sleep(5)  # Wait before restarting

def run_flask():
    """Run Flask in a separate thread"""
    print("🚀 Starting Flask API Server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Start Flask API in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    print("🎯 Starting Free Fire Emote Bot...")
    # Run the main bot
    asyncio.run(StarTinG())
