package flatasks.ui.skin
{
	import flash.display.GradientType;
	import flash.geom.Matrix;

	import mx.skins.Border;

	public class ScrollBarSkinTrack extends Border
	{
				
		override public function get measuredHeight():Number {
			return 1;
		}
		
		override public function get measuredWidth():Number {
			return 16;
		}
		
		override protected function updateDisplayList(w:Number, h:Number):void {
			trace('updateDisplayList', w, h);
			super.updateDisplayList(w,h);
			graphics.clear();
			
			if( w <= 0 || h <= 0 ) {
				return;
			}			
			
			graphics.beginFill(0xBEBEBE);
			graphics.drawRect(0,0,w,h);		
			graphics.beginFill(0xCCCCCC);
			graphics.drawRect(1,0,w,h-1);					
			graphics.endFill();			
						
		}
	}
}