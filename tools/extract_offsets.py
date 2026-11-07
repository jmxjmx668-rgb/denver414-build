#!/usr/bin/env python3
"""Extract GhostLock offset table for CDY-AN00 4.14 from build artifacts.

Inputs: System.map (kallsyms), vmlinux (ELF+DWARF).
Outputs: src/devices/cdy414/offsets.h snippet + common.h constants.
"""
import re
import struct
import sys
import json
from elftools.elf.elffile import ELFFile


def parse_system_map(path):
    syms = {}
    text_base = None
    for line in open(path, encoding='utf-8', errors='replace'):
        parts = line.split()
        if len(parts) < 3:
            continue
        try:
            addr = int(parts[0], 16)
        except ValueError:
            continue
        name = parts[2]
        syms[name] = addr
        if name == '_text' and text_base is None:
            text_base = addr
    return syms, text_base


def dwarf_member_offsets(vmlinux_path, struct_names):
    """Return {struct: {member: offset}} from DWARF (first matching CU)."""
    out = {}
    with open(vmlinux_path, 'rb') as f:
        elf = ELFFile(f)
        if not elf.has_dwarf_info():
            raise RuntimeError('no DWARF in vmlinux (CONFIG_DEBUG_INFO?)')
        dw = elf.get_dwarf_info()
        for cu in dw.iter_CUs():
            for die in cu.iter_DIEs():
                if die.tag != 'DW_TAG_structure_type':
                    continue
                name = die.attributes.get('DW_AT_name')
                if not name:
                    continue
                n = name.value.decode('ascii', 'replace')
                if n not in struct_names or n in out:
                    continue
                members = {}
                for ch in die.iter_children():
                    if ch.tag != 'DW_TAG_member':
                        continue
                    mn = ch.attributes.get('DW_AT_name')
                    mo = ch.attributes.get('DW_AT_data_member_location')
                    if mn is None:
                        continue
                    off = 0
                    if mo is not None:
                        if mo.form == 'DW_FORM_exprloc':
                            off = struct.unpack('<B', mo.value[:1])[0] if len(mo.value) == 1 else mo.value[1]
                            if len(mo.value) >= 2 and mo.value[0] == 0x23:  # DW_OP_plus_uconst
                                off = struct.unpack('<B', mo.value[1:2])[0]
                                if len(mo.value) > 2:
                                    off = int.from_bytes(mo.value[2:], 'little')
                        else:
                            off = mo.value
                    members[mn.value.decode('ascii', 'replace')] = off
                size = die.attributes.get('DW_AT_byte_size')
                members['__size'] = size.value if size else 0
                out[n] = members
            if all(s in out for s in struct_names):
                break
    return out


WANT_STRUCTS = {
    'task_struct', 'mm_struct', 'file_operations', 'rt_mutex_waiter',
    'rt_mutex', 'cred',
}

WANT_SYMS = [
    'init_task', 'init_cred', 'init_uts_ns', 'empty_zero_page',
    'root_task_group', 'kptr_restrict', 'selinux_blob_sizes',
    'security_hook_heads', 'kmalloc_caches', 'anon_pipe_buf_ops',
    'ashmem_misc', 'ashmem_fops', 'ashmem_ioctl', 'ashmem_compat_ioctl',
    'ashmem_mmap', 'ashmem_open', 'ashmem_release', 'ashmem_show_fdinfo',
    'configfs_read_iter', 'configfs_bin_write_iter', 'copy_splice_read',
    'noop_llseek', 'loggers', 'sysctl_bootid', 'system_unbound_wq',
    'call_usermodehelper_exec_work', 'init_user_ns', 'perf_event_paranoid',
    'nf_log_none', 'nf_log_syslog', 'sysctl_perf_event_paranoid', 'init_files', 'init_fs', 'ksoftirqd',
]


def main():
    smap, vmlinux = sys.argv[1], sys.argv[2]
    syms, text_base = parse_system_map(smap)
    print('[+] System.map: %d symbols, _text=0x%x' % (len(syms), text_base))
    off = {}
    miss = []
    for s in WANT_SYMS:
        if s in syms:
            off[s] = syms[s] - text_base
        else:
            miss.append(s)
    print('[-] missing symbols:', miss)

    structs = dwarf_member_offsets(vmlinux, WANT_STRUCTS)
    print('[+] DWARF structs found:', {k: v.get('__size') for k, v in structs.items()})

    res = {'_text': text_base, 'symbols': off, 'structs': structs}
    json.dump(res, open('cdy_offsets.json', 'w'), indent=1)
    print('[+] wrote cdy_offsets.json')

    # render a preview of the device table
    def o(name):
        v = off.get(name)
        return '0x%08X' % v if v is not None else '0'

    ts = structs.get('task_struct', {})
    mm = structs.get('mm_struct', {})
    fo = structs.get('file_operations', {})
    rw = structs.get('rt_mutex_waiter', {})
    print('''
=== preview ===
kimage_text_base = 0xffffff8008080000
mm size = 0x%x, order estimate = %d
waiter: task=0x%x lock=0x%x prio=0x%x deadline=0x%x size=0x%x
task: prio=0x%x pi_blocked_on=0x%x cred=0x%x real_cred=0x%x pid=0x%x comm=0x%x tasks=0x%x seccomp=0x%x
fops: llseek=0x%x read=0x%x write=0x%x read_iter=0x%x write_iter=0x%x ioctl=0x%x compat=0x%x mmap=0x%x open=0x%x release=0x%x
''' % (
        mm.get('__size', 0), (mm.get('__size', 1) - 1).bit_length() - 12,
        rw.get('task', 0), rw.get('lock', 0), rw.get('prio', 0), rw.get('deadline', 0), rw.get('__size', 0),
        ts.get('prio', 0), ts.get('pi_blocked_on', 0), ts.get('cred', 0), ts.get('real_cred', 0),
        ts.get('pid', 0), ts.get('comm', 0), ts.get('tasks', 0), ts.get('seccomp', 0),
        fo.get('llseek', 0), fo.get('read', 0), fo.get('write', 0), fo.get('read_iter', 0),
        fo.get('write_iter', 0), fo.get('unlocked_ioctl', 0), fo.get('compat_ioctl', 0),
        fo.get('mmap', 0), fo.get('open', 0), fo.get('release', 0)))


if __name__ == '__main__':
    main()
