"""Record the machine profile for the paper's compute-environment section. stdlib only; Windows + Linux.
  python scripts/profile_machine.py > results/machine_profile.json
"""
import json, os, platform, sys


def ram_gb():
    try:
        if os.name == "nt":
            import ctypes

            class MS(ctypes.Structure):
                _fields_ = [("l", ctypes.c_ulong), ("m", ctypes.c_ulong), ("tp", ctypes.c_ulonglong), ("ap", ctypes.c_ulonglong),
                            ("tpf", ctypes.c_ulonglong), ("apf", ctypes.c_ulonglong), ("tv", ctypes.c_ulonglong), ("av", ctypes.c_ulonglong),
                            ("ae", ctypes.c_ulonglong)]
            s = MS(); s.l = ctypes.sizeof(MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s))
            return round(s.tp / 2**30, 1)
        with open("/proc/meminfo") as f:
            return round(int(f.readline().split()[1]) / 2**20, 1)
    except Exception:
        return None


print(json.dumps({"os": platform.platform(), "machine": platform.machine(), "processor": platform.processor(),
                  "logical_cpus": os.cpu_count(), "ram_gb": ram_gb(), "python": sys.version.split()[0]}, indent=2))
