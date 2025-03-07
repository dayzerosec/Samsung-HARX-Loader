'''
File:       harx_plugin_file.py
Authors:    @SpecterDev
Purpose:    Contains helper class for parsing H-Arx plugin files.
Note:       Most of the info here is undocumented and therefore reversed and not complete (and may have inaccuracies)
'''
import struct

PLUGIN_MAGIC    = b'PLUG-IN'
UH_MAGIC        = b'GREENTEA'

class HarxPluginFile:
    '''
    Layout of the H-Arx plugin header.
    
    struct harx_plugin_info
    {
        char magic[0x10];                            // 0x00

        union
        {
            struct harx_plugin_info_v1
            {
                uint64_t plugin_text_start;         // 0x10
                uint64_t plugin_text_end;           // 0x18
                uint64_t plugin_rodata_start;       // 0x20
                uint64_t plugin_rodata_end;         // 0x28
                uint64_t plugin_rwdata_start;       // 0x30
                uint64_t plugin_rwdata_end;         // 0x38
            }; // size: 0x40 (including common header)
            struct harx_plugin_info_v2 
            {
                char version_two[0x10];             // 0x10
                uint64_t plugin_text_start;         // 0x20
                uint64_t plugin_text_end;           // 0x28
                uint64_t plugin_rodata_start;       // 0x30
                uint64_t plugin_rodata_end;         // 0x38
                uint64_t plugin_rwdata_start;       // 0x40
                uint64_t plugin_rwdata_end;         // 0x48
                char unk_50h[0x10];                 // 0x50
                uint64_t plugin_rela_start;         // 0x60
                uint64_t plugin_rela_end;           // 0x68
                uint64_t unk_70h;                   // 0x70
            }; // size: 0x78 (including common header)
        };
    }; // size: 0x40 (v1) or 0x78 (v2)
    '''

    def __init__(self, f):
        # Check if its a recognized H-Arx plugin, and parse it if so
        self.valid = False
        self.data_offset = 0
        magic = f.read(0x00, 0x8)

        if magic == UH_MAGIC:
            # It's the UH (microhypervisor) plugin, which has the H-Arx header @ 0x1000
            # Double check this
            if f.read(0x1000, 0x7) == PLUGIN_MAGIC:
                self.valid = True
                self.parse_header(f, 0x1000)
                self.data_offset = 0x1000
        elif magic[:7] == PLUGIN_MAGIC:
            # It's a non-UH plugin @ 0x0
            self.valid = True
            self.parse_header(f, 0)

    def is_valid(self):
        return self.valid

    def parse_header(self, f, offset):
        # Check the version by checking if +0x10 is version two magic
        self.header_ver     = 1
        self.header_size    = 0x40
        if f.read(offset + 0x10, 0xC) == b'PLUG-IN_VER2':
            self.header_ver     = 2
            self.header_size    = 0x78

        # Parse header
        if self.header_ver == 1:
            self.text_start     = struct.unpack("<Q", f.read(offset + 0x10, 8))[0]
            self.text_end       = struct.unpack("<Q", f.read(offset + 0x18, 8))[0]
            self.rodata_start   = struct.unpack("<Q", f.read(offset + 0x20, 8))[0]
            self.rodata_end     = struct.unpack("<Q", f.read(offset + 0x28, 8))[0]
            self.rwdata_start   = struct.unpack("<Q", f.read(offset + 0x30, 8))[0]
            self.rwdata_end     = struct.unpack("<Q", f.read(offset + 0x38, 8))[0]
        elif self.header_ver == 2:
            self.text_start     = struct.unpack("<Q", f.read(offset + 0x20, 8))[0]
            self.text_end       = struct.unpack("<Q", f.read(offset + 0x28, 8))[0]
            self.rodata_start   = struct.unpack("<Q", f.read(offset + 0x30, 8))[0]
            self.rodata_end     = struct.unpack("<Q", f.read(offset + 0x38, 8))[0]
            self.rwdata_start   = struct.unpack("<Q", f.read(offset + 0x40, 8))[0]
            self.rwdata_end     = struct.unpack("<Q", f.read(offset + 0x48, 8))[0]
            self.rela_start     = struct.unpack("<Q", f.read(offset + 0x60, 8))[0]
            self.rela_end       = struct.unpack("<Q", f.read(offset + 0x68, 8))[0]

    def get_segment_range(self, seg):
        if seg == "text":
            return (self.text_start, self.text_end)
        elif seg == "rodata":
            return (self.rodata_start, self.rodata_end)
        elif seg == "rwdata":
            return (self.rwdata_start, self.rwdata_end)
        else:
            return (0, 0)

    def get_segment_addr(self, seg):
        if seg == "text":
            return self.text_start
        elif seg == "rodata":
            return self.rodata_start
        elif seg == "rwdata":
            return self.rwdata_start
        else:
            return 0

    def get_segment_data_offset(self, seg):
        base_addr = self.get_segment_addr("text")
        seg_addr = self.get_segment_addr(seg)
        return self.data_offset + (seg_addr - base_addr)

    def get_segment_size(self, seg):
        if seg == "text":
            return self.text_end - self.text_start
        elif seg == "rodata":
            return self.rodata_end - self.rodata_start
        elif seg == "rwdata":
            return self.rwdata_end - self.rwdata_start
        else:
            return 0

    def get_load_addr(self):
        return self.get_segment_range("text")[0]

    def get_entry_point_addr(self):
        return self.get_load_addr() + self.header_size
        