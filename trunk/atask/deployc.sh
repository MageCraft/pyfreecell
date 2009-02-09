sdk_path="C:/Program Files/Adobe/Flex Builder 3/sdks/3.1.0"
storetype=pkcs12
keystore=xatasks.p12
storepass=780524
app_path=atasks/bin-debug/
app_xml=${app_path}/atasks-app.xml
swf=atasks.swf
air_package=xatasks.air

echo "generating $air_package"
java -jar -Xmx512m "${sdk_path}/lib/adt.jar" -package -storetype $storetype -keystore $keystore -storepass $storepass $air_package $app_xml -C $app_path $swf
echo 'done'

web_dir=atasksd/media
mv -f $air_package $web_dir
