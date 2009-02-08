sdk_path="C:/Program Files/Adobe/Flex Builder 3/sdks/3.1.0"
adt="java -jar -Xmx512m ${sdk_path}/lib/adt.jar"
adt="C:/Program Files/Adobe/Flex Builder 3/sdks/3.1.0/bin/adt"
storetype=pkcs12
keystore=xatasks.p12
storepass=780524
app_path=atasks/bin-debug/
app_xml=${app_path}/atasks-app.xml

function run_adt
{
"$adt" -package -storetype $storetype -keystore $keystore -storepass $storepass \
xatasks.air $app_xml -C $app_path 
}

run_adt
