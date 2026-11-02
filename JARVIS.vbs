Set WshShell = CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strPath
WshShell.Run """" & strPath & "\.venv\Scripts\python.exe"" """ & strPath & "\launch_jarvis.py""", 1, False
