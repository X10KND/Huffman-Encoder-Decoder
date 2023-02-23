position = 0
found = 0

def decode_tree(b, limit, tree, code = ""):

    global position, found

    if found == limit:
        return

    if b[position] == "1":
        found += 1
        tree[code] = int(b[position + 1: position + 8], 2)
        position += 8
        return

    else:
        position += 1
        left = decode_tree(b, limit, tree, code + "0")
        right = decode_tree(b, limit, tree, code + "1")

f = open("encoded.txt", "rb")
outfile = open("decoded.txt", "w")

read_msg = f.readlines()

encoded_data = []
for m in read_msg:
    encoded_data += m

encoded_msg = ""
for m in encoded_data:
    encoded_msg += f"{int(bin(m)[2:]):08}"

tree_len = int(encoded_msg[0:8], 2)
padding = int(encoded_msg[8:11], 2)
encoded_msg = encoded_msg[11:]

huffman_table = {}

if tree_len > 1:
    decode_tree(encoded_msg, tree_len, huffman_table)
else:
    decode_tree(encoded_msg, tree_len, huffman_table, "0")
    
encoded_msg = encoded_msg[position : -padding]

i = 0
out = ""
out_msg = ""
while i < len(encoded_msg):

    out += encoded_msg[i]
    try:
        out_msg += chr(huffman_table[out])
        out = ""
    except:
        pass

    i += 1

print(out_msg)
outfile.write(out_msg)

f.close()
outfile.close()
