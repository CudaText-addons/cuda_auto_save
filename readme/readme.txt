plugin for CudaText.
automatically saves modified files. currently: only named tabs (ignores untitled tabs).
it has config file with few options, call it by menu "Options / Settings-plugins / Auto Save".
options:

- save_interval: interval of timer which auto-saves files, in seconds. default: 30. to disable saving by timer, just set some huge value like 1000000.
- save_before_closing_tab: boolean, 0 or 1: enables to auto-save files on tab closing (without any confirmation).

author: Alexey (CudaText)
license: MIT
