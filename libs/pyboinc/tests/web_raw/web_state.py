server_version = """<boinc_gui_rpc_reply>
<server_version>
   <major>7</major>
   <minor>16</minor>
   <release>3</release>
</server_version>
</boinc_gui_rpc_reply>
"""

cc_status = """<boinc_gui_rpc_reply>
<cc_status>
   <network_status>2</network_status>
   <ams_password_error>0</ams_password_error>
   <task_suspend_reason>8</task_suspend_reason>
   <task_mode>2</task_mode>
   <task_mode_perm>2</task_mode_perm>
   <task_mode_delay>0.000000</task_mode_delay>
   <gpu_suspend_reason>0</gpu_suspend_reason>
   <gpu_mode>2</gpu_mode>
   <gpu_mode_perm>2</gpu_mode_perm>
   <gpu_mode_delay>0.000000</gpu_mode_delay>
   <network_suspend_reason>0</network_suspend_reason>
   <network_mode>2</network_mode>
   <network_mode_perm>2</network_mode_perm>
   <network_mode_delay>0.000000</network_mode_delay>
   <disallow_attach>0</disallow_attach>
   <simple_gui_only>0</simple_gui_only>
   <max_event_log_lines>2000</max_event_log_lines>
</cc_status>
</boinc_gui_rpc_reply>
"""

disk_usage_summary = """<boinc_gui_rpc_reply>
<disk_usage_summary>
<project>
  <master_url>https://csgrid.org/csg/</master_url>
  <disk_usage>0.000000</disk_usage>
</project>
<project>
  <master_url>http://www.gpugrid.net/</master_url>
  <disk_usage>344319715.000000</disk_usage>
</project>
<d_total>30376042496.000000</d_total>
<d_free>23042801664.000000</d_free>
<d_boinc>422143.000000</d_boinc>
<d_allowed>15188021248.000000</d_allowed>
</disk_usage_summary>
</boinc_gui_rpc_reply>
"""

file_transfers = """<boinc_gui_rpc_reply>
<file_transfers>
</file_transfers>
</boinc_gui_rpc_reply>
"""

