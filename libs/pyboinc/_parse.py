from ._tag import Tag
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta

INTEGER_TAG = {
    Tag.MAJOR,
    Tag.MINOR,
    Tag.RELEASE,
    Tag.NETWORK_STATUS,
    Tag.AMS_PASSWORD_ERROR,
    Tag.TASK_SUSPEND_REASON,
    Tag.TASK_MODE,
    Tag.TASK_MODE_PERM,
    Tag.GPU_SUSPEND_REASON,
    Tag.GPU_MODE_PERM,
    Tag.NETWORK_SUSPEND_REASON,
    Tag.NETWORK_MODE,
    Tag.NETWORK_MODE_PERM,
    Tag.MAX_EVENT_LOG_LINES,
    Tag.SEQNO,
    Tag.PRI,
    Tag.RPC_SEQNO,
    Tag.USERID,
    Tag.TEAMID,
    Tag.HOSTID,
    Tag.NRPC_FAILURES,
    Tag.MASTER_FETCH_FAILURES,
    Tag.NJOBS_SUCCESS,
    Tag.NJOBS_ERROR,
    Tag.VERSION_NUM,
    Tag.EXIT_STATUS,
    Tag.STATE,
    Tag.ACTIVE_TASK_STATE,
    Tag.APP_VERSION_NUM,
    Tag.SLOT,
    Tag.PID,
    Tag.SCHEDULER_STATE,
    Tag.P_NCPUS,
    Tag.COUNT,
    Tag.VENDOR_ID,
    Tag.HALF_FP_CONFIG,
    Tag.SINGLE_FP_CONFIG,
    Tag.DOUBLE_FP_CONFIG,
    Tag.EXECUTION_CAPABILITIES,
    Tag.GLOBAL_MEM_SIZE,
    Tag.LOCAL_MEM_SIZE,
    Tag.MAX_CLOCK_FREQUENCY,
    Tag.MAX_COMPUTE_UNITS,
    Tag.NV_COMPUTE_CAPABILITY_MAJOR,
    Tag.NV_COMPUTE_CAPABILITY_MINOR,
    Tag.AMD_SIMD_INSTRUCTION_WIDTH,
    Tag.AMD_SIMD_PER_COMPUTE_UNIT,
    Tag.AMD_SIMD_WIDTH,
    Tag.NUM_RETRIES,
}

FLOAT_TAG = {
    Tag.TASK_MODE_DELAY,
    Tag.GPU_MODE_DELAY,
    Tag.NETWORK_MODE_DELAY,
    Tag.DISK_USAGE,
    Tag.D_TOTAL,
    Tag.D_FREE,
    Tag.D_BOINC,
    Tag.D_ALLOWED,
    Tag.USER_TOTAL_CREDIT,
    Tag.USER_EXPAVG_CREDIT,
    Tag.HOST_TOTAL_CREDIT,
    Tag.HOST_EXPAVG_CREDIT,
    Tag.REC,
    Tag.RESOURCE_SHARE,
    Tag.DESIRED_DISK_USAGE,
    Tag.DURATION_CORRECTION_FACTOR,
    Tag.FRACTION_DONE,
    Tag.SWAP_SIZE,
    Tag.WORKING_SET_SIZE,
    Tag.WORKING_SET_SIZE_SMOOTHED,
    Tag.PAGE_FAULT_RATE,
    Tag.BYTES_SENT,
    Tag.BYTES_RECEIVED,
    Tag.PROGRESS_RATE,
    Tag.P_FPOPS,
    Tag.P_IOPS,
    Tag.P_MEMBW,
    Tag.P_CALCULATED,
    Tag.M_NBYTES,
    Tag.M_CACHE,
    Tag.M_SWAP,
    Tag.D_TOTAL,
    Tag.D_FREE,
    Tag.PEAK_FLOPS,
    Tag.XFER_SPEED,
}

BOOL_TAG = {
    Tag.DISALLOW_ATTACH,
    Tag.SIMPLE_GUI_ONLY,
    Tag.SCHED_RPC_PENDING,
    Tag.SEND_TIME_STATS_LOG,
    Tag.SEND_JOB_LOG,
    Tag.P_VM_EXTENSIONS_DISABLED,
    Tag.HAVE_OPENCL,
    Tag.AVAILABLE,
    Tag.ENDIAN_LITTLE,
    Tag.IS_UPLOAD,
}

LIST_TAG = {
    Tag.MSGS,
    Tag.RESULTS,
    Tag.PROJECTS,
    Tag.GUI_URLS,
    Tag.FILE_TRANSFERS,
    Tag.COPROCS,
}

TIMEDELTA_TAG = {
    Tag.ELAPSED_TIME,
    Tag.FINAL_CPU_TIME,
    Tag.FINAL_ELAPSED_TIME,
    Tag.ESTIMATED_CPU_TIME_REMAINING,
    Tag.CHECKPOINT_CPU_TIME,
    Tag.CURRENT_CPU_TIME,
    Tag.ELAPSED_TIME,
    Tag.TIME_SO_FAR,
}

TIME_TAG = {
    Tag.TIME,
    Tag.CPID_TIME,
    Tag.USER_CREATE_TIME,
    Tag.HOST_CREATE_TIME,
    Tag.MIN_RPC_TIME,
    Tag.NEXT_RPC_TIME,
    Tag.REC_TIME,
    Tag.LAST_RPC_TIME,
    Tag.REPORT_DEADLINE,
    Tag.RECEIVED_TIME,
    Tag.FIRST_REQUEST_TIME,
    Tag.NEXT_REQUEST_TIME,
}

TAG_PARSER = {
    Tag.BODY: lambda x: x.replace("<![CDATA[", "").replace("]]>", "").strip(),
    Tag.PROJECT_URL: lambda x: Project(master_url=x)
}
INTEGER_TAG_PARSER = int
FLOAT_TAG_PARSER = float
TIME_TAG_PARSER = lambda x: datetime.fromtimestamp(float(x))
TIMEDELTA_TAG_PARSER = lambda x: timedelta(seconds=float(x))
BOOL_TAG_PARSER = bool
for parser_func, tags in [
    (INTEGER_TAG_PARSER, INTEGER_TAG),
    (FLOAT_TAG_PARSER, FLOAT_TAG),
    (TIME_TAG_PARSER, TIME_TAG),
    (TIMEDELTA_TAG_PARSER, TIMEDELTA_TAG),
    (BOOL_TAG_PARSER, BOOL_TAG),
]:
    TAG_PARSER.update((tag, parser_func) for tag in tags)


def parse_generic(e: ET.Element):
    if len(e) > 0:
        if e.tag in LIST_TAG:
            return [parse_generic(cc) for cc in e]
        else:
            # recurse on elements with children
            return dict((c.tag, parse_generic(c)) for c in e)
    elif e.text is not None:
        # set parsed value if available
        return TAG_PARSER.get(e.tag, str)(e.text)
    else:
        # self closing
        return True


class Project:
    master_url: str

    def __init__(self, *args, **kwargs):
        self.__dict__ = kwargs

    def __eq__(self, other):
        return str(other) == str(self)

    def __repr__(self):
        return "<Project {}, {}>".format(self.master_url, self.__dict__)

    def __str__(self):
        return self.master_url
