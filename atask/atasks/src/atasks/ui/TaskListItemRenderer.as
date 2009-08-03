package atasks.ui
{
	import atasks.core.Task;
	import atasks.events.EditableLabelEvent;
	
	import flash.display.DisplayObject;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.geom.Rectangle;
	import flash.text.FontStyle;
	
	import mx.containers.Canvas;
	import mx.controls.Button;
	import mx.controls.CheckBox;
	import mx.controls.Label;
	import mx.controls.List;
	
	
	public class TaskListItemRenderer extends Canvas
	{
		private var checkBoxDone:CheckBox;
		private var labelTask:EditableLabel;
		private var buttonDelete:Button;
		private var labelAddTask:Label;
		
		
		[Embed(source="/../assets/img/delete.gif")]
		private var skinButtonDelete:Class;
		
		
		public function TaskListItemRenderer()
		{
			super();
			setStyle('borderSides','bottom');
			setStyle('borderStyle','solid');
			setStyle('borderThickness',1);
			setStyle('borderColor',0xcccccc);
		}
		
		private function createTaskItem():void {
			checkBoxDone = new CheckBox;
			checkBoxDone.addEventListener(Event.CHANGE, checkBoxDone_onChange);
			addChild(checkBoxDone);
			labelTask = new EditableLabel;
			labelTask.editable = true;			
			labelTask.setStyle('fontSize',13);
			labelTask.addEventListener(EditableLabelEvent.TEXT_CHANGED, labelTask_onTextChanged);
			addChild(labelTask);
			buttonDelete = new Button;
			buttonDelete.setStyle('skin', skinButtonDelete);
			buttonDelete.addEventListener(MouseEvent.MOUSE_DOWN, buttonDelete_onMouseDown);
			addChild(buttonDelete);			
		}
		
		private function createAddTaskItem():void {
			labelAddTask = new Label;
			labelAddTask.setStyle('fontSize',13);
			labelAddTask.setStyle('fontWeight','bold');			
			labelAddTask.text = "Add New Task...";
			labelAddTask.addEventListener(MouseEvent.MOUSE_DOWN, labelAddTask_onMouseDown);
			addChild(labelAddTask);
		}
		
		private function setLabelTaskFontStyle():void {
			if( data.task.done ) {				 
				labelTask.setStyle('fontStyle', FontStyle.ITALIC); 
			} else {
				labelTask.setStyle('fontStyle', FontStyle.REGULAR);
			}
		}
		
		private function labelAddTask_onMouseDown(event:MouseEvent):void {
			
		}
		
		private function checkBoxDone_onChange(event:Event):void {
			data.task.done = checkBoxDone.selected;
			data.fnUpdateTask(data.task);
			setLabelTaskFontStyle();
		}
		
		private function buttonDelete_onMouseDown(event:MouseEvent):void {
			data.fnDeleteTask(data);
		}
		
		private function labelTask_onTextChanged(event:EditableLabelEvent):void {
			data.task.content = labelTask.text;
			data.fnUpdateTask(data.task);
		}
		
		override protected function commitProperties():void {
			super.commitProperties();
			if(checkBoxDone) {
				removeChild(checkBoxDone);
				checkBoxDone = null;
			}
			if(labelTask) {
				removeChild(labelTask);
				labelTask = null;
			}
			if(buttonDelete) {
				removeChild(buttonDelete);
				buttonDelete = null;
			}
			if(labelAddTask) {
				removeChild(labelAddTask);
				labelAddTask = null;
			}
			if( data ) {
				if( data.task ) {
					createTaskItem();
					var task:Task = data.task;
					checkBoxDone.selected = task.done;
					labelTask.text = task.content;
					setLabelTaskFontStyle();		
				} else {
					createAddTaskItem();
				}								 
			}
		}
		
		override protected function updateDisplayList(unscaledWidth:Number, unscaledHeight:Number):void {
			super.updateDisplayList(unscaledWidth, unscaledHeight);
			var startX:int = 0;
			
			if( checkBoxDone ) {
				checkBoxDone.x = startX;
				checkBoxDone.setActualSize(checkBoxDone.measuredWidth, checkBoxDone.measuredHeight);
				checkBoxDone.y = (unscaledHeight - checkBoxDone.height) / 2;
				startX += checkBoxDone.width + 3;				
			}
			if( labelTask ) {
				labelTask.x = startX;
				labelTask.setActualSize(unscaledWidth - startX, labelTask.measuredHeight);
				labelTask.y = (unscaledHeight - labelTask.height) / 2;				
			}
			if( buttonDelete ) {
				if( List(owner).isItemHighlighted(data) ) {
					buttonDelete.visible = true;
					buttonDelete.setActualSize(buttonDelete.measuredWidth, buttonDelete.measuredHeight);
					buttonDelete.x = unscaledWidth - buttonDelete.width;
					buttonDelete.y = (unscaledHeight - buttonDelete.height) / 2;
				} else {
					buttonDelete.visible = false;
				}
			}
			
			if( data && data.editing ) {
				var listParent:DisplayObject = List(owner).parent;
				var r:Rectangle = labelTask.getBounds(listParent);
				trace(r);
			}
			
		}
		
		override protected function measure():void {
			measuredHeight = 30;
		}

	}
}