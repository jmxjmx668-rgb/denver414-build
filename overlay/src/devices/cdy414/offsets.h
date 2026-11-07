/* Huawei Nova 7 SE 5G (CDY-AN00) - kirin820 / HarmonyOS2 2.0.0.294(C00E230R4P6)
 * kernel 4.14.116, VA_BITS=39, KASLR on, CFI on, LTO on, no SELINUX_DEVELOP.
 * Symbol offsets extracted from the STOCK boot.img kallsyms (191k symbols).
 * Struct offsets from the toolchain-matched rebuild DWARF. */
OFFSETS_ENTRY("4.14.116",
  .kernel_phys_load=0x00080000ULL, .phys_offset=0, STRUCT_OFFSETS_CDY414,
  .kimage_text_base=0xffffff8008080000ULL,
  .off_init_task=0x2ED2F40, .off_init_cred=0x2EE40B0, .off_init_uts_ns=0x2ED2D00, .off_empty_zero_page=0x31CC000,
  .off_root_task_group=0x31D2A40,
  .off_selinux_enforcing=0, /* absent */
  .off_kptr_restrict=0x2ED2450,
  .off_selinux_blob_sizes=0, .off_security_hook_heads=0x1FE0698, .off_kmalloc_caches=0x1FE01F8,
  .off_anon_pipe_buf_ops=0x2014E00,
  .off_ashmem_misc_fops=0x305F8B8, /* ashmem_misc.fops field */
  .off_ashmem_fops=0x20D7108,
  .off_ashmem_ioctl=0x1FA1A34, .off_ashmem_compat_ioctl=0, .off_ashmem_mmap=0x1FA1C74,
  .off_ashmem_open=0x1FAE3D8, .off_ashmem_release=0x1FAE3DC, .off_ashmem_show_fdinfo=0,
  .off_configfs_read_iter=0, .off_configfs_bin_write_iter=0,
  .off_copy_splice_read=0, .off_noop_llseek=0x1F9F144, .off_cap_capable_active=0,
  .off_slide_nfulnl_logger=0x2EC7080, .off_slide_loggers_0_1=0x2EC7080, .off_slide_boot_id=0x333B5A4,
  .off_system_unbound_wq=0x2EC1B38, .off_call_usermodehelper_exec_work=0x1FACDB0,
  .off_sysctl_perf_event_paranoid=0x2EC21E8,
),
