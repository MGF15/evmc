# EVM Opcode Checker

This script allows users to check if a specific Ethereum Virtual Machine (EVM) opcode exists by sending an eth_call request to an Ethereum-compatible RPC node. Additionally, users can list all supported EVM opcodes.

# Features

1-Check if a specific opcode exists on the EVM.

2-List all available opcodes.

3-Support for custom RPC URLs.

4-Default RPC URL: https://1rpc.io/matic (Polygon Mainnet).

# Install dependencies:

> pip install requests

Usage

1. Check for a Specific Opcode

To check if an opcode exists, run:

> python evmc.py <OPCODE_NAME>

Example:

> python evmc.py STOP

Output:
```sh
🔗 Chain ID: 0x89
✅ (0x00) STOP opcode found.
```
2. Check with a Custom RPC URL

If you want to use a different RPC URL (e.g., Infura, Alchemy), provide it as the second argument:

> python evmc.py <OPCODE_NAME> <RPC_URL>

Example:

> python evmc.py STOP https://mainnet.infura.io/v3/YOUR_INFURA_KEY

3. List All Opcodes

To print all available EVM opcodes, run:

> python evmc.py ALL
