package flatasks.ui
{
	import flash.events.Event;
	import flash.events.FocusEvent;
	import flash.events.MouseEvent;
	import flash.geom.Point;
	
	import flatasks.ui.controls.FlatasksCheckBox;
	
	import mx.containers.Canvas;
	import mx.controls.Button;
	import mx.controls.CheckBox;
	import mx.controls.Label;
	import mx.controls.List;
	import mx.controls.TextInput;
	import mx.events.FlexEvent;

	public class FlatasksListItemRenderer extends Canvas
	{
		private var checkBoxDone:CheckBox;
		private var input:TextInput;
		private var labelText:Label;
		private var editing:Boolean;
		private var buttonSetting:Button;
		
		[Embed(source="/assets/img/btn_setting.png")]
		private var skinButtonSetting:Class;
		
		public function FlatasksListItemRenderer()
		{
			super();
			setStyle('borderColor', 0xAFB3CD);
			setStyle('borderStyle', 'solid');
			setStyle('borderSides', 'bottom');		
						
		}	
		
		private function createLabelText():void {
			labelText = new Label();
			labelText.addEventListener(MouseEvent.CLICK, labelText_onClick);
			addChild(labelText);
			
		}
		
		private function labelText_onClick(event:MouseEvent):void {			
			if(!editing) {
				editing = true;
				invalidateProperties();
			}
		}
		
		private function createCheckBoxDone():void {
			checkBoxDone = new FlatasksCheckBox();
			checkBoxDone.addEventListener(Event.CHANGE, checkBoxDone_onChange);
			addChild(checkBoxDone);			
		}
		
		private function checkBoxDone_onChange(event:Event):void {
			if(data) {
				data.task.done = checkBoxDone.selected;
				updateTask();	
			}
		}
		
		private function createButtonSetting():void {
			buttonSetting = new Button();
			buttonSetting.setStyle('skin', skinButtonSetting);
			buttonSetting.addEventListener(MouseEvent.CLICK, buttonSetting_onClick);
			buttonSetting.visible = false;
			addChild(buttonSetting);
					
		}
		
		private function buttonSetting_onClick(event:MouseEvent):void {						
			var pt:Point = new Point(buttonSetting.x, buttonSetting.y);
			var pt1:Point = localToGlobal(pt);			
			data.showTaskSettingMenu(pt1.x, pt1.y);						
		}
		
		private function updateTask():void {
			data.onTaskUpdated(data.task);
		}
		
		private function setInputStyle(focusIn:Boolean=true):void {
			if(focusIn) {
				input.setStyle('focusAlpha',1);					
				//input.setStyle('backgroundAlpha',0.3);
			} else {
				input.setStyle('focusAlpha',0);					
				//input.setStyle('backgroundAlpha',0);
			}
		}
		
		private function createInput():void {
			input = new TextInput();			
			input.setStyle('borderStyle', 'none');						
			setInputStyle(true);			
			input.addEventListener(FlexEvent.ENTER, input_onEnter);
			input.addEventListener(FocusEvent.FOCUS_OUT, input_onFocusOut);
			input.addEventListener(FocusEvent.FOCUS_IN, input_onFocusIn);
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
			input_onFocusOut(null);
			
		}
		
		private function input_onFocusIn(event:FocusEvent):void {
			setInputStyle();
		}
		
		private function input_onFocusOut(event:FocusEvent):void {
			input.visible = false;
			setInputStyle(false);
			updateTaskContent();
			editing = false;
			invalidateProperties();			
		}
		
		
		override protected function commitProperties():void {
			super.commitProperties();
			if(checkBoxDone) {
				checkBoxDone.removeEventListener(Event.CHANGE, checkBoxDone_onChange);
				removeChild(checkBoxDone);
				checkBoxDone = null;
			}
			if(input) {
				input.removeEventListener(FlexEvent.ENTER, input_onEnter);
				input.removeEventListener(FocusEvent.FOCUS_OUT, input_onFocusOut);
				input.removeEventListener(FocusEvent.FOCUS_IN, input_onFocusIn);
				removeChild(input);
				input = null;
			}
			if(labelText) {
				labelText.removeEventListener(MouseEvent.CLICK, labelText_onClick);
				removeChild(labelText);
				labelText = null;
			}
			if(buttonSetting) {
				buttonSetting.removeEventListener(MouseEvent.CLICK, buttonSetting_onClick);
				removeChild(buttonSetting);
				buttonSetting = null;
			}
			
			if(data) {
				createCheckBoxDone();
				if(editing) {
					createInput();
					input.text = data.task.content;
					input.setFocus();
				} else {
					createLabelText();
					labelText.text = data.task.content;
				}	
				createButtonSetting();			
				checkBoxDone.selected = data.task.done;				
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
			if(labelText) {
				labelText.setActualSize(labelText.measuredWidth, labelText.measuredHeight);
				labelText.x = startX;
				labelText.y = (h - labelText.height) / 2;
			}
			if(buttonSetting) {
				buttonSetting.setActualSize(buttonSetting.measuredWidth, buttonSetting.measuredHeight);
				buttonSetting.x = w - buttonSetting.width - 3;
				buttonSetting.y = (h - buttonSetting.height) / 2;				
				
				if(List(owner).isItemHighlighted(data)) {
					buttonSetting.visible = true;					
				} else {
					buttonSetting.visible = false;
				}
				
				
			}
			if(input) {
				input.setActualSize(w-startX-2, input.measuredHeight);
				input.x = startX;
				input.y = (h - input.height) / 2;				
			}
			
		}
		
		override protected function measure():void {
			measuredHeight = 24;
		}
		
		
		
	}
}