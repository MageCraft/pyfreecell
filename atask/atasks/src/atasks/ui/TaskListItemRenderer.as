package atasks.ui
{
	import atasks.core.Task;
	import atasks.events.EditableLabelEvent;
	
	import flash.events.Event;
	import flash.events.MouseEvent;
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
		
		private function createLabel():void {
			labelTask = new EditableLabel;
			labelTask.editable = true;			
			labelTask.setStyle('fontSize',13);			
			labelTask.addEventListener(EditableLabelEvent.TEXT_CHANGED, labelTask_onTextChanged);
			labelTask.addEventListener(EditableLabelEvent.TEXT_EDITING_FINISHED, labelTask_onEditingFinished);
			addChild(labelTask);
		}
		
		private function createCheckBox():void {
			checkBoxDone = new CheckBox;
			checkBoxDone.addEventListener(Event.CHANGE, checkBoxDone_onChange);
			addChild(checkBoxDone);
		}		
		
		private function createDeleteButton():void {
			buttonDelete = new Button;
			buttonDelete.setStyle('skin', skinButtonDelete);
			buttonDelete.addEventListener(MouseEvent.MOUSE_DOWN, buttonDelete_onMouseDown);
			addChild(buttonDelete);	
		}		
		
		private function createTaskItem():void {
			createCheckBox();
			createLabel();
			createDeleteButton();
		}
		
		private function createAddTaskItem():void {
			createCheckBox();
			createLabel();
			labelAddTask = new Label;
			labelAddTask.text = "Add new item...";
			labelAddTask.setStyle('fontWeight', 'bold');
			labelAddTask.setStyle('fontSize', 13);
			labelAddTask.addEventListener(MouseEvent.CLICK, labelAddTask_onClick);
			addChild(labelAddTask);	
		}
		
		private function setLabelTaskFontStyle():void {
			if( data.task.done ) {				 
				labelTask.setStyle('fontStyle', FontStyle.ITALIC); 
			} else {
				labelTask.setStyle('fontStyle', FontStyle.REGULAR);
			}
		}
		
		private function labelAddTask_onClick(event:MouseEvent):void {
			labelAddTask.visible = false;
			labelTask.dispatchEvent(event);
		}		
		
		private function checkBoxDone_onChange(event:Event):void {
			data.task.done = checkBoxDone.selected;
			data.fnUpdateTask(data.task);
			setLabelTaskFontStyle();
		}
		
		private function buttonDelete_onMouseDown(event:MouseEvent):void {
			data.fnDeleteTask(data);
		}
		
		private function labelTask_onEditingFinished(event:EditableLabelEvent):void {
			if( !data.task && !labelTask.text ) {
				labelAddTask.visible = true;
				invalidateProperties();
			}		
		}
		
		private function labelTask_onTextChanged(event:EditableLabelEvent):void {
			if( data.task ) {
				data.task.content = labelTask.text;
				data.fnUpdateTask(data.task);
				invalidateProperties();
			} else {
				if( labelTask.text ) { 
					var task:Task = new Task;
					task.content = labelTask.text;
					data.task = task;
					data.fnAddTask(data.task, event.finishedReason == "enter");
					invalidateProperties();
				}
			}			
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
			if( labelAddTask ) {
				labelAddTask.x = labelTask.x;
				checkBoxDone.visible = false;
				if( data && data.editableAtFirst ) {
					labelAddTask.dispatchEvent(new MouseEvent(MouseEvent.CLICK));	
				}
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
			if( data && data.editableAtFirst ) {
				
			}
						
			
		}
		
		override protected function measure():void {
			measuredHeight = 25;
		}

	}
}