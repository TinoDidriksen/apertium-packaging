make clean
make -j8 || make -j8 || make -j8 || make -j8 || make
make install DESTDIR=/opt/win32-pkg/$PKG_NAME
for INST in $EXTRA_INST
do
	install $INST /opt/win32-pkg/$PKG_NAME/opt/win32/bin
done

cd /opt/win32-pkg/$PKG_NAME/opt/win32/bin
/misc/branches/packaging/win32-copy-deps.pl

cd /opt/win32-pkg/$PKG_NAME/opt
for DEP in $EXTRA_DEPS
do
	cp -avf /opt/mxe/usr/i686-w64-mingw32.shared/bin/$DEP win32/bin/
done

set +e
find . -type f -name '*.exe' -or -name '*.dll' | grep -v 7z | xargs -rn1 /opt/mxe/usr/bin/i686-w64-mingw32.shared-strip
find . -type f -name '*.exe' -or -name '*.dll' | grep -v 7z | xargs -rn1 chmod uga+x
find . -type f -name '*.a' | xargs -rn1 /opt/mxe/usr/bin/i686-w64-mingw32.shared-strip --strip-debug
set -e
chmod -R uga+r win32
mv win32 $PKG_NAME
zip -9r $PKG_NAME-$PKG_VER.zip $PKG_NAME
7za a -l $PKG_NAME-$PKG_VER.7z $PKG_NAME
rm -fv ~apertium/public_html/win32/nightly/$PKG_NAME-[0-9]*.zip
rm -fv ~apertium/public_html/win32/nightly/$PKG_NAME-[0-9]*.7z
mv -v *.zip ~apertium/public_html/win32/nightly/
mv -v *.7z ~apertium/public_html/win32/nightly/
cd ~apertium/public_html/win32/nightly/
ln -sfv $PKG_NAME-$PKG_VER.zip $PKG_NAME-latest.zip
ln -sfv $PKG_NAME-$PKG_VER.7z $PKG_NAME-latest.7z
chown -R apertium:apertium ~apertium/public_html/win32
