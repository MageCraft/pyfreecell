// ActionScript file
private function send(url:String, resultHandler:Function, method:String=URLRequestMethod.GET, vars:URLVariables=null, dataFormat:String=URLLoaderDataFormat.TEXT):void {
	var loader:URLLoader = new URLLoader();
	var req:URLRequest = new URLRequest(url);
	req.method = method;
	if( vars )
		req.data = vars;				 
	loader.dataFormat = dataFormat;				
	loader.addEventListener(Event.COMPLETE, resultHandler,false,0,true);
	loader.addEventListener(HTTPStatusEvent.HTTP_RESPONSE_STATUS, onHttpResponseStatus,false,0,true);
	loader.addEventListener(IOErrorEvent.IO_ERROR, onIOError, false, 0, true);
	loader.load(req);			
}

private function onHttpResponseStatus(event:HTTPStatusEvent):void {
	trace(event.status);
	//txtResults.text += 'http status code is ' + event.status + '\n';
}

private function onIOError(event:IOErrorEvent):void {
	trace(event.errorID, event.text);
	//txtResults.text += 'IO Error, id: ' + event.errorID + ', message: ' + event.text + '\n';
	
}

