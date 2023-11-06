import numpy as np

def encode_one_number(initial_number):
    new_number = bin(abs(int(np.round(initial_number * (10 ** 5), 0)))).replace('0b', '') 
    while len(new_number) < 32:
        new_number = '0' + new_number
    #print(new_number)
    if initial_number < 0:
        new_number = new_number.replace('0', '2').replace('1', '0').replace('2', '1')  
        #print(new_number)
        index_to_add = len(new_number) - 1
        added = False
        while not added and index_to_add >= 0:
            if new_number[index_to_add] == '0':
                new_number = new_number[:index_to_add] + '1' + new_number[index_to_add + 1:]
                added = True
                break
            if new_number[index_to_add] == '1':
                new_number = new_number[:index_to_add] + '0' + new_number[index_to_add + 1:]
                index_to_add -= 1 
        if not added:
            new_number = '1' + new_number
    #print(new_number)
    new_number = new_number[1:] + '0'
    #print(new_number)
    if initial_number < 0:
        new_number = new_number.replace('0', '2').replace('1', '0').replace('2', '1')
    #print(new_number)
    chunk_list = []
    index_start = 32
    while index_start >= 5:
        chunk_list.append(new_number[index_start - 5:index_start])
        index_start -= 5 
    while chunk_list[-1] == '00000':
        chunk_list = chunk_list[:-1]
    #print(chunk_list)
    for chunk_num in range(len(chunk_list) - 1):
        chunk_list[chunk_num] = '1' + chunk_list[chunk_num] 
    chunk_list[len(chunk_list) - 1] = '0' + chunk_list[len(chunk_list) - 1] 
    #print(chunk_list)
    for chunk_num in range(len(chunk_list)):
        chunk_list[chunk_num] = chr(int(chunk_list[chunk_num], 2) + 63)
    #print(chunk_list)
    ret_str = ""
    for chunk_num in range(len(chunk_list)):
        ret_str += chunk_list[chunk_num]
    return ret_str
     
def encode_list(list_coord):
    list_coord = return_offset(list_coord)
    for coord_num in range(len(list_coord)):
        list_coord[coord_num] = encode_one_number(list_coord[coord_num])
    return list_coord

def return_offset(list_coord):
    for coord_num in range(len(list_coord) - 1, 0, -1):
        list_coord[coord_num] -= list_coord[coord_num - 1]
    return list_coord
  
print(encode_one_number(-179.9832104))
print(encode_list([38.5, 40.7, 43.252]))
print(encode_list([-120.2, -120.95, -126.453]))
