from helper import hash160

bit_field_size = 10
bit_field = [0] * bit_field_size
for item in (b'hello world', b'goodbye'):
    h = hash160(item)
    bit = int.from_bytes(h, 'big') % bit_field_size
    bit_field[bit] = 1
print(bit_field)

exit()

from merkleblock import MerkleTree
from helper import merkle_parent

hex_hashes = [
    "9745f7173ef14ee4155722d1cbf13304339fd00d900b759c6f9d58579b5765fb",
    "5573c8ede34936c29cdfdfe743f7f5fdfbd4f54ba0705259e62f39917065cb9b",
    "82a02ecbb6623b4274dfcab82b336dc017a27136e08521091e443e62582e8f05",
    "507ccae5ed9b340363a0e6d765af148be9cb1c8766ccc922f83e4ae681658308",
    "a7a4aec28e7162e1e9ef33dfa30f0bc0526e6cf4b11a576f6c5de58593898330",
    "bb6267664bd833fd9fc82582853ab144fece26b7a8a5bf328f8a059445b59add",
    "ea6d7ac1ee77fbacee58fc717b990c4fcccf1b19af43103c090f601677fd8836",
    "457743861de496c429912558a106b810b0507975a49773228aa788df40730d41",
    "7688029288efc9e9a0011c960a6ed9e5466581abf3e3a6c26ee317461add619a",
    "b1ae7f15836cb2286cdd4e2c37bf9bb7da0a2846d06867a429f654b2e7f383c9",
    "9b74f89fa3f93e71ff2c241f32945d877281a6a50a6bf94adac002980aafe5ab",
    "b3a92b5b255019bdaf754875633c2de9fec2ab03e6b8ce669d07cb5b18804638",
    "b5c0b915312b9bdaedd2b86aa2d0f8feffc73a2d37668fd9010179261e25e263",
    "c9d52c5cb1e557b92c84c52e7c4bfbce859408bedffc8a5560fd6e35e10b8800",
    "c555bc5fc3bc096df0a0c9532f07640bfb76bfe4fc1ace214b8b228a1297a4c2",
    "f9dbfafc3af3400954975da24eb325e326960a25b87fffe23eef3e7ed2fb610e",
]

tree = MerkleTree(len(hex_hashes))
tree.nodes[4] = [bytes.fromhex(h) for h in hex_hashes]
while tree.root() is None:
    if tree.is_leaf():
        tree.up()
    else:
        left_hash = tree.get_left_node()
        right_hash = tree.get_right_node()
        if left_hash is None:
            tree.left()
        elif right_hash is None:
            tree.right()
        else:
            tree.set_current_node(merkle_parent(left_hash, right_hash))
            tree.up()
print(tree)

exit()

from io import BytesIO
from network import SimpleNode, GetHeadersMessage, HeadersMessage
from block import Block, GENESIS_BLOCK, LOWEST_BITS
from helper import calculate_new_bits
previous = Block.parse(BytesIO(GENESIS_BLOCK))
first_epoch_timestamp = previous.timestamp
expected_bits = LOWEST_BITS
count = 1
node = SimpleNode('mainnet.programmingbitcoin.com', testnet=False)
node.handshake()
for _ in range(25):
    getheaders = GetHeadersMessage(start_block=previous.hash())
    node.send(getheaders)
    headers = node.wait_for(HeadersMessage)
    for header in headers.blocks:
        if not header.check_pow():
            raise RuntimeError('bad PoW at block {}'.format(count))
        if header.prev_block != previous.hash():
            raise RuntimeError('discontinuous block at {}'.format(count))
        if count % 2016 == 0:
            time_diff = previous.timestamp - first_epoch_timestamp
            expected_bits = calculate_new_bits(previous.bits, time_diff)
            print(expected_bits.hex())
            first_epoch_timestamp = header.timestamp
        if header.bits != expected_bits:
            raise RuntimeError('bad bits at block {}'.format(count))
        previous = header
        count += 1
