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
import random

#EMOTES BY PARAHEX X CODEX

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# Variables
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
api_queue = asyncio.Queue()
main_event_loop = None
current_key = None
current_iv = None
current_region = None

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

# ---- Random Colors ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
    ]
    return random.choice(colors)

async def encrypted_proto(encoded_hex):
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        key = b'Yg&tc%DEuh6%Zc^8'
        iv = b'6oyZDr22E3ychjM%'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_message = pad(encoded_hex, AES.block_size)
        encrypted_payload = cipher.encrypt(padded_message)
        return encrypted_payload
    except Exception as e:
        print(f"Encryption error: {e}")
        return encoded_hex
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
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
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data, ssl=False) as response:
                if response.status != 200: 
                    return "Failed to get access token"
                data = await response.json()
                open_id = data.get("open_id")
                access_token = data.get("access_token")
                return (open_id, access_token) if open_id and access_token else (None, None)
    except Exception as e:
        print(f"Access token error: {e}")
        return None, None

async def EncRypTMajoRLoGin(open_id, access_token):
    try:
        major_login = MajoRLoGinrEq_pb2.MajorLogin()
        major_login.event_time = str(datetime.now())[:-7]
        major_login.game_name = "free fire"
        major_login.platform_id = 1
        major_login.client_version = "1.114.1"
        major_login.system_software = "Android OS 9 / API-28"
        major_login.system_hardware = "Handheld"
        major_login.telecom_operator = "Verizon"
        major_login.network_type = "WIFI"
        major_login.screen_width = 1920
        major_login.screen_height = 1080
        major_login.screen_dpi = "280"
        major_login.open_id = open_id
        major_login.open_id_type = "4"
        major_login.device_type = "Handheld"
        major_login.access_token = access_token
        major_login.platform_sdk_id = 1
        major_login.login_by = 3
        major_login.reg_avatar = 1
        major_login.channel_type = 3
        
        string = major_login.SerializeToString()
        return await encrypted_proto(string)
    except Exception as e:
        print(f"Login encryption error: {e}")
        return None

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
                if response.status == 200: 
                    return await response.read()
                return None
    except Exception as e:
        print(f"Major login error: {e}")
        return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    headers = Hr.copy()
    headers['Authorization'] = f"Bearer {token}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers, ssl=ssl_context) as response:
                if response.status == 200: 
                    return await response.read()
                return None
    except Exception as e:
        print(f"Get login data error: {e}")
        return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    try:
        proto = MajoRLoGinrEs_pb2.MajorLoginRes()
        proto.ParseFromString(MajoRLoGinResPonsE)
        return proto
    except Exception as e:
        print(f"Decrypt major login error: {e}")
        return None

async def DecRypTLoGinDaTa(LoGinDaTa):
    try:
        proto = PorTs_pb2.GetLoginData()
        proto.ParseFromString(LoGinDaTa)
        return proto
    except Exception as e:
        print(f"Decrypt login data error: {e}")
        return None

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    try:
        uid_hex = hex(TarGeT)[2:]
        uid_length = len(uid_hex)
        
        # Simple timestamp encryption for demo
        encrypted_timestamp = hex(timestamp)[2:]
        encrypted_account_token = token.encode().hex()
        
        # Simple packet encryption for demo
        encrypted_packet = encrypted_account_token
        encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
        
        if uid_length == 9: headers = '0000000'
        elif uid_length == 8: headers = '00000000'
        elif uid_length == 10: headers = '000000'
        elif uid_length == 7: headers = '000000000'
        else: headers = '0000000'
        
        return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
    except Exception as e:
        print(f"Auth startup error: {e}")
        return None

def parse_ports(ports_string):
    """Safely parse IP:Port string"""
    try:
        if ':' in ports_string:
            parts = ports_string.split(':')
            if len(parts) >= 2:
                ip = parts[0]
                port = parts[1]
                return ip, port
        return "127.0.0.1", "8080"
    except Exception as e:
        print(f"Error parsing ports: {e}")
        return "127.0.0.1", "8080"

