plugin for CudaText.
automatically saves modified files. currently: only named tabs (ignores untitled tabs).
it has config file with few options, call it by menu "Options / Settings-plugins / Auto Save".
options:

- save_interval
  interval of timer which auto-saves files, in seconds. default: 30. 
  to disable saving by timer, set to 0.

- save_before_closing_tab
  0 or 1, default is 0 (off): enables to auto-save on tab closing (without any confirmation).

author: Alexey (CudaText)
license: MIT
