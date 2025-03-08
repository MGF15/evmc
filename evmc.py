import requests
import sys

# Read opcodes from file
evm_opcodes = [line.strip() for line in open('op', 'r').readlines()]

# Check if user provided enough arguments
if len(sys.argv) < 2:
    print("Usage: python evmc.py <OPCODE_NAME> ['ALL'] [CUSTOM_RPC_URL]")
    sys.exit(1)

op_c = sys.argv[1].upper()  # Convert to uppercase for case-insensitive comparison
RPC_URL = sys.argv[2] if len(sys.argv) > 2 else "https://1rpc.io/matic"  # Default RPC if none provided

# If user wants all opcodes, print them
if op_c == "ALL" and len(sys.argv) < 2:
    print("Available EVM Opcodes:")
    for line in evm_opcodes:
        parts = line.split("\t")
        if len(parts) > 1:
            print(f"0x{parts[0]} - {parts[1].split()[0]}")
    sys.exit(0)

# Find the specific opcode
op = None if sys.argv[1].upper() != "ALL" else ""
for line in evm_opcodes:
    parts = line.split("\t")
    if len(parts) > 1 and op_c == parts[1].split()[0].upper():
        op = "0x" + parts[0]
        break

if op is None:
    print(f"❌ Opcode '{op_c}' not supported.")
    sys.exit(1)

# Function to send JSON-RPC requests
def rpc_request(method, params):
    headers = {"Content-Type": "application/json"}
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}

    try:
        response = requests.post(RPC_URL, headers=headers, json=payload, timeout=15)
        #print(response.text)
        if response.json().get("result") != None:
            #print(response.text)
            return response.json().get("result")
        else:
            #print(response.text)
            if len(response.json().get("error").get("message").split('invalid')) > 1: #hack 
                #print(response.json().get("error").get("message"))
                return "0"
            if len(response.json().get("error").get("message").split('stack')) > 1:
                return "0x"
            #else:
            #    return "0x"
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        
    except requests.exceptions.RequestException as e:
        print(f"🚨 RPC Error: {e}")
        sys.exit(1)

# Function to check for opcode
def check_opcode(opz,op_c):

    call_params = {
        "from": "0x0000000000000000000000000000000000000000",
        "to": None,
        "data": opz
    }
    
    response = rpc_request("eth_call", [call_params, "latest"])
    
    if response == "0x":
        print(f"✅ ({opz}) {op_c} opcode found.")
    else:
        print(f"❌ ({opz}) {op_c} No opcode found.")

# Run the opcode check
# check all

if sys.argv[1].upper() == "ALL":
    # Get Chain ID
    chain_id = rpc_request("eth_chainId", [])
    print(f"🔗 Chain ID: {int(chain_id,16)}")

    for lin in evm_opcodes:
        part = lin.split("\t")
        #print("0x" + part[0][0])
        if part[0][0] == "#":
            pass #optmiz we don't wan't to check all 148 opcodes
        else:
            check_opcode("0x" + part[0],part[1])
else:
    # Get Chain ID
    chain_id = rpc_request("eth_chainId", [])
    print(f"🔗 Chain ID: {int(chain_id,16)}")
    check_opcode(op,op_c)

#{'jsonrpc': '2.0', 'error': {'code': -32000, 'message': 'stack underflow (0 <=> 2)'}, 'id': 1}

#{'jsonrpc': '2.0', 'error': {'code': -32000, 'message': 'invalid opcode: PUSH0'}, 'id': 1}
