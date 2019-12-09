import ctypes
from hexdump import hexdump

class AlacDecoder:
    def __init__(self):
        self.libalac = ctypes.CDLL("./ap2/libalac-wr.dylib", use_errno=True)
        self.libalac.apple_alac_init.restype = ctypes.c_int
        self.libalac.apple_alac_decode_frame.restype = ctypes.c_int
        self.libalac.apple_alac_terminate.restype = ctypes.c_int

    def init(self):
        fmt = (ctypes.c_int * 12)()
        fmt[0] = 96
        fmt[1] = 352
        fmt[2] = 0
        fmt[3] = 16
        fmt[4] = 40
        fmt[5] = 10
        fmt[6] = 14
        fmt[7] = 2
        fmt[8] = 255
        fmt[9] = 0
        fmt[10] = 0
        fmt[11] = 44100

        res = self.libalac.apple_alac_init(fmt)
        return res

    def decode_frame(self, frame):
        data_len = ctypes.c_uint(len(frame))
        buf = ctypes.create_string_buffer(4096)
        buf_len = ctypes.c_int(len(buf))
        res = self.libalac.apple_alac_decode_frame(frame, data_len, buf, ctypes.byref(buf_len))
        return res, buf[:buf_len.value*4]

    def terminate(self):
        self.libalac.apple_alac_terminate()
        del self.libalac
