def bytes_from_file(filename, filesize=False, chunksize=8192):
    "Generator for yielding bytes from file"
    print("DBG:BINFILE: Opening file %s" % filename)
    with open(filename, "rb") as f:
        while True:
            # print("DBG: Getting new chunk")
            # print("DBG: Ptr at %s" % f.tell())
            if filesize:
                print("DBG: %s %% Done" % (f.tell()*100 / filesize))
            chunk = f.read(chunksize)
            if chunk:
                yield chunk
                # for b in chunk:
                #     yield b
            else:
                print("DBG: Have now read entire file")
                break
