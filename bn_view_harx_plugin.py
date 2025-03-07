'''
File:       bn_view_harx_plugin.py
Authors:    @SpecterDev
Purpose:    Implements the H-Arx plugin view for binary ninja
'''

import binaryninja as bn
from .harx_plugin_file import HarxPluginFile

class HarxPluginView(bn.BinaryView):
    name = "H-Arx Plugin"
    long_name = "H-Arx Plugin"

    def log(self, msg, error=False):
        msg = f"[H-Arx Plugin Loader] {msg}"
        if not error:
            bn.log_info(msg)
        else:
            bn.log_error(msg)

    def __init__(self, data):
        bn.BinaryView.__init__(self, parent_view=data, file_metadata=data.file)
        self.data = data
        self.plugin_file = HarxPluginFile(data)

    @classmethod
    def is_valid_for_data(self, data):
        self.plugin_file = HarxPluginFile(data)
        return self.plugin_file.is_valid()

    def perform_get_address_size(self):
        return 4

    def init(self):
        # H-Arx plugins will be ARMv8 / AARCH64
        self.arch = bn.Architecture["aarch64"]
        self.platform = self.arch.standalone_platform

        # Load the binary
        plugin = self.plugin_file
        self.load_address = plugin.get_load_addr()

        self.log("Detected H-Arx plugin")

        # Map .text
        text_addr   = plugin.get_segment_addr("text")
        text_size   = plugin.get_segment_size("text")
        text_offset = plugin.get_segment_data_offset("text")
        self.add_auto_segment(
            text_addr,
            text_size,
            text_offset,
            text_size,
            bn.SegmentFlag.SegmentReadable | bn.SegmentFlag.SegmentExecutable
        )

        self.add_user_section(
            "code",
            text_offset,
            text_size,
            bn.SectionSemantics.ReadOnlyCodeSectionSemantics
        )

        # Map .rodata
        rodata_addr   = plugin.get_segment_addr("rodata")
        rodata_size   = plugin.get_segment_size("rodata")
        rodata_offset = plugin.get_segment_data_offset("rodata")
        self.add_auto_segment(
            rodata_addr,
            rodata_size,
            rodata_offset,
            rodata_size,
            bn.SegmentFlag.SegmentReadable
        )

        self.add_user_section(
            "rodata",
            rodata_offset,
            rodata_size,
            bn.SectionSemantics.ReadOnlyDataSectionSemantics
        )

        # Map .data
        rwdata_addr   = plugin.get_segment_addr("rwdata")
        rwdata_size   = plugin.get_segment_size("rwdata")
        rwdata_offset = plugin.get_segment_data_offset("rwdata")
        self.add_auto_segment(
            rwdata_addr,
            rwdata_size,
            rwdata_offset,
            rwdata_size,
            bn.SegmentFlag.SegmentReadable | bn.SegmentFlag.SegmentWritable
        )

        self.add_user_section(
            "rwdata",
            rwdata_offset,
            rwdata_size,
            bn.SectionSemantics.ReadWriteDataSectionSemantics
        )

        # Entry point is after the header
        entry_point_addr = plugin.get_entry_point_addr()
        self.add_entry_point(entry_point_addr)

        self.define_auto_symbol_and_var_or_function(
            bn.Symbol(bn.SymbolType.FunctionSymbol, entry_point_addr, "_start"),
            bn.Type.function(bn.Type.void(), []),
            bn.Architecture["aarch64"].standalone_platform
        )

        self.update_analysis()

        return True
