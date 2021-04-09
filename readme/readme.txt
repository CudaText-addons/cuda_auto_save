Plugin for CudaText.

"Auto Save" automatically saves modified files, it works only with named tabs
ignoring untitled tabs.

Plugin options
--------------

You can access to options using "Options / Settings-plugins / Auto Save / Config"

- "save_interval_seconds" (number, default: 30)
  interval of timer which auto-saves files, in seconds.
  to disable auto-saving by timer, set to 0.

- "save_max_MB_file_size" (number, default: 5)
  max size in MB where plugin will proceed with auto-saving.
  to auto-save regardless the file size, set to 0.

- "save_before_closing_tab" (0 or 1, default: 0)
  enables to auto-save file just before its closing (without any confirmation).

- "on_deactivate" (0 or 1, default: 0)
  enables to auto-save when CudaText looses focus.
  requires CudaText 1.114+.

- "save_on_tab_change" (0 or 1, default: 0)
  enables to auto-save file after changing active tab.

About
-----

Author:       Alexey Torgashin (CudaText)
Contributors:
              @JairoMartinezA (at GitHub)
License:      MIT
