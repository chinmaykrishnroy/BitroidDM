import sys


def enable_native_window_shadow(window) -> bool:
    if sys.platform != "win32":
        return False

    try:
        import ctypes
        from ctypes import wintypes

        class Margins(ctypes.Structure):
            _fields_ = [
                ("cxLeftWidth", ctypes.c_int),
                ("cxRightWidth", ctypes.c_int),
                ("cyTopHeight", ctypes.c_int),
                ("cyBottomHeight", ctypes.c_int),
            ]

        hwnd = wintypes.HWND(int(window.winId()))
        dwm = ctypes.windll.dwmapi

        DWMWA_NCRENDERING_POLICY = 2
        DWMNCRP_ENABLED = 2
        policy = ctypes.c_int(DWMNCRP_ENABLED)
        dwm.DwmSetWindowAttribute(
            hwnd,
            ctypes.c_int(DWMWA_NCRENDERING_POLICY),
            ctypes.byref(policy),
            ctypes.sizeof(policy),
        )

        # A 1px frame is enough for DWM to keep native shadow behavior while
        # the visible titlebar/buttons remain fully client-rendered by Qt.
        margins = Margins(1, 1, 1, 1)
        dwm.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))

        # Rounded corners are Windows 11 only; older builds simply ignore this.
        DWMWA_WINDOW_CORNER_PREFERENCE = 33
        DWMWCP_ROUND = 2
        corner_preference = ctypes.c_int(DWMWCP_ROUND)
        dwm.DwmSetWindowAttribute(
            hwnd,
            ctypes.c_int(DWMWA_WINDOW_CORNER_PREFERENCE),
            ctypes.byref(corner_preference),
            ctypes.sizeof(corner_preference),
        )

        return True
    except Exception:
        return False
