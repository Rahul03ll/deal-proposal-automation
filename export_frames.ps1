Add-Type -AssemblyName System.Drawing

$brainDir = "C:\Users\KIIT\.gemini\antigravity\brain\9c77df73-1e61-457c-ba52-ded39d2152c9"
$scratchDir = "C:\Users\KIIT\.gemini\antigravity\scratch\deal_proposal_automation"
$framesDir = "$scratchDir\raw_frames"
if (-not (Test-Path $framesDir)) { New-Item -ItemType Directory -Path $framesDir }

$images = @(
    "$brainDir\sheet_tracker_view_1789486920181.jpg",
    "$brainDir\editor_code_view_1789486980332.jpg",
    "$brainDir\terminal_run_view_1789487031031.jpg",
    "$brainDir\proposal_sow_doc_1789487194826.jpg"
)

$targetW = 800
$targetH = 450

for ($i = 0; $i -lt $images.Count; $i++) {
    $srcPath = $images[$i]
    if (Test-Path $srcPath) {
        $bmpSrc = [System.Drawing.Image]::FromFile($srcPath)
        $bmpDst = New-Object System.Drawing.Bitmap $targetW, $targetH
        $g = [System.Drawing.Graphics]::FromImage($bmpDst)
        $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.DrawImage($bmpSrc, 0, 0, $targetW, $targetH)
        $g.Dispose()
        $bmpSrc.Dispose()

        $outPath = "$framesDir\frame_$i.bmp"
        $bmpDst.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Bmp)
        $bmpDst.Dispose()
        Write-Host "Exported: $outPath"
    }
}
