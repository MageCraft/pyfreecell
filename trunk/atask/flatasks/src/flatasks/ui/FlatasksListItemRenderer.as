package flatasks.ui
{
	import flash.events.Event;
	import flash.events.FocusEvent;
	
	import mx.containers.Canvas;
	import mx.controls.CheckBox;
	import mx.controls.TextInput;
	import mx.events.FlexEvent;

	public class FlatasksListItemRenderer extends Canvas
	{
		private var checkBoxDone:CheckBox;
		private var input:TextInput;
		
		public function FlatasksListItemRenderer()
		{
			super();
		}
		
		
		private function createCheckBoxDone():void {
			checkBoxDone = new CheckBox();
			checkBoxDone.addEventListener(Event.CHANGE, checkBoxDone_onChange);
			addChild(checkBoxDone);			
		}
		
		private function checkBoxDone_onChange(event:Event):void {
			if(data) {
				data.task.done = checkBoxDone.selected;
				updateTask();	
			}
		}
		
		private function updateTask():void {
			data.onTaskUpdated(data.task);
		}
		
		private function createInput():void {
			input = new TextInput();
			input.setStyle('borderStyle', 'none');
			input.setStyle('backgroundAlpha',0);
			input.setStyle('alpha',0);
			input.setStyle('focusAlpha',0);	
			input.addEventListener(FlexEvent.ENTER, input_onEnter);
			input.addEventListener(FocusEvent.FOCUS_OUT, input_onFocusOut);	
			addChild(input);
		}
		
		private function updateTaskContent():void {
			if(data) {
				if( data.task.content != input.text ) {
					data.task.content = input.text;
					updateTask();
				}
			}
		}
		
		private function input_onEnter(event:FlexEvent):void {
			updateTaskContent()
		}
		
		private function input_onFocusOut(event:FocusEvent):void {
			updateTaskContent();
		}
		
		
		override protected function commitProperties():void {
			super.commitProperties();
			if(checkBoxDone) {
				removeChild(checkBoxDone);
				checkBoxDone = null;
			}
			if(input) {
				removeChild(input);
				input = null;
			}
			
			if(data) {
				createCheckBoxDone();
				createInput();				
				checkBoxDone.selected = data.task.done;
				input.text = data.task.content;
			}
		}
		
		override protected function updateDisplayList(w:Number, h:Number):void {
			super.updateDisplayList(w,h);
			var startX:int;
			if(checkBoxDone) {
				checkBoxDone.x = startX;
				checkBoxDone.setActualSize(checkBoxDone.measuredWidth, checkBoxDone.measuredHeight);
				checkBoxDone.y = (h - checkBoxDone.height)/2;
				startX += checkBoxDone.width + 3;
			}
			if(input) {
				input.setActualSize(w-startX, input.measuredHeight);
				input.x = startX;
				input.y = (h - input.height) / 2;				
			}
		}
		
		
		
	}
}