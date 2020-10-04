plugin for CudaText.
automatically saves modified files. currently: only named tabs (ignores untitled tabs).
it has config file with few options, call it by menu "Options / Settings-plugins / Auto Save".

options:
- "save_interval" (number, default: 30)
  interval of timer which auto-saves files, in seconds. 
  to disable auto-saving by timer, set to 0.

- "save_before_closing_tab" (0 or 1, default: 0)
  enables to auto-save file just before its closing (without any confirmation).

- "on_deactivate" (0 or 1, default: 0)
  enables to auto-save when CudaText looses focus.
  requires CudaText 1.114+.

author: Alexey Torgashin (CudaText)
license: MIT
