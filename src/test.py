from recipe import *

if __name__ == "__main__":
    import random
    import time

    xrange = range
    try:
        from StringIO import StringIO
    except ImportError:
        from io import BytesIO as StringIO

    # Generates random data for the test
    # targetdata = ''.join([chr(random.randint(0, 127)) for n in range(1 << 16)])
    with open('source.txt', 'rb') as f:
        targetdata = f.read()

    chunks = [targetdata[i:i + 2048] for i in xrange(0, 1 << 17, 2048)]
    for i in xrange(8):
        a, b = (
            random.randrange(0, len(chunks)), random.randrange(0, len(chunks)))
        chunks[a], chunks[b] = chunks[b], chunks[a]

    # hostdata = ''.join([chr(random.randint(0, 127)) for n in range(1 << 16)])
    with open('destination.txt', 'rb') as f:
        hostdata = f.read()
    # with open('destination.txt', 'rb') as f:
    #     hostdata = f.read()

    # targetstream: file to be patched
    # hoststream: what the unpatched target needs to become
    # mergedstream: output after patching

    # Python 3 bytes compatibility
    mergedstream = StringIO()
    if __builtins__.bytes == str:
        targetstream = StringIO(targetdata)
        hoststream = StringIO(hostdata)
    else:
        targetstream = StringIO(bytes(targetdata, "ascii"))
        hoststream = StringIO(bytes(hostdata, "ascii"))

    # main process
    targetchecksums = blockchecksums(targetstream)
    binarypatch = rsyncdelta(hoststream, targetchecksums)
    patchstream(targetstream, mergedstream, binarypatch)

    mergedstream.seek(0)
    patcheddata = mergedstream.read()

    # write result to new file
    with open("result.txt", "wb") as f:
        f.write(patcheddata.encode("ascii"))

    if __builtins__.bytes == str:
        assert patcheddata == hostdata
    else:
        assert str(patcheddata, 'ascii') == hostdata

    print("Test passed.")
