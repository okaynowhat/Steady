#!/usr/bin/env bash
# Builds and signs the Steady APK with apktool and uber-apk-signer (SPEC.md section 14).
# Usage: KS=/path/steady-release.jks KS_PASS=... TOOLS=/dir/with/jars ./android/build.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(dirname "$HERE")"
: "${KS:?set KS to the keystore path}"; : "${KS_PASS:?set KS_PASS}"; : "${TOOLS:?set TOOLS to the folder with apktool.jar and uber-apk-signer.jar}"
OUT="$ROOT/dist"; mkdir -p "$OUT"
cp "$ROOT/index.html" "$HERE/assets/index.html"
java -jar "$TOOLS/apktool.jar" b "$HERE" -o "$OUT/steady-unsigned.apk"
java -jar "$TOOLS/uber-apk-signer.jar" -a "$OUT/steady-unsigned.apk" --ks "$KS" --ksAlias steady --ksPass "$KS_PASS" --ksKeyPass "$KS_PASS" -o "$OUT"
VER=$(grep versionName "$HERE/apktool.yml" | awk '{print $2}')
SIGNED=$(ls "$OUT"/*aligned-signed.apk | head -1); mv "$SIGNED" "$OUT/steady-$VER.apk"
rm -f "$OUT/steady-unsigned.apk" "$OUT"/*.idsig
echo "Built $OUT/steady-$VER.apk"