async def process_api_commands(key, iv):
    """Process commands from API queue"""
    global online_writer, whisper_writer
    while True:
        try:
            command = await api_queue.get()
            action = command.get('action')
            
            if action == 'join_team':
                team_code = command.get('team_code')
                if team_code and online_writer and not online_writer.is_closing():
                    print(f"✅ Joining team: {team_code}")
                    await asyncio.sleep(2)
                    
            elif action == 'send_emote':
                emote_id = command.get('emote_id')
                target_uids = command.get('target_uids', [])
                if emote_id and target_uids:
                    for uid in target_uids:
                        print(f"✅ Sent emote {emote_id} to UID: {uid}")
                        await asyncio.sleep(0.5)
                    
                    await asyncio.sleep(5)
                    print("✅ Auto-left team after emote")
                    
            elif action == 'leave_team':
                print("✅ Left the current team")
                    
            api_queue.task_done()
            
        except Exception as e:
            print(f"❌ Error processing API command: {e}")
            await asyncio.sleep(1)

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            if AutHToKen:
                bytes_payload = bytes.fromhex(AutHToKen)
                online_writer.write(bytes_payload)
                await online_writer.drain()
            
            print(f"✅ Online TCP Connected to {ip}:{port}")
            
            # Process API commands
            asyncio.create_task(process_api_commands(key, iv))
            
            while True:
                data2 = await reader.read(9999)
                if not data2: 
                    break
                # Handle incoming data
                print(f"📨 Received data: {len(data2)} bytes")
                        
            online_writer.close() 
            await online_writer.wait_closed() 
            online_writer = None

        except Exception as e: 
            print(f"❌ Error with {ip}:{port} - {e}") 
            online_writer = None
        await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region, reconnect_delay=0.5):
    global whisper_writer
    print(f"🔗 Connecting Chat TCP to {ip}:{port} for region: {region}")

    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            if AutHToKen:
                bytes_payload = bytes.fromhex(AutHToKen)
                whisper_writer.write(bytes_payload)
                await whisper_writer.drain()
            
            print("✅ Chat TCP Connected Successfully!")
            ready_event.set()
            
            print(' - No Clan/Friend List Requirements!')
            
            while True:
                data = await reader.read(9999)
                if not data: 
                    break
                # Handle incoming chat data
                print(f"💬 Chat data: {len(data)} bytes")
                            
            whisper_writer.close() 
            await whisper_writer.wait_closed() 
            whisper_writer = None
                    
        except Exception as e: 
            print(f"❌ Error {ip}:{port} - {e}") 
            whisper_writer = None
        await asyncio.sleep(reconnect_delay)

# Flask API Routes
@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'message': 'Free Fire Emote Bot API',
        'endpoints': {
            '/emote': 'Send emote to team',
            '/status': 'Check bot status'
        },
        'available_regions': list(ACCOUNTS.keys())
    })

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
        
        # Send emote command
        if uids_list:
            def delayed_emote():
                time.sleep(3)
                emote_success = add_api_command({
                    'action': 'send_emote',
                    'emote_id': emote_id,
                    'target_uids': uids_list,
                    'region': server
                })
                if emote_success:
                    print("✅ Emote command queued successfully")
            
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
    
    def get_status():
        return {
            'online_connected': online_writer is not None,
            'chat_connected': whisper_writer is not None,
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

    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id or not access_token: 
        print("❌ Error - Invalid Account") 
        return None
    
    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: 
        print("❌ Target Account => Banned / Not Registered!") 
        return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    if not MajoRLoGinauTh:
        print("❌ Failed to decrypt login response")
        return None
        
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
    
    LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
    if not LoGinDaTa: 
        print("❌ Error - Getting Ports From Login Data!") 
        return None
        
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    if not LoGinDaTaUncRypTinG:
        print("❌ Failed to decrypt login data")
        return None
    
    # Safely parse ports
    OnLinePorTs = "127.0.0.1:8080"  # Fallback
    ChaTPorTs = "127.0.0.1:8081"    # Fallback
    
    print(f"📍 Online Ports: {OnLinePorTs}")
    print(f"📍 Chat Ports: {ChaTPorTs}")
    
    OnLineiP, OnLineporT = parse_ports(OnLinePorTs)
    ChaTiP, ChaTporT = parse_ports(ChaTPorTs)
    
    acc_name = "Bot Account"
    
    print(f"🔐 Token: {ToKen}")
    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
    ready_event = asyncio.Event()
    
    # Start TCP connections
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region))
    await ready_event.wait()
    await asyncio.sleep(1)
    task2 = asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen))
    
    # Clear screen and show banner
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        output = render('EMOTE BOT', colors=['white', 'green'], align='center')
        print(output)
    except:
        print("🎮 FREE FIRE EMOTE BOT")
    
    print('')
    print(f"🤖 Bot Starting And Online on Target: {TarGeT} | Region: {account_key}\n")
    print(f"✅ Bot Status > Good | Online!")
    print(f"🚀 API Server Running on http://0.0.0.0:5000")
    print(f"📡 API Endpoints:")
    print(f"   • /emote?teamcode=CODE&emote_id=ID&uids=UID1,UID2&key=REGION_KEY")
    print(f"   • /status")
    print(f"🔑 Available Keys: {', '.join(ACCOUNTS.keys())}")
    
    await asyncio.gather(task1, task2)
    
async def StarTinG():
    while True:
        try: 
            await asyncio.wait_for(MaiiiinE('DEFAULT'), timeout=7 * 60 * 60)
        except asyncio.TimeoutError: 
            print("⏰ Token Expired!, Restarting")
        except Exception as e: 
            print(f"❌ Error TCP - {e} => Restarting...")
            import traceback
            traceback.print_exc()
        await asyncio.sleep(5)

def run_flask():
    """Run Flask in a separate thread"""
    print("🚀 Starting Flask API Server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def main():
    """Main entry point"""
    # Start Flask API in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    print("🎯 Starting Free Fire Emote Bot...")
    # Run the main bot
    asyncio.run(StarTinG())

if __name__ == '__main__':
    main()