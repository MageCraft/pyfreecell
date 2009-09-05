package flatasks.ui
{
	import flash.display.Sprite;
	import flash.events.KeyboardEvent;
	import flash.events.MouseEvent;
	
	import mx.controls.CheckBox;
	import mx.controls.List;
	import mx.controls.TextInput;
	import mx.controls.listClasses.IListItemRenderer;

	public class FlatasksList extends List
	{
		private var checkBoxDone:CheckBox;
		private var input:TextInput;
		
		public function FlatasksList()
		{
			super();
		}
		
		override protected function drawSelectionIndicator(indicator:Sprite, x:Number, y:Number, width:Number, height:Number, color:uint, itemRenderer:IListItemRenderer):void {
			
		}
		
		override protected function drawHighlightIndicator(indicator:Sprite, x:Number, y:Number, width:Number, height:Number, color:uint, itemRenderer:IListItemRenderer):void {
			
		}
		
		override protected function keyDownHandler(event:KeyboardEvent):void {
			
		}
		
		override protected function mouseDownHandler(event:MouseEvent):void {
			
		}
		
		
		
	}
}