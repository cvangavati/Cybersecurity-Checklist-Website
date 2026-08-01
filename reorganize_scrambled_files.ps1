$ErrorActionPreference = 'Stop'
$repo = 'c:\Users\cvang\OneDrive\Documents\GitHub\Cybersecurity-Checklist-Website'
$phishing = Join-Path $repo 'Phishing'
$security = Join-Path $repo 'SecurityPipeline'

New-Item -ItemType Directory -Path (Join-Path $phishing 'src'), (Join-Path $phishing 'content'), (Join-Path $phishing 'stores'), (Join-Path $phishing '__tests__'), (Join-Path $security 'scripts'), (Join-Path $security '__tests__'), (Join-Path $security '__fixtures__'), (Join-Path $security '.github/workflows') -Force | Out-Null

$moves = @(
  @{ Source = 'AwarenessBanner.module (3).css'; Destination = Join-Path $phishing 'src/AwarenessBanner.module.css' },
  @{ Source = 'AwarenessModal (3).jsx'; Destination = Join-Path $phishing 'src/AwarenessModal.jsx' },
  @{ Source = 'AwarenessProvider (3).jsx'; Destination = Join-Path $phishing 'src/AwarenessProvider.jsx' },
  @{ Source = 'backend.test (3).js'; Destination = Join-Path $phishing '__tests__/backend.test.js' },
  @{ Source = 'content.test (1).js'; Destination = Join-Path $phishing '__tests__/content.test.js' },
  @{ Source = 'en (3).json'; Destination = Join-Path $phishing 'content/en.json' },
  @{ Source = 'es (3).json'; Destination = Join-Path $phishing 'content/es.json' },
  @{ Source = 'frontend.test (3).jsx'; Destination = Join-Path $phishing '__tests__/frontend.test.jsx' },
  @{ Source = 'messageStateStore (3).js'; Destination = Join-Path $phishing 'stores/messageStateStore.js' },
  @{ Source = 'messagingConfig (3).js'; Destination = Join-Path $phishing 'messagingConfig.js' },
  @{ Source = 'README (9) (1).md'; Destination = Join-Path $phishing 'README.md' },
  @{ Source = 'README (3) (1).md'; Destination = Join-Path $phishing 'src/AwarenessBanner.jsx' },
  @{ Source = 'README (1).md'; Destination = Join-Path $phishing '.gitignore' },
  @{ Source = 'ReportPhishingForm (1).jsx'; Destination = Join-Path $phishing 'src/ReportPhishingForm.jsx' },
  @{ Source = 'ReportPhishingForm.module (3).css'; Destination = Join-Path $phishing 'src/ReportPhishingForm.module.css' },
  @{ Source = 'reportStore (1).js'; Destination = Join-Path $phishing 'stores/reportStore.js' },
  @{ Source = 'selectNextMessage (3).js'; Destination = Join-Path $phishing 'selectNextMessage.js' },
  @{ Source = 'server (3).js'; Destination = Join-Path $phishing 'server.js' },
  @{ Source = 'useAwareness (3).js'; Destination = Join-Path $phishing 'src/useAwareness.js' },
  @{ Source = 'actionLabels (1).js'; Destination = Join-Path $phishing 'package.json' },
  @{ Source = 'consolidate (1).js'; Destination = Join-Path $security 'consolidate.js' },
  @{ Source = 'generate-sbom (1).sh'; Destination = Join-Path $security 'scripts/generate-sbom.sh' },
  @{ Source = 'run-security-scan (1).sh'; Destination = Join-Path $security 'scripts/run-security-scan.sh' },
  @{ Source = 'security (1).yml'; Destination = Join-Path $security '.github/workflows/security.yml' },
  @{ Source = 'README (7) (1).md'; Destination = Join-Path $security '__tests__/consolidate.test.js' },
  @{ Source = 'package-lock (1).json'; Destination = Join-Path $security 'suppressions.json' }
)

foreach ($move in $moves) {
  $sourcePath = Join-Path $phishing $move.Source
  if (-not (Test-Path $sourcePath)) {
    continue
  }
  $destinationPath = $move.Destination
  if (Test-Path $destinationPath) {
    Write-Host "Skipping existing target: $destinationPath"
    continue
  }
  New-Item -ItemType Directory -Path ([System.IO.Path]::GetDirectoryName($destinationPath)) -Force | Out-Null
  Move-Item -Path $sourcePath -Destination $destinationPath -Force
  Write-Host "Moved $($move.Source) -> $destinationPath"
}
