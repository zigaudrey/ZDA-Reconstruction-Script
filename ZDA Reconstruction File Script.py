# This script is used to recreate a ZDA file to MOD Giana's Return

# To not mess up, extract the ZDA file with Bartlomiej Duda's script and edit the files.
# The order of files and compression level doesn't matter.

# Script by Zigaudrey. Credit no needed

import os
import sys
import struct
import zlib

from itertools import cycle

def crypting_data(in_data, key_data):
    data_size = len(in_data)
    out_data = bytearray()
    
    for curr_offset in range(data_size):
        data_byte = struct.pack("B", in_data[curr_offset])
        xor_res = bytes(a ^ b for a, b in zip(struct.pack("B", in_data[curr_offset]), struct.pack("B", key_data[curr_offset])))
        out_data.extend(xor_res)
    
    return out_data

def create_key(targ_file):
    data_key= b'\xBB' + targ_file
    return data_key

def compress_data(in_file_path, out_folder_path):
    if not os.path.exists(out_folder_path):
        os.makedirs(out_folder_path)

    file_list = os.listdir(in_file_path)

    reconstructed = bytearray()
    recon_start = b'ZDA\x00' + struct.pack("<L", len(file_list)) + bytes(4)
    recon_header = bytearray()
    recon_body = bytearray()

    data_uncomp = []
    data_comp = []
    data_offset = []

    for i in range(len(file_list)):
        recon_header += bytes(file_list[i].encode("utf-8")) + bytes(52 - len(file_list[i]))

    recon_start = recon_start[:8] +  struct.pack("<L", len(recon_start) + len(recon_header)) 

    for i in range(len(file_list)):
        file_path= in_file_path + file_list[i]
                                
        bmp_file = open(file_path, 'rb')
        bas_file = bmp_file.read()
        bmp_file.close()
        data_offset.append(struct.pack("<L", len(recon_body)))
        data_uncomp.append(struct.pack("<L", len(bas_file)))
        key_data = create_key(bas_file) #Key is itself with b"\xBB" added at the first
        c_data= crypting_data(bas_file, key_data)
        c_data= zlib.compress(c_data, 6) #Compression Lvl
        data_comp.append(struct.pack("<L", len(c_data)))
        recon_body += c_data
    
    f_path = out_folder_path + "sprite-MOD.zda"

    recon_header = bytearray()

    for i in range(len(file_list)):
        recon_header += bytes(file_list[i].encode("utf-8")) + bytes(40 - len(file_list[i])) + data_uncomp[i] + data_comp[i] + data_offset[i]

    reconstructed = recon_start + recon_header + recon_body

    out_file = open(f_path, "wb+")
    out_file.write(reconstructed)
    out_file.close()


def main():
    folder_path = "Put Folder Path"
    p_out_folder_path = "Put Output Folder Path"
    compress_data(folder_path, p_out_folder_path)

main()
