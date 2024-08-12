[Setup]
AppName=Payments
AppVersion=1.0
DefaultDirName={pf}\Payments
DefaultGroupName=Payments
OutputBaseFilename=PaymentsInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Payments.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "static\images\*"; DestDir: "{app}\static\images"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "db\my_database.db"; DestDir: "{app}\db"; Flags: ignoreversion  # Inclure la base de données

[Icons]
Name: "{group}\Payments"; Filename: "{app}\Payments.exe"
Name: "{userdesktop}\Payments"; Filename: "{app}\Payments.exe"

[Run]
Filename: "{app}\Payments.exe"; Description: "{cm:LaunchProgram,Payments}"; Flags: nowait postinstall skipifsilent