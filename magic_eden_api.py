import requests

class MagicEdenAPI:
    def __init__(self, session):
        self.session = session

    async def get_magic_nfts(self, address):
        magic_endpoint = f"https://api-mainnet.magiceden.dev/v2/wallets/{address}/tokens"
        async with self.session.get(magic_endpoint) as resp:
            if resp.status == 200:
                tokens = await resp.json()
                if isinstance(tokens, list) and tokens:
                    magic_nfts = [token.get('token') for token in tokens]
                    print(f"Magic Eden NFT(s) found for account {address}.")
                    return magic_nfts
                elif isinstance(tokens, dict) and tokens.get('token'):
                    magic_nfts = [tokens.get('token')]
                    print(f"Magic Eden NFT found for account {address}.")
                    return magic_nfts
        return None
