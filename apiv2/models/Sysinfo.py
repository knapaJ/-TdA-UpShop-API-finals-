import platform
import psutil
from datetime import datetime


class SystemInfo:
    @property
    def cpu_load(self) -> float:
        """avg load on last five minutes"""
        return psutil.getloadavg()[1]

    @property
    def ram_usage(self) -> float:
        return psutil.virtual_memory().percent

    @property
    def disk_usage(self) -> float:
        return psutil.disk_usage('/').percent

    @property
    def boot_time(self) -> datetime:
        return datetime.fromtimestamp(psutil.boot_time())

    @property
    def platform(self) -> str:
        return platform.platform()
