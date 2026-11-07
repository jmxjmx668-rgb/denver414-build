/* Huawei Nova 7 SE 5G (CDY-AN00) — kirin820 / emui12(HarmonyOS2) 2.0.0.294(C00E230R4P6)
 * kernel 4.14.116, VA_BITS=39, KASLR on, CFI on, no SELINUX_DEVELOP.
 * Offsets extracted from a toolchain-matched rebuild (clang-r353983c) of the
 * CDY_HarmonyOS2.0 kernel source with the device's runtime config.
 * NOTE: provisional values pending artifact extraction — VERIFY before use. */
OFFSETS_ENTRY("4.14.116",
  .kernel_phys_load=0x00080000ULL, STRUCT_OFFSETS_CDY414,
  .kimage_text_base=0xffffff8008080000ULL,
  .off_init_task=0, .off_init_cred=0, .off_init_uts_ns=0, .off_empty_zero_page=0,
  .off_root_task_group=0,
  .off_selinux_enforcing=0, /* variable does not exist (no SELINUX_DEVELOP) */
  .off_kptr_restrict=0,
  .off_selinux_blob_sizes=0, .off_security_hook_heads=0, .off_kmalloc_caches=0,
  .off_anon_pipe_buf_ops=0,
  .off_ashmem_misc_fops=0, .off_ashmem_fops=0,
  .off_ashmem_ioctl=0, .off_ashmem_compat_ioctl=0, .off_ashmem_mmap=0,
  .off_ashmem_open=0, .off_ashmem_release=0, .off_ashmem_show_fdinfo=0,
  .off_configfs_read_iter=0, .off_configfs_bin_write_iter=0,
  .off_copy_splice_read=0, .off_noop_llseek=0, .off_cap_capable_active=0,
  .off_slide_nfulnl_logger=0, .off_slide_loggers_0_1=0, .off_slide_boot_id=0,
  .off_sysctl_perf_event_paranoid=0,
  .off_system_unbound_wq=0, .off_call_usermodehelper_exec_work=0,
),
