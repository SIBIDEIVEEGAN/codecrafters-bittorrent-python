import json
import sys

# import bencodepy - available if you need it!
# import requests - available if you need it!

# Examples:
#
# - decode_bencode(b"5:hello") -> b"hello"
# - decode_bencode(b"10:hello12345") -> b"hello12345"



def decode_bencode(bencoded_value):
    if chr(bencoded_value[0]).isdigit():
                
                len , rest = bencoded_value.split(b":",1)
                len = int(len)
                return rest[:len],rest[len:]   # add the next part of data
                
    elif chr(bencoded_value[0]) == "i":
       
       end = bencoded_value.index(b"e")
       return int(bencoded_value[1:end]),bencoded_value[end+1:]
      
    elif chr(bencoded_value[0]) == "l":
        bencoded_value = bencoded_value[1:]
        rlist = []
        while not bencoded_value.startswith(b"e"): 
            itm,bencoded_value=decode_bencode(bencoded_value) 
            rlist.append(itm)
            
        return rlist,bencoded_value[1:]
                       # remove what we just added from data
    elif chr(bencoded_value[0]) == "d":
         
         bencoded_value = bencoded_value[1:]
         rlist = {}
         while not bencoded_value.startswith(b"e"): 
            itmk,bencoded_value=decode_bencode(bencoded_value) 
            itmv,bencoded_value=decode_bencode(bencoded_value) 
            rlist[itmk.decode()] = itmv
            
         return rlist,bencoded_value[1:]
       
    else:
        raise NotImplementedError("Only strings are supported at the moment")


def main():
    command = sys.argv[1]

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    #print("Logs from your program will appear here!")

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # Let's convert them to strings for printing to the console.
        def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()

            raise TypeError(f"Type not serializable: {type(data)}")

        # Uncomment this block to pass the first stage
        data,_=decode_bencode(bencoded_value)
        print(json.dumps(data, default=bytes_to_str))
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
