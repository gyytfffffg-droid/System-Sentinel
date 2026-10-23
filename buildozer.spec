[app]
title = System Sentinel
package.name = systemsentinel
package.domain = org.sentinel
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy,psutil
orientation = portrait
osx.kivy_version = 2.3.0
fullscreen = 0
android.permissions = INTERNET, READ_PHONE_STATE, READ_SMS, RECEIVE_SMS
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

