package atasks.events
{
	import flash.events.Event;

	public class EditableLabelEvent extends Event
	{

		public static const TEXT_EDITING_START:String = "textEditingStart";
		public static const TEXT_EDITING_FINISHED:String = "textEditingFinished";
		public static const TEXT_CHANGED:String = "textChanged";		 

		public var finishedReason:String;
		
		public function EditableLabelEvent(type:String, bubbles:Boolean=false, cancelable:Boolean=false)
		{
			super(type, bubbles, cancelable);
		}

	}
}

