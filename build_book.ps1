$ErrorActionPreference = 'Stop'

$candidates = @(
    (Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'),
    'python3',
    'python'
)

$runtime = $null
$versionCheck = @'
import sys
import PIL
import pypdf
import reportlab
expected = ('12.3.0', '6.10.0', '4.4.9')
actual = (PIL.__version__, pypdf.__version__, reportlab.Version)
sys.exit(0 if actual == expected else 1)
'@
foreach ($candidate in $candidates) {
    try {
        & $candidate -c $versionCheck 2>$null
        if ($LASTEXITCODE -eq 0) {
            $runtime = $candidate
            break
        }
    }
    catch [System.Management.Automation.CommandNotFoundException] {
        continue
    }
}

if ($null -eq $runtime) {
    throw 'Python with Pillow 12.3.0, pypdf 6.10.0, and ReportLab 4.4.9 is required.'
}

& $runtime (Join-Path $PSScriptRoot 'build_book.py')
exit $LASTEXITCODE
