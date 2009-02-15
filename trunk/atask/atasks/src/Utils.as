package
{
	import flash.desktop.NativeApplication;
	
	public class Utils
	{
		public function Utils()
		{
		}
		
		public static function getAppVersion():String {
			var appXML:XML = NativeApplication.nativeApplication.applicationDescriptor;
			var ns:Namespace = appXML.namespace();
			var appVersion:String = appXML.ns::version[0];
			return appVersion;
		}

	}
}