host_info = """<boinc_gui_rpc_reply>
<host_info>
    <timezone>7200</timezone>
    <domain_name>localhost.localdomain</domain_name>
    <ip_addr></ip_addr>
    <host_cpid>6ff7ac390e38920ad823c0cad62fa674</host_cpid>
    <p_ncpus>4</p_ncpus>
    <p_vendor>AuthenticAMD</p_vendor>
    <p_model>AMD Phenom(tm) II X4 955 Processor [Family 16 Model 4 Stepping 3]</p_model>
    <p_features>fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm 3dnowext 3dnow constant_tsc rep_good nopl nonstop_tsc cpuid extd_apicid pni monitor cx16 popcnt lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw ibs skinit wdt hw_pstate vmmcall npt lbrv svm_lock nrip_save</p_features>
    <p_fpops>3739229239.108397</p_fpops>
    <p_iops>58382830997.115273</p_iops>
    <p_membw>1000000000.000000</p_membw>
    <p_calculated>1586431995.189977</p_calculated>
    <p_vm_extensions_disabled>0</p_vm_extensions_disabled>
    <m_nbytes>12552216576.000000</m_nbytes>
    <m_cache>524288.000000</m_cache>
    <m_swap>12591296512.000000</m_swap>
    <d_total>30376042496.000000</d_total>
    <d_free>23042801664.000000</d_free>
    <os_name>Linux openSUSE</os_name>
    <os_version>openSUSE Tumbleweed [5.5.9-1-default|libc 2.31 (GNU libc)]</os_version>
    <n_usable_coprocs>1</n_usable_coprocs>
    <wsl_available>0</wsl_available>
    <coprocs>
<coproc_cuda>
   <count>1</count>
   <name>GeForce GTX 1060 6GB</name>
   <available_ram>4167041024.000000</available_ram>
   <have_cuda>1</have_cuda>
   <have_opencl>1</have_opencl>
   <peak_flops>4373760000000.000000</peak_flops>
   <cudaVersion>10020</cudaVersion>
   <drvVersion>44064</drvVersion>
   <totalGlobalMem>4294967295.000000</totalGlobalMem>
   <sharedMemPerBlock>49152.000000</sharedMemPerBlock>
   <regsPerBlock>65536</regsPerBlock>
   <warpSize>32</warpSize>
   <memPitch>2147483647.000000</memPitch>
   <maxThreadsPerBlock>1024</maxThreadsPerBlock>
   <maxThreadsDim>1024 1024 64</maxThreadsDim>
   <maxGridSize>2147483647 65535 65535</maxGridSize>
   <clockRate>1708500</clockRate>
   <totalConstMem>65536.000000</totalConstMem>
   <major>6</major>
   <minor>1</minor>
   <textureAlignment>512.000000</textureAlignment>
   <deviceOverlap>1</deviceOverlap>
   <multiProcessorCount>10</multiProcessorCount>
   <coproc_opencl>
      <name>GeForce GTX 1060 6GB</name>
      <vendor>NVIDIA Corporation</vendor>
      <vendor_id>4318</vendor_id>
      <available>1</available>
      <half_fp_config>0</half_fp_config>
      <single_fp_config>191</single_fp_config>
      <double_fp_config>63</double_fp_config>
      <endian_little>1</endian_little>
      <execution_capabilities>1</execution_capabilities>
      <extensions>cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_fp64 cl_khr_byte_addressable_store cl_khr_icd cl_khr_gl_sharing cl_nv_compiler_options cl_nv_device_attribute_query cl_nv_pragma_unroll cl_nv_copy_opts cl_nv_create_buffer cl_khr_int64_base_atomics cl_khr_int64_extended_atomics</extensions>
      <global_mem_size>6365118464</global_mem_size>
      <local_mem_size>49152</local_mem_size>
      <max_clock_frequency>1708</max_clock_frequency>
      <max_compute_units>10</max_compute_units>
      <nv_compute_capability_major>6</nv_compute_capability_major>
      <nv_compute_capability_minor>1</nv_compute_capability_minor>
      <amd_simd_per_compute_unit>0</amd_simd_per_compute_unit>
      <amd_simd_width>0</amd_simd_width>
      <amd_simd_instruction_width>0</amd_simd_instruction_width>
      <opencl_platform_version>OpenCL 1.2 CUDA 10.2.141</opencl_platform_version>
      <opencl_device_version>OpenCL 1.2 CUDA</opencl_device_version>
      <opencl_driver_version>440.64.00</opencl_driver_version>
   </coproc_opencl>
<pci_info>
   <bus_id>1</bus_id>
   <device_id>0</device_id>
   <domain_id>0</domain_id>
</pci_info>
</coproc_cuda>
    </coprocs>
</host_info>
</boinc_gui_rpc_reply>
"""

seqno = """<boinc_gui_rpc_reply>
<seqno>47</seqno>
</boinc_gui_rpc_reply>
"""

