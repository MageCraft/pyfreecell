os=$(uname)

echo os is $os

if [ "$os" = "Darwin" ]
then
    sdk_path="/Applications/Adobe Flex Builder 3/sdks/3.2.0"
else
    sdk_path="C:/Program Files/Adobe/Flex Builder 3/sdks/3.1.0"
fi

echo sdk path is $sdk_path

storetype=pkcs12
keystore=xatasks.p12
storepass=780524
app_path=atasks/bin-debug/
app_descriptor=${app_path}/atasks-app.xml
swf=atasks.swf

usage()
{
    echo "$0 -v version -destdir folder"
    echo "-v version: version of generated air package"
    echo "-destdir folder: dest folder of generated air package to be put"
}


if [ $# -eq 0 ]
then
    usage
    exit -1
fi

while [ $# -ge 1 ]
do
    case "$1" in 
	-v)
	    air_version="$2";shift;;
	-destdir)
	    dest_dir="$2"; shift;;
	*)
	    usage 
	    break;;
    esac
    shift
done

if [ -z $air_version ]
then
    usage
    exit -1
elif [ -z $dest_dir ]
then
   usage 
   exit -1 
fi

air_package=xatasks-${air_version}.air

sed "s/\(<version>\).*\(<\/version>\)/\1${air_version}\2/g" $app_descriptor > temp
mv -f temp $app_descriptor

echo "generating $air_package"
java -jar -Xmx512m "${sdk_path}/lib/adt.jar" -package -storetype $storetype -keystore $keystore -storepass $storepass $air_package $app_descriptor -C $app_path $swf
echo 'done'

mv -f $air_package $dest_dir
