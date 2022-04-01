Plugin for CudaText.
"Auto Save" automatically saves modified documents.
Now it saves also untitled documents (by option).

Plugin options
--------------

You can access options using menu: "Options / Settings-plugins / Auto Save / Config"

- "save_interval_seconds" (number, default: 30)
  interval of timer which auto-saves files, in seconds.
  to disable auto-saving by timer, set to 0.

- "save_max_MB_file_size" (number, default: 5)
  used only if "save_session" is 0.
  max size in MB where plugin will proceed with auto-saving.
  to auto-save regardless the file size, set to 0.

- "save_before_closing_tab" (0 or 1, default: 0)
  enables to auto-save file just before its closing (without any confirmation).

- "on_deactivate" (0 or 1, default: 0)
  enables to auto-save when CudaText looses focus.

- "save_on_tab_change" (0 or 1, default: 0)
  enables to auto-save file after changing active tab.

- "save_session" (0 or 1, default: 1)
  if 1: plugin saves the entire current session (includes saving of untitled
  documents by default, directly to the session JSON file).
  if 0: plugin uses the 'old' method, without session, it saves only named
  modified documents to their files.

- "session_flags" (string, has several option-chars, default: empty)
  option is used when "save_session" is 1.
  option works only under CudaText 1.153.1+.
  if has char 'n': don't save modified named files to the session.
  if has char 'u': don't save untitled documents to the session.

- "not_save_tmpdir" (0 or 1, default: 0)
  if 0: files in tmp-dir are saved
  if 1: files in tmp-dir are not saved

About
-----

Authors:
  Alexey Torgashin (CudaText)
  Jairo Martinez Antonio, https://github.com/JairoMartinezA
License: MIT