msgs = """<boinc_gui_rpc_reply>
<msgs>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>1</seqno>
 <body><![CDATA[
Starting BOINC client version 7.16.3 for x86_64-suse-linux-gnu
]]></body>
 <time>1586722353</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>2</seqno>
 <body><![CDATA[
log flags: file_xfer, sched_ops, task
]]></body>
 <time>1586722353</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>3</seqno>
 <body><![CDATA[
Libraries: libcurl/7.69.1 OpenSSL/1.1.1d-fips zlib/1.2.11 libidn2/2.3.0 libpsl/0.21.0 (+libidn2/2.3.0) libssh/0.9.3/openssl/zlib nghttp2/1.40.0
]]></body>
 <time>1586722353</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>4</seqno>
 <body><![CDATA[
Data directory: /var/lib/boinc
]]></body>
 <time>1586722353</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>5</seqno>
 <body><![CDATA[
CUDA: NVIDIA GPU 0: GeForce GTX 1060 6GB (driver version 440.64, CUDA version 10.2, compute capability 6.1, 4096MB, 3974MB available, 4374 GFLOPS peak)
]]></body>
 <time>1586722354</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>6</seqno>
 <body><![CDATA[
OpenCL: NVIDIA GPU 0: GeForce GTX 1060 6GB (driver version 440.64.00, device version OpenCL 1.2 CUDA, 6070MB, 3974MB available, 4374 GFLOPS peak)
]]></body>
 <time>1586722354</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>7</seqno>
 <body><![CDATA[
[libc detection] gathered: 2.31, GNU libc
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>8</seqno>
 <body><![CDATA[
Host name: localhost.localdomain
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>9</seqno>
 <body><![CDATA[
Processor: 4 AuthenticAMD AMD Phenom(tm) II X4 955 Processor [Family 16 Model 4 Stepping 3]
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>10</seqno>
 <body><![CDATA[
Processor features: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm 3dnowext 3dnow constant_tsc rep_good nopl nonstop_tsc cpuid extd_apicid pni monitor cx16 popcnt lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw ibs skinit wdt hw_pstate vmmcall npt lbrv svm_lock nrip_save
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>11</seqno>
 <body><![CDATA[
OS: Linux openSUSE: openSUSE Tumbleweed [5.5.9-1-default|libc 2.31 (GNU libc)]
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>12</seqno>
 <body><![CDATA[
Memory: 11.69 GB physical, 11.73 GB virtual
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>13</seqno>
 <body><![CDATA[
Disk: 28.29 GB total, 21.46 GB free
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>14</seqno>
 <body><![CDATA[
Local time is UTC +2 hours
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>15</seqno>
 <body><![CDATA[
Config: don't use GPUs while firefox is running
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>16</seqno>
 <body><![CDATA[
General prefs: from GPUGRID (last modified 19-Mar-2020 17:04:26)
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>17</seqno>
 <body><![CDATA[
Host location: none
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>18</seqno>
 <body><![CDATA[
General prefs: using your defaults
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>19</seqno>
 <body><![CDATA[
Reading preferences override file
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>20</seqno>
 <body><![CDATA[
Preferences:
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>21</seqno>
 <body><![CDATA[
   max memory usage when active: 5985.36 MB
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>22</seqno>
 <body><![CDATA[
   max memory usage when idle: 10773.65 MB
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>23</seqno>
 <body><![CDATA[
   max disk usage: 14.14 GB
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>24</seqno>
 <body><![CDATA[
   suspend work if non-BOINC CPU load exceeds 25%
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>25</seqno>
 <body><![CDATA[
   (to change preferences, visit a project web site or select Preferences in the Manager)
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>26</seqno>
 <body><![CDATA[
Setting up project and slot directories
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>27</seqno>
 <body><![CDATA[
Checking active tasks
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project>Citizen Science Grid</project>
 <pri>1</pri>
 <seqno>28</seqno>
 <body><![CDATA[
URL https://csgrid.org/csg/; Computer ID 110693; resource share 100
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>29</seqno>
 <body><![CDATA[
URL http://www.gpugrid.net/; Computer ID 539892; resource share 100
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>30</seqno>
 <body><![CDATA[
Setting up GUI RPC socket
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>31</seqno>
 <body><![CDATA[
Checking presence of 65 project files
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project></project>
 <pri>1</pri>
 <seqno>32</seqno>
 <body><![CDATA[
Suspending computation - time of day
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>33</seqno>
 <body><![CDATA[
Sending scheduler request: Requested by project.
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>34</seqno>
 <body><![CDATA[
Requesting new tasks for NVIDIA GPU
]]></body>
 <time>1586722355</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>35</seqno>
 <body><![CDATA[
Scheduler request completed: got 0 new tasks
]]></body>
 <time>1586722356</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>36</seqno>
 <body><![CDATA[
No tasks sent
]]></body>
 <time>1586722356</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>37</seqno>
 <body><![CDATA[
This computer has reached a limit on tasks in progress
]]></body>
 <time>1586722356</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>38</seqno>
 <body><![CDATA[
Sending scheduler request: Requested by project.
]]></body>
 <time>1586725957</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>39</seqno>
 <body><![CDATA[
Requesting new tasks for NVIDIA GPU
]]></body>
 <time>1586725957</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>40</seqno>
 <body><![CDATA[
Scheduler request completed: got 0 new tasks
]]></body>
 <time>1586725958</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>41</seqno>
 <body><![CDATA[
No tasks sent
]]></body>
 <time>1586725958</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>42</seqno>
 <body><![CDATA[
This computer has reached a limit on tasks in progress
]]></body>
 <time>1586725958</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>43</seqno>
 <body><![CDATA[
Sending scheduler request: Requested by project.
]]></body>
 <time>1586729561</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>44</seqno>
 <body><![CDATA[
Requesting new tasks for NVIDIA GPU
]]></body>
 <time>1586729561</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>45</seqno>
 <body><![CDATA[
Scheduler request completed: got 0 new tasks
]]></body>
 <time>1586729626</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>46</seqno>
 <body><![CDATA[
No tasks sent
]]></body>
 <time>1586729626</time>
</msg>
<msg>
 <project>GPUGRID</project>
 <pri>1</pri>
 <seqno>47</seqno>
 <body><![CDATA[
This computer has reached a limit on tasks in progress
]]></body>
 <time>1586729626</time>
</msg>
</msgs>
</boinc_gui_rpc_reply>
"""

