' Brain Quest - Silent Launcher
' This script starts the server silently and opens the browser

Dim objShell, objFSO, strBatFile, strPath

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

strPath = "c:\Users\vrajp\CodeFolder\Fun-Projects\Math-Tricks"
strBatFile = strPath & "\run_app.bat"

' Check if batch file exists
If Not objFSO.FileExists(strBatFile) Then
    MsgBox "Error: run_app.bat not found!", 16, "Brain Quest"
    WScript.Quit
End If

' Run batch file silently
objShell.Run strBatFile, 0, False

' Small delay, then show message
WScript.Sleep 1000
objShell.Popup "Brain Quest is starting...", 2, "Brain Quest", 64
