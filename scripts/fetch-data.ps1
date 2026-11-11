$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$H = @{ "User-Agent" = "opencode" }
$root = "C:\Users\CHR\Desktop\Git\ChiakoRh"

try {
    $user = Invoke-RestMethod "https://api.github.com/users/ChiakoRh" -Headers $H -TimeoutSec 25
    $repos = Invoke-RestMethod "https://api.github.com/users/ChiakoRh/repos?per_page=100" -Headers $H -TimeoutSec 25

    $slim = [ordered] @{}
    foreach ($r in $repos) {
        if ($r.fork) { continue }
        $langs = [ordered] @{}
        try {
            $l = Invoke-RestMethod $r.languages_url -Headers $H -TimeoutSec 25
            $l.PSObject.Properties | ForEach-Object { $langs[$_.Name] = $_.Value }
        } catch { }
        $slim[$r.name] = [ordered] @{
            description = $r.description
            stars       = $r.stargazers_count
            language    = $r.language
            pushed_at   = ([datetime]$r.pushed_at).ToString("yyyy-MM-dd")
            languages   = $langs
        }
    }

    $data = [ordered] @{
        user = [ordered] @{ followers = $user.followers; public_repos = $user.public_repos }
        repos = $slim
    }
    $json = $data | ConvertTo-Json -Depth 5
    [IO.File]::WriteAllText("$root\scripts\data.json", $json, [Text.UTF8Encoding]::new($false))
    Write-Output "data.json written (non-fork repos: $($slim.Count))"

    New-Item -ItemType Directory -Force "$root\scripts\.cache" | Out-Null
    foreach ($name in @("WSK", "BPB-Scan", "RemGodCatcher", "KKDA", "KHP", "KAL")) {
        $p = "$root\scripts\.cache\$name.jpg"
        if (-not (Test-Path $p)) {
            Invoke-WebRequest "https://opengraph.githubassets.com/1/ChiakoRh/$name" -Headers $H -OutFile $p -TimeoutSec 30
            Write-Output "cover: $name"
        }
    }
} catch {
    Write-Output "github api failed: $($_.Exception.Message)"
    exit 1
}
