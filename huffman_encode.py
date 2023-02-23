import numpy as np

class Node:

    def __init__(self, val = None, isLeaf = False):
        self.val = val
        self.isLeaf = isLeaf


def tree_visit(node, tree, code = ""):

    if node.isLeaf:
        tree[ord(node.val)] = code
        return

    tree_visit(node.left, tree, code + "0")
    tree_visit(node.right, tree, code + "1")


def encode_tree(node):

    if node.isLeaf:
        return "1" + f"{int(bin(ord(node.val))[2:]):07}"
    else:
        return "0" + encode_tree(node.left) + encode_tree(node.right)


f = open("input.txt", "r")
outfile = open("encoded.txt", "wb")

msg = "".join(f.readlines())
arr_msg = np.array(list(msg))
unique_ele = np.unique(arr_msg)

node_arr = []
for x in unique_ele:
    
    count = (x == arr_msg).sum()
    new_node = Node(x, True)

    node_arr.append([count, new_node])

node_arr.sort(key=lambda x: x[0])

if len(node_arr) != 1:
    while len(node_arr) != 1:

        left = node_arr.pop(0)
        right = node_arr.pop(0)

        new_node = Node()
        new_node.left = left[1]
        new_node.right = right[1]

        count = left[0] + right[0]
        node_arr.append([count, new_node])
        node_arr.sort(key=lambda x: x[0])


    root_node = node_arr[0][1]
    huffman_tree = {}
    tree_visit(root_node, huffman_tree)

else:
    root_node = node_arr[0][1]
    huffman_tree = {}
    huffman_tree[ord(root_node.val)] = "0"

tree_len = f"{int(bin(len(huffman_tree))[2:]):08}"
encoded_tree = encode_tree(root_node)

encoded_msg = ""
for m in msg:
    encoded_msg += huffman_tree[ord(m)]

padding = 8 - (len(tree_len) + 3 + len(encoded_tree) + len(encoded_msg)) % 8
encoded_data = tree_len + f"{int(bin(padding)[2:]):03}" + encoded_tree + encoded_msg + ("0" * padding)

for i in range(0, len(encoded_data), 8):
    outfile.write(int(encoded_data[i : i + 8], 2).to_bytes(1, byteorder='big'))

f.close()
outfile.close()