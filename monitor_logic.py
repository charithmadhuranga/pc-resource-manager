import psutil
import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class SystemMonitor:
    def __init__(self):
        self._prev_net_io = None
        self._prev_disk_io = None
        self._prev_timestamp = None

    def get_cpu_usage_per_core(self) -> List[float]:
        try:
            return psutil.cpu_percent(interval=0.1, percpu=True)
        except Exception:
            return []

    def get_cpu_usage_overall(self) -> float:
        try:
            return psutil.cpu_percent(interval=0.1)
        except Exception:
            return 0.0

    def get_cpu_freq(self) -> Dict[str, Any]:
        try:
            freq = psutil.cpu_freq()
            if freq:
                return {"current": freq.current, "min": freq.min, "max": freq.max}
        except Exception:
            pass
        return {"current": 0, "min": 0, "max": 0}

    def get_ram_usage(self) -> Dict[str, Any]:
        try:
            mem = psutil.virtual_memory()
            return {
                "total": mem.total,
                "available": mem.available,
                "used": mem.used,
                "percent": mem.percent,
            }
        except Exception:
            return {"total": 0, "available": 0, "used": 0, "percent": 0}

    def get_swap_memory(self) -> Dict[str, Any]:
        try:
            swap = psutil.swap_memory()
            return {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent,
            }
        except Exception:
            return {"total": 0, "used": 0, "free": 0, "percent": 0}

    def get_disk_usage(self, path: str = "/") -> Dict[str, Any]:
        try:
            disk = psutil.disk_usage(path)
            return {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            }
        except Exception:
            return {"total": 0, "used": 0, "free": 0, "percent": 0}

    def get_all_disks(self) -> List[Dict[str, Any]]:
        disks = []
        try:
            partitions = psutil.disk_partitions()
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append(
                        {
                            "device": partition.device,
                            "mountpoint": partition.mountpoint,
                            "fstype": partition.fstype,
                            "total": usage.total,
                            "used": usage.used,
                            "free": usage.free,
                            "percent": usage.percent,
                        }
                    )
                except Exception:
                    continue
        except Exception:
            pass
        return disks

    def get_disk_io_stats(self) -> Dict[str, Any]:
        try:
            current_time = datetime.now().timestamp()
            io = psutil.disk_io_counters()

            if io is None:
                return {
                    "read_count": 0,
                    "write_count": 0,
                    "read_bytes": 0,
                    "write_bytes": 0,
                    "read_speed": 0,
                    "write_speed": 0,
                }

            if self._prev_disk_io and self._prev_timestamp:
                time_diff = current_time - self._prev_timestamp
                if time_diff > 0:
                    read_speed = (
                        io.read_bytes - self._prev_disk_io["read_bytes"]
                    ) / time_diff
                    write_speed = (
                        io.write_bytes - self._prev_disk_io["write_bytes"]
                    ) / time_diff
                else:
                    read_speed = 0
                    write_speed = 0
            else:
                read_speed = 0
                write_speed = 0

            self._prev_disk_io = {
                "read_bytes": io.read_bytes,
                "write_bytes": io.write_bytes,
            }
            self._prev_timestamp = current_time

            return {
                "read_count": io.read_count,
                "write_count": io.write_count,
                "read_bytes": io.read_bytes,
                "write_bytes": io.write_bytes,
                "read_speed": read_speed,
                "write_speed": write_speed,
            }
        except Exception:
            return {
                "read_count": 0,
                "write_count": 0,
                "read_bytes": 0,
                "write_bytes": 0,
                "read_speed": 0,
                "write_speed": 0,
            }

    def get_network_io(self) -> Dict[str, Any]:
        try:
            current_time = datetime.now().timestamp()
            net_io = psutil.net_io_counters()

            if self._prev_net_io and self._prev_timestamp:
                time_diff = current_time - self._prev_timestamp
                if time_diff > 0:
                    sent_speed = (
                        net_io.bytes_sent - self._prev_net_io["bytes_sent"]
                    ) / time_diff
                    recv_speed = (
                        net_io.bytes_recv - self._prev_net_io["bytes_recv"]
                    ) / time_diff
                else:
                    sent_speed = 0
                    recv_speed = 0
            else:
                sent_speed = 0
                recv_speed = 0

            self._prev_net_io = {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
            }
            self._prev_timestamp = current_time

            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "sent_speed": sent_speed,
                "recv_speed": recv_speed,
            }
        except Exception:
            return {
                "bytes_sent": 0,
                "bytes_recv": 0,
                "packets_sent": 0,
                "packets_recv": 0,
                "sent_speed": 0,
                "recv_speed": 0,
            }

    def get_process_list(
        self, sort_by: str = "cpu", limit: int = 100
    ) -> List[Dict[str, Any]]:
        processes = []
        try:
            for proc in psutil.process_iter(
                ["pid", "name", "username", "cpu_percent", "memory_percent", "status"]
            ):
                try:
                    info = proc.info
                    processes.append(
                        {
                            "pid": info.get("pid", 0),
                            "name": info.get("name", "Unknown"),
                            "username": info.get("username", "Unknown"),
                            "cpu_percent": info.get("cpu_percent", 0) or 0,
                            "memory_percent": info.get("memory_percent", 0) or 0,
                            "status": info.get("status", "unknown"),
                        }
                    )
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    continue
        except Exception:
            pass

        if sort_by == "cpu":
            processes.sort(key=lambda x: x["cpu_percent"], reverse=True)
        elif sort_by == "memory":
            processes.sort(key=lambda x: x["memory_percent"], reverse=True)
        elif sort_by == "name":
            processes.sort(key=lambda x: x["name"].lower())
        elif sort_by == "pid":
            processes.sort(key=lambda x: x["pid"])

        return processes[:limit]

    def get_process_details(self, pid: int) -> Optional[Dict[str, Any]]:
        try:
            proc = psutil.Process(pid)
            with proc.oneshot():
                return {
                    "pid": proc.pid,
                    "name": proc.name(),
                    "username": proc.username(),
                    "status": proc.status(),
                    "cpu_percent": proc.cpu_percent(),
                    "memory_percent": proc.memory_percent(),
                    "memory_info": proc.memory_info()._asdict(),
                    "cpu_times": proc.cpu_times()._asdict(),
                    "num_threads": proc.num_threads(),
                    "create_time": proc.create_time(),
                    "cmdline": proc.cmdline(),
                    "exe": proc.exe(),
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
        except Exception:
            return None

    def kill_process(self, pid: int) -> bool:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False
        except Exception:
            return False

    def kill_process_force(self, pid: int) -> bool:
        try:
            proc = psutil.Process(pid)
            proc.kill()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False
        except Exception:
            return False

    def get_system_info(self) -> Dict[str, Any]:
        try:
            boot_time = psutil.boot_time()
            return {
                "platform": os.name,
                "os": os.uname().sysname if hasattr(os, "uname") else "Unknown",
                "release": os.uname().release if hasattr(os, "uname") else "Unknown",
                "version": os.uname().version if hasattr(os, "uname") else "Unknown",
                "machine": os.uname().machine if hasattr(os, "uname") else "Unknown",
                "boot_time": boot_time,
                "cpu_count": psutil.cpu_count(logical=True),
                "cpu_count_physical": psutil.cpu_count(logical=False),
                "total_memory": psutil.virtual_memory().total,
            }
        except Exception:
            return {
                "platform": os.name,
                "os": "Unknown",
                "release": "Unknown",
                "version": "Unknown",
                "machine": "Unknown",
                "boot_time": 0,
                "cpu_count": 0,
                "cpu_count_physical": 0,
                "total_memory": 0,
            }

    def get_battery_info(self) -> Optional[Dict[str, Any]]:
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    " secs_left": battery.secsleft,
                    "power_plugged": battery.power_plugged,
                }
        except Exception:
            pass
        return None
