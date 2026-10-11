"""Android system bar handling for edge-to-edge Android 15+.

Apps targeting API 35+ are forced to draw edge-to-edge, so Kivy's window
covers the status and navigation bars. The top app bar then sits underneath the
clock and its buttons stop receiving touches, and the navigation bar overlaps
the bottom of a game board.

``hide_system_bars`` requests immersive mode (both bars hidden, revealed
transiently by a swipe) so the app fills the screen like other games.
``system_bar_insets`` reads the remaining insets as a fallback, allowing the
content to be padded below any system bar that stays visible.
"""


def hide_system_bars(platform_name):
    """Hide the status and navigation bars on Android (no-op elsewhere)."""
    if platform_name != "android":
        return

    try:
        from android.runnable import run_on_ui_thread
        from jnius import autoclass
    except Exception:
        return

    @run_on_ui_thread
    def _hide():
        try:
            activity = autoclass("org.kivy.android.PythonActivity").mActivity
            window = activity.getWindow()
            version = autoclass("android.os.Build$VERSION")
            if version.SDK_INT >= 30:
                controller = window.getInsetsController()
                if controller is None:
                    return
                types = autoclass("android.view.WindowInsets$Type")
                behavior = autoclass("android.view.WindowInsetsController")
                controller.hide(types.systemBars())
                controller.setSystemBarsBehavior(
                    behavior.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
                )
            else:
                view = autoclass("android.view.View")
                decor = window.getDecorView()
                decor.setSystemUiVisibility(
                    view.SYSTEM_UI_FLAG_LAYOUT_STABLE
                    | view.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                    | view.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                    | view.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    | view.SYSTEM_UI_FLAG_FULLSCREEN
                    | view.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                )
        except Exception:
            pass

    _hide()


def system_bar_insets(platform_name):
    """Return the (top, bottom) system bar heights in physical pixels.

    Returns ``(0, 0)`` on every non-Android platform and whenever the insets
    cannot be read, so desktop rendering is never affected.
    """
    if platform_name != "android":
        return (0, 0)

    try:
        from jnius import autoclass

        activity = autoclass("org.kivy.android.PythonActivity").mActivity
        decor = activity.getWindow().getDecorView()
        insets = decor.getRootWindowInsets()
        if insets is None:
            return (0, 0)

        version = autoclass("android.os.Build$VERSION")
        if version.SDK_INT >= 30:
            inset_type = autoclass("android.view.WindowInsets$Type")
            bars = insets.getInsets(inset_type.systemBars())
            return (int(bars.top), int(bars.bottom))
        return (
            int(insets.getSystemWindowInsetTop()),
            int(insets.getSystemWindowInsetBottom()),
        )
    except Exception:
        return (0, 0)
