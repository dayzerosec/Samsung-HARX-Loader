#pragma author Specter
#pragma description harx_plugin_info

import type.base;

using uint64_t = u64;

struct harx_plugin_header_v1
{
	char magic[0x10];
	type::Hex<u64> plugin_text_start;         // 0x10
	type::Hex<u64> plugin_text_end;           // 0x18
	type::Hex<u64> plugin_rodata_start;       // 0x20
	type::Hex<u64> plugin_rodata_end;         // 0x28
	type::Hex<u64> plugin_rwdata_start;       // 0x30
	type::Hex<u64> plugin_rwdata_end;         // 0x38
};

struct harx_plugin_header_v2
{
    char magic[0x10];
    char version_two[0x10];             // 0x10 - should be "PLUG-IN_VER2"
	type::Hex<u64> plugin_text_start;         // 0x20
	type::Hex<u64> plugin_text_end;           // 0x28
	type::Hex<u64> plugin_rodata_start;       // 0x30
	type::Hex<u64> plugin_rodata_end;         // 0x38
	type::Hex<u64> plugin_rwdata_start;       // 0x40
	type::Hex<u64> plugin_rwdata_end;         // 0x48
	char unk_50h[0x10];                 // 0x50
	type::Hex<u64> plugin_rela_start;         // 0x60
	type::Hex<u64> plugin_rela_end;           // 0x68
	type::Hex<u64> unk_70h;                   // 0x70
};

harx_plugin_header_v2 header @ 0x1000;