[app]
title = IQOptionBacktest
package.name = iqoptionbacktest
package.domain = org.iqoption
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,requests,pytz,iqoptionapi
orientation = portrait
fullscreen = 1

# Permissões
android.permissions = INTERNET

# APIs e SDKs
android.api = 31
android.minapi = 21
android.ndk = 23b
android.sdk = 24
android.build_tools = 36.0.0

# Arquiteturas suportadas
android.archs = armeabi-v7a,arm64-v8a

# Modo de build
android.build_type = release

# Desativa compilação com Cython para reduzir problemas
use_setup_py = false

# Logs
log_level = 2

# Icone do aplicativo (opcional - substitua por seu caminho)
# icon.filename = %(source.dir)s/icon.png
