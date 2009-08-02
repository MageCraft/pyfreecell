// ActionScript file
import flash.events.Event;

private function send(url:String,                       
                      resultHandler:Function, 
                      method:String=URLRequestMethod.GET, vars:URLVariables=null, 
                      dataFormat:String=URLLoaderDataFormat.TEXT):void {
	trace('send', url);
	var loader:URLLoader = new URLLoader();
	var req:URLRequest = new URLRequest(url);
	req.method = method;
	if( vars )
		req.data = vars;				 
	loader.dataFormat = dataFormat;				
	loader.addEventListener(Event.COMPLETE, resultHandler);
	loader.addEventListener(HTTPStatusEvent.HTTP_RESPONSE_STATUS, defaultHttpResponseHandler);
	loader.addEventListener(IOErrorEvent.IO_ERROR, defaultIOErrorHandler);
	loader.load(req);  		
}

private function send1(url:String, 
                      resultHandler:Function,                      
                      httpResponseHandler:Function,
                      /*ioErrorHandler:Function,*/ 
                      method:String=URLRequestMethod.GET, 
                      vars:URLVariables=null, 
                      dataFormat:String=URLLoaderDataFormat.TEXT):void {
	trace('send', url);
	var loader:URLLoader = new URLLoader();
	var req:URLRequest = new URLRequest(url);
	req.method = method;
	if( vars )
		req.data = vars;				 
	loader.dataFormat = dataFormat;				
	loader.addEventListener(Event.COMPLETE, resultHandler);
	loader.addEventListener(HTTPStatusEvent.HTTP_RESPONSE_STATUS, httpResponseHandler);
	loader.addEventListener(IOErrorEvent.IO_ERROR, defaultIOErrorHandler);
	loader.load(req);  		
}


private function defaultHttpResponseHandler(event:HTTPStatusEvent):void {
	trace('onHttpResponseStatus', event.status, event.responseURL);	
}

private function defaultIOErrorHandler(event:IOErrorEvent):void {
	trace('onIOError',event.errorID, event.text);	
}


