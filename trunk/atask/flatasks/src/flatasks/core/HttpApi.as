package flatasks.core
{
	import flash.events.Event;
	import flash.events.HTTPStatusEvent;
	import flash.events.IOErrorEvent;
	import flash.net.URLLoader;
	import flash.net.URLLoaderDataFormat;
	import flash.net.URLRequest;
	import flash.net.URLRequestMethod;
	import flash.net.URLVariables;
	
	public class HttpApi
	{
		public function HttpApi()
		{
				
		}
		
		public static function send(url:String, 
								    resultHandler:Function,								    
								    method:String=URLRequestMethod.GET,
								    vars:URLVariables=null,
								    dataFormat:String=URLLoaderDataFormat.TEXT,
								    errorHandler:Function=null):void {
			var loader:URLLoader = new URLLoader();
			var req:URLRequest = new URLRequest(url);
			req.method = method;
			if( vars )
				req.data = vars;				 
			loader.dataFormat = dataFormat;				
			loader.addEventListener(Event.COMPLETE, resultHandler);
			loader.addEventListener(HTTPStatusEvent.HTTP_STATUS, defaultHttpResponseHandler);
			loader.addEventListener(IOErrorEvent.IO_ERROR, defaultIOErrorHandler);
			loader.load(req);			
		}
		
		private static function defaultHttpResponseHandler(event:HTTPStatusEvent):void {
			trace(event.status);
		}
		
		private static function defaultIOErrorHandler(event:IOErrorEvent):void {
			trace(event.text);
		}

	}
}