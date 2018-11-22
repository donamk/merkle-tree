import copy

from utils import *
import math
from node import Node
from merkle_tree import MerkleTree


def merkle_proof(tx, merkle_tree):
    """Given a tx and a Merkle tree object, retrieve its list of tx's and
    parse through it to arrive at the minimum amount of information required
    to arrive at the correct block header. This does not include the tx
    itself.

    Return this data as a list; remember that order matters!
    """
    #### YOUR CODE HERE
    if not tx in merkle_tree.leaves:
        return []

    if len(merkle_tree.leaves) <= 1:
        return list()

    return explore(tx, merkle_tree.leaves.index(tx), merkle_tree._root, list())


def explore(target_tx, tx_idx, parent, proof_txs):
    left_child = parent._left
    right_child = parent._right

    if type(left_child) == str:
        if left_child == target_tx:
            proof_txs.append(Node('r', right_child))
        elif right_child == target_tx:
            proof_txs.append(Node('l', left_child))
        return proof_txs
    else:
        if tx_idx % 2 ** parent.height < 2 ** parent.height / 2:
            proof_txs.append(Node('r', right_child.data))
            return explore(target_tx, tx_idx, left_child, proof_txs)
        else:
            proof_txs.append(Node('l', left_child.data))
            return explore(target_tx, tx_idx, right_child, proof_txs)


def verify_proof(tx, merkle_proof):
    """Given a Merkle proof - constructed via `merkle_proof(...)` - verify
    that the correct block header can be retrieved by properly hashing the tx
    along with every other piece of data in the proof in the correct order
    """
    #### YOUR CODE HERE
    proof_nodes = merkle_proof[::-1]
    root_hash = tx
    for node in proof_nodes:
        if node.direction == 'l':
            root_hash = node.tx + root_hash
        else:
            root_hash = root_hash + node.tx
        root_hash = hash_data(root_hash)

    return root_hash


