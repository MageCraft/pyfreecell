package  atasks.ui
{
	import atasks.events.EditableLabelEvent;
	
	import flash.display.DisplayObject;
	import flash.events.FocusEvent;
	import flash.events.MouseEvent;
	
	import mx.containers.Canvas;
	import mx.controls.Label;
	import mx.controls.TextInput;
	import mx.core.IUITextField;
	import mx.core.mx_internal;
	import mx.events.FlexEvent;
	import mx.events.ResizeEvent;

	[Event(name="textEditingStart", type="mint.leaf.events.EditableLabelEvent")]
	[Event(name="textEditingFinished", type="mint.leaf.events.EditableLabelEvent")]
	[Event(name="textChanged", type="mint.leaf.events.EditableLabelEvent")]

	public class EditableLabel extends Canvas
	{
		private var _text:String;
		private var _editable:Boolean;

		private var _label:Label;
		private var _input:TextInput;

		private var editing:Boolean = false;
		
		public var editExist:Boolean = true;

		public function EditableLabel()
		{
			percentWidth = 100;
			percentHeight = 100;			

			addEventListener(ResizeEvent.RESIZE,this_onResize);
			addEventListener(MouseEvent.CLICK,this_onClick);
		}

		public function set text(text:String):void {
			_text = text;
			if(_label) {
				_label.text = text;
			}
		}

		public function get text():String {
			return _text;
		}

		public function set editable(editable:Boolean):void {
			_editable = editable;	
		}

		public function get editable():Boolean {
			return _editable;
		}

		override protected function createChildren():void {
			super.createChildren();
			createLabel();
		}

		private function createLabel():void {
			if(_label) {
				return;
			}

			_label = new Label();
			_label.text = text;	
			_label.setStyle("verticalCenter",0);

			addChild(_label);

			this_onResize(null);
		}

		private function this_onResize(event:ResizeEvent):void {
			if(_label) {
				_label.width = width;
			}
		}

		private function this_onClick(event:MouseEvent):void {
			if(!editing) {
				startEditing();
			}
		}

		private function startEditing():void {		
			if(!editable) {
				return;
			}

			_label.visible = false;
			_input = new TextInput();
			_input.width = width;
			if(editExist) {			
				_input.text = text;
			}			
			_input.setStyle("borderStyle","solid");
			_input.setStyle("cornerRadius",3);
			_input.addEventListener(FlexEvent.ENTER,input_onEnter);
			_input.addEventListener(FocusEvent.FOCUS_OUT,input_onFocusOut);
			stage.addEventListener(MouseEvent.MOUSE_DOWN,stage_onMouseDown);
			addChild(_input);
			editing = true;
			dispatchEvent(new EditableLabelEvent(EditableLabelEvent.TEXT_EDITING_START));
			callLater(inputSetSelection);
		}

		private function inputSetSelection():void {
			var textField:IUITextField = _input.mx_internal::getTextField();			
			textField.alwaysShowSelection = false;			
			_input.setSelection(0,0);			
			textField.setFocus();
		}

		private function input_onEnter(event:FlexEvent):void {
			finishEditing();
		}

		private function input_onFocusOut(event:FocusEvent):void {
			finishEditing();
		}

		private function stage_onMouseDown(event:MouseEvent):void {
			// if current down object is not the input,finish the editing
			if(event.target != _input && !_input.contains(DisplayObject(event.target))) {
				finishEditing();
			}
		}


		private function finishEditing(enter:Boolean=false):void {
			if(!editing) {
				return;
			}
			
			var changed:Boolean = text != _input.text;
			text = _input.text;
			_input.removeEventListener(FlexEvent.ENTER,input_onEnter);
			_input.removeEventListener(FocusEvent.FOCUS_OUT,input_onFocusOut);
			stage.removeEventListener(MouseEvent.MOUSE_DOWN,stage_onMouseDown);
			removeChild(_input);
			_input = null;
			_label.visible = true;
			editing = false;
			var e1:EditableLabelEvent = new EditableLabelEvent(EditableLabelEvent.TEXT_EDITING_FINISHED)
			if(enter) e1.finishedReason = "enter";
			dispatchEvent(e1);
			if(changed) {
				var e2:EditableLabelEvent = new EditableLabelEvent(EditableLabelEvent.TEXT_CHANGED);
				if(enter) e2.finishedReason = "enter";
				dispatchEvent(e2);
			}
		}




	}
}

