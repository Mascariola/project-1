[app]
title = My Application
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = all
fullscreen = 1
source.include_patterns = assets/*,images/*.png

[buildozer]
log_level = 2

[android]
ndk = 23b
sdk = 20
api = 31
ndk_api = 21
arch = armeabi-v7a
minapi = 21
presplash.filename = %(source.dir)s/images/presplash.png
icon.filename = %(source.dir)s/images/icon.png
copy_libs = 1
keystore = %(source.dir)s/android.keystore
keyalias = %(package.name)s
keyalias_password = %(package.name)s