projects = """<boinc_gui_rpc_reply>
<projects>
<project>
    <master_url>https://csgrid.org/csg/</master_url>
    <project_name>Citizen Science Grid</project_name>
    <symstore></symstore>
    <user_name>Niels</user_name>
    <team_name></team_name>
    <host_venue></host_venue>
    <email_hash>5a8a8920f2c1e96a7d5cd75da2e6e501</email_hash>
    <cross_project_id>00529581a60054f9364959c0c0c331af</cross_project_id>
    <external_cpid>8980a1cd92ae44575caa46e5dc8cbadc</external_cpid>
    <cpid_time>1586709207.000000</cpid_time>
    <user_total_credit>0.000000</user_total_credit>
    <user_expavg_credit>0.000000</user_expavg_credit>
    <user_create_time>1586709207.000000</user_create_time>
    <rpc_seqno>0</rpc_seqno>
    <userid>563633</userid>
    <teamid>0</teamid>
    <hostid>110693</hostid>
    <host_total_credit>0.000000</host_total_credit>
    <host_expavg_credit>0.000000</host_expavg_credit>
    <host_create_time>1586709217.000000</host_create_time>
    <nrpc_failures>0</nrpc_failures>
    <master_fetch_failures>0</master_fetch_failures>
    <min_rpc_time>0.000000</min_rpc_time>
    <next_rpc_time>0.000000</next_rpc_time>
    <rec>0.000000</rec>
    <rec_time>0.000000</rec_time>
    <resource_share>100.000000</resource_share>
    <desired_disk_usage>0.000000</desired_disk_usage>
    <duration_correction_factor>1.000000</duration_correction_factor>
    <sched_rpc_pending>0</sched_rpc_pending>
    <send_time_stats_log>0</send_time_stats_log>
    <send_job_log>0</send_job_log>
    <njobs_success>0</njobs_success>
    <njobs_error>0</njobs_error>
    <elapsed_time>0.000000</elapsed_time>
    <last_rpc_time>1586709217.556251</last_rpc_time>
    <dont_use_dcf/>
    <rsc_backoff_time>
        <name>CPU</name>
        <value>0.000000</value>
    </rsc_backoff_time>
    <rsc_backoff_interval>
        <name>CPU</name>
        <value>0.000000</value>
    </rsc_backoff_interval>
    <rsc_backoff_time>
        <name>NVIDIA</name>
        <value>0.000000</value>
    </rsc_backoff_time>
    <rsc_backoff_interval>
        <name>NVIDIA</name>
        <value>0.000000</value>
    </rsc_backoff_interval>
    <no_rsc_apps>NVIDIA</no_rsc_apps>
<gui_urls>


    <gui_url>
        <name>Message boards</name>
        <description>Correspond with other users on the Citizen Science Grid message boards</description>
        <url>https://csgrid.org/csg/forum_index.php</url>
    </gui_url>
    <gui_url>
        <name>Your account</name>
        <description>View your account information</description>
        <url>https://csgrid.org/csg/home.php</url>
    </gui_url>
    <gui_url>
        <name>Your tasks</name>
        <description>View the last week or so of computational work</description>
        <url>https://csgrid.org/csg/results.php?userid=563633</url>
    </gui_url>
    
</gui_urls>
    <sched_priority>-0.000000</sched_priority>
    <project_files_downloaded_time>0.000000</project_files_downloaded_time>
    <project_dir>/var/lib/boinc/projects/csgrid.org_csg</project_dir>
</project>
<project>
    <master_url>http://www.gpugrid.net/</master_url>
    <project_name>GPUGRID</project_name>
    <symstore></symstore>
    <user_name>root</user_name>
    <team_name></team_name>
    <host_venue></host_venue>
    <email_hash>5a8a8920f2c1e96a7d5cd75da2e6e501</email_hash>
    <cross_project_id>645b24ccb81db535a8aabff1ee390c57</cross_project_id>
    <external_cpid></external_cpid>
    <cpid_time>1584633242.000000</cpid_time>
    <user_total_credit>280409.812500</user_total_credit>
    <user_expavg_credit>20978.467946</user_expavg_credit>
    <user_create_time>1584633242.000000</user_create_time>
    <rpc_seqno>94</rpc_seqno>
    <userid>554937</userid>
    <teamid>0</teamid>
    <hostid>539892</hostid>
    <host_total_credit>252078.375000</host_total_credit>
    <host_expavg_credit>20724.210140</host_expavg_credit>
    <host_create_time>1586432004.000000</host_create_time>
    <nrpc_failures>0</nrpc_failures>
    <master_fetch_failures>0</master_fetch_failures>
    <min_rpc_time>1586729657.140112</min_rpc_time>
    <next_rpc_time>1586733226.140112</next_rpc_time>
    <rec>15456.136497</rec>
    <rec_time>1586708317.245634</rec_time>
    <resource_share>100.000000</resource_share>
    <desired_disk_usage>0.000000</desired_disk_usage>
    <duration_correction_factor>0.655056</duration_correction_factor>
    <sched_rpc_pending>0</sched_rpc_pending>
    <send_time_stats_log>0</send_time_stats_log>
    <send_job_log>0</send_job_log>
    <njobs_success>16</njobs_success>
    <njobs_error>1</njobs_error>
    <elapsed_time>75265.865141</elapsed_time>
    <last_rpc_time>1586729626.140112</last_rpc_time>
    <rsc_backoff_time>
        <name>CPU</name>
        <value>0.000000</value>
    </rsc_backoff_time>
    <rsc_backoff_interval>
        <name>CPU</name>
        <value>0.000000</value>
    </rsc_backoff_interval>
    <rsc_backoff_time>
        <name>NVIDIA</name>
        <value>0.000000</value>
    </rsc_backoff_time>
    <rsc_backoff_interval>
        <name>NVIDIA</name>
        <value>0.000000</value>
    </rsc_backoff_interval>
<gui_urls>

    <gui_url>
        <name>Your account</name>
        <description>View your account information and credit totals</description>
        <url>http://www.gpugrid.net/show_user.php?userid=554937</url>
    </gui_url>
    
    <gui_url>
        <name>Your results</name>
        <description>Your recently completed tasks</description>
        <url>http://www.gpugrid.net/results.php?userid=554937</url>
    </gui_url>
    <gui_url>
        <name>Server state</name>
        <description>Status of GPUGRID's server</description>
        <url>http://www.gpugrid.net/server_status.php</url>
    </gui_url>
    <gui_url>
        <name>Science</name>
        <description>Small contributions, great causes.</description>
        <url>http://www.gpugrid.net/science.php</url>
    </gui_url>
    <gui_url>
        <name>Donate</name>
        <description>Thank you for considering a donation to GPUGRID</description>
        <url>http://www.gpugrid.net/gpugrid_donations.php</url>
    </gui_url>
    <gui_url>
        <name>Forum / Help</name>
        <description>Questions, support and discussions</description>
        <url>http://www.gpugrid.net/forum_index.php</url>
    </gui_url>
</gui_urls>
    <sched_priority>-2.099418</sched_priority>
    <project_files_downloaded_time>0.000000</project_files_downloaded_time>
    <project_dir>/var/lib/boinc/projects/www.gpugrid.net</project_dir>
</project>
</projects>
</boinc_gui_rpc_reply>
"""

