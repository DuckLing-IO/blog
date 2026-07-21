$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$python = "D:\Miniconda3\python.exe"
$pyinstaller = "D:\Miniconda3\Scripts\pyinstaller.exe"

if (-not (Test-Path $python)) {
    throw "未找到 Python：$python"
}
if (-not (Test-Path $pyinstaller)) {
    throw "未找到 PyInstaller：$pyinstaller"
}

Push-Location $projectRoot
try {
    & $python -c "from PIL import Image; image=Image.open(r'img/favicon.png').convert('RGBA'); image.save(r'img/blog-manager.ico', sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])"
    if (Test-Path "$projectRoot\DuckLingBlogManager.exe") {
        Remove-Item -LiteralPath "$projectRoot\DuckLingBlogManager.exe" -Force
    }
    & $pyinstaller --noconfirm --clean --distpath $projectRoot --workpath "$projectRoot\build\blog-manager" blog-manager.spec
    Write-Host "构建完成：$projectRoot\DuckLingBlogManager\DuckLingBlogManager.exe"
}
finally {
    Pop-Location
}
