// ActionScript file
private function send(url:String, resultHandler:Function, method:String=URLRequestMethod.GET, vars:URLVariables=null, dataFormat:String=URLLoaderDataFormat.TEXT):void {
	trace('send', url);
	var loader:URLLoader = new URLLoader();
	var req:URLRequest = new URLRequest(url);
	req.method = method;
	if( vars )
		req.data = vars;				 
	loader.dataFormat = dataFormat;				
	loader.addEventListener(Event.COMPLETE, resultHandler);
	loader.addEventListener(HTTPStatusEvent.HTTP_RESPONSE_STATUS, onHttpResponseStatus);
	loader.addEventListener(IOErrorEvent.IO_ERROR, onIOError);
	loader.load(req);			
}

private function onHttpResponseStatus(event:HTTPStatusEvent):void {
	trace('onHttpResponseStatus', event.status);	
	//txtResults.text += 'http status code is ' + event.status + '\n';
}

private function onIOError(event:IOErrorEvent):void {
	trace('onIOError',event.errorID, event.text);
	//txtResults.text += 'IO Error, id: ' + event.errorID + ', message: ' + event.text + '\n';
	
}


