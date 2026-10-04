param([string]$KnownHwnds = "")
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class WinMsg {
    [DllImport("user32.dll")]
    public static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
}
"@
$known = @()
if ($KnownHwnds -ne "") { $known = $KnownHwnds.Split(",") | ForEach-Object { $_.Trim() } }
$closed = @()
for ($i = 0; $i -lt 3; $i++) {
    $targets = Get-Process msedge -ErrorAction SilentlyContinue | Where-Object {
        $_.MainWindowHandle -ne 0 -and ($known -notcontains "$($_.MainWindowHandle)") -and
        ($_.MainWindowTitle -like "*Example*" -or $_.MainWindowTitle -like "*New tab*")
    }
    foreach ($t in $targets) {
        [WinMsg]::PostMessage($t.MainWindowHandle, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null
        $closed += "$($t.MainWindowHandle):$($t.MainWindowTitle)"
    }
    if ($closed.Count -gt 0) { break }
    Start-Sleep -Seconds 4
}
Write-Output ("CLOSED=" + ($closed -join " | "))