results = """<boinc_gui_rpc_reply>
<results>
<result>
    <name>2ffeA01_379_3-TONI_MDADpr4sf-5-10-RND0805_0</name>
    <wu_name>2ffeA01_379_3-TONI_MDADpr4sf-5-10-RND0805</wu_name>
    <platform>x86_64-pc-linux-gnu</platform>
    <version_num>210</version_num>
    <plan_class>cuda100</plan_class>
    <project_url>http://www.gpugrid.net/</project_url>
    <final_cpu_time>2319.130000</final_cpu_time>
    <final_elapsed_time>2325.731392</final_elapsed_time>
    <exit_status>0</exit_status>
    <state>2</state>
    <report_deadline>1587130361.000000</report_deadline>
    <received_time>1586698361.771048</received_time>
    <estimated_cpu_time_remaining>3571.091666</estimated_cpu_time_remaining>
    <report_immediately/>
<active_task>
    <active_task_state>0</active_task_state>
    <app_version_num>210</app_version_num>
    <slot>0</slot>
    <pid>0</pid>
    <scheduler_state>1</scheduler_state>
    <checkpoint_cpu_time>2134.710000</checkpoint_cpu_time>
    <fraction_done>0.600000</fraction_done>
    <current_cpu_time>2134.710000</current_cpu_time>
    <elapsed_time>2137.328429</elapsed_time>
    <swap_size>9757118464.000000</swap_size>
    <working_set_size>347529216.000000</working_set_size>
    <working_set_size_smoothed>347529216.000000</working_set_size_smoothed>
    <page_fault_rate>0.000000</page_fault_rate>
    <bytes_sent>0.000000</bytes_sent>
    <bytes_received>0.000000</bytes_received>
   <progress_rate>0.000281</progress_rate>
</active_task>
    <resources>0.981 CPUs + 1 NVIDIA GPU</resources>
</result>
<result>
    <name>2dgmC03_379_4-TONI_MDADpr4sd-5-10-RND1588_0</name>
    <wu_name>2dgmC03_379_4-TONI_MDADpr4sd-5-10-RND1588</wu_name>
    <platform>x86_64-pc-linux-gnu</platform>
    <version_num>210</version_num>
    <plan_class>cuda100</plan_class>
    <project_url>http://www.gpugrid.net/</project_url>
    <final_cpu_time>0.000000</final_cpu_time>
    <final_elapsed_time>0.000000</final_elapsed_time>
    <exit_status>0</exit_status>
    <state>2</state>
    <report_deadline>1587133291.000000</report_deadline>
    <received_time>1586701291.917992</received_time>
    <estimated_cpu_time_remaining>8927.729164</estimated_cpu_time_remaining>
    <report_immediately/>
    <resources>0.981 CPUs + 1 NVIDIA GPU</resources>
</result>
</results>
</boinc_gui_rpc_reply>
"""

