[Setup]
AppName=CSV Merger
AppVersion=1.0
DefaultDirName={autopf}\CSV Merger
DefaultGroupName=CSV Merger
OutputBaseFilename=CSV_Merger_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\dist\CSV Merger\CSV Merger.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\CSV Merger\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\batch_configs.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\settings.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\recent_merges.json"; DestDir: "{app}"; Flags: ignoreversion

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Icons]
Name: "{group}\CSV Merger"; Filename: "{app}\CSV Merger.exe"
Name: "{autodesktop}\CSV Merger"; Filename: "{app}\CSV Merger.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CSV Merger.exe"; Description: "Launch CSV Merger"; Flags: nowait postinstall skipifsilent
