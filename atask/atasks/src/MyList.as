package
{
	import flash.display.Sprite;
	
	import mx.controls.List;
	import mx.controls.listClasses.IListItemRenderer;

	public class MyList extends List
	{
		public function MyList()
		{
			super();
		}
		
		override protected function drawHighlightIndicator(indicator:Sprite, x:Number, y:Number, width:Number, height:Number, color:uint, itemRenderer:IListItemRenderer):void {
			//do nothing
		}
		
		override protected function drawSelectionIndicator(indicator:Sprite, x:Number, y:Number, width:Number, height:Number, color:uint, itemRenderer:IListItemRenderer):void
		{
			//do nothing
		}
		
	}
}