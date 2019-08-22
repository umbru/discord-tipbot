discord-tipbot
====

💸 An Umbru tip bot for Discord

## Usage

Command prefix : `!`

|Command                         |Description                                  |Example                                            |
|--------------------------------|---------------------------------------------|---------------------------------------------------|
|`!info`                         |Show Umbru network/blockchain info.          |                                                   |
|`!help`                         |Show help message.                           |                                                   |
|`!balance`                      |Show your balances.                          |                                                   |
|`!deposit`                      |Show your deposit address.                   |                                                   |
|`!tip (@user) (amount)`         |Tip specified amount to specified user.      |`!tip @ryxor 5`                                    |
|`!withdraw (address) (amount)`  |Withdraw amount to specified address.        |`!withdraw UWAiMq8mjiJLvtZ3phfdyefATPxDNZcLib 10`  |
|`!withdrawall (address)`        |Withdral all Umbru to specified address.     |`!withdrawall UWAiMq8mjiJLvtZ3phfdyefATPxDNZcLib`  |

## Requirement

* Python 3.5.3 or higher
* [discord.py](https://github.com/Rapptz/discord.py) (rewrite)
* [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc)

```
python3 -m pip install -U discord.py
```

```
python3 -m pip install python-bitcoinrpc
```

## How to run bot

1. Edit `config.py`

2. Edit configuration file of umbrud (umbru.conf)

```
daemon=1
server=1
rpcuser={same as config.py}
rpcpassword={same as config.py}
```

3. Run `tipbot.py`

```
python3 tipbot.py
```