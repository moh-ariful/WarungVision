# utils.py
from datetime import datetime, timezone, timedelta
# Timezone Indonesia (WIB, UTC+7)
WIB = timezone(timedelta(hours=7))

def now_local_str() -> str:
    """
    Mengembalikan waktu sekarang dalam format string,
    menggunakan zona waktu WIB (UTC+7).
    Contoh: 2025-12-01 10:25:30 WIB
    """
    return datetime.now(WIB).strftime("%Y-%m-%d %H:%M:%S WIB")


def today_id_date_str() -> str:
    """
    Mengembalikan TANGGAL HARI INI dalam format Indonesia:
    DD/MM/YYYY, misal: 01/12/2025
    Fungsi ini dipakai untuk memberi konteks ke model
    agar tidak salah menganggap tanggal hari ini sebagai 'masa depan'.
    """
    return datetime.now(WIB).strftime("%d/%m/%Y")
