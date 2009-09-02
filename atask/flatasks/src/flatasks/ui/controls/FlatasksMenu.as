package flatasks.ui.controls
{
	import flash.display.DisplayObjectContainer;
	import flash.geom.Point;
	
	import mx.controls.Menu;
	import mx.events.FlexEvent;
	
	public class FlatasksMenu
	{
		private static var parent:DisplayObjectContainer;
		
		public function FlatasksMenu()
		{
		}
		
		public static function createMenu(p:DisplayObjectContainer, mdp:Object, showRoot:Boolean=true):Menu {
			parent = p;
			var menu:Menu = Menu.createMenu(parent,mdp,showRoot);
			menu.addEventListener(FlexEvent.UPDATE_COMPLETE, menu_onUpdateComplete);
			menu.setStyle('openDuration',0);
			return menu;			
		}
		
		private static function menu_onUpdateComplete(event:FlexEvent):void {
			var menu:Menu = event.target as Menu;			
			if( menu.y + menu.height > parent.height ) {
				menu.y = parent.height - menu.height;
			}
			if( menu.x + menu.width > parent.width) {
				menu.x = parent.width - menu.width;
			}
		}
		
		public static function show(menu:Menu, pt:Point):void {			
			var pt1:Point = parent.localToGlobal(pt);
			menu.show(pt1.x,pt1.y);
		}
		

	}
}