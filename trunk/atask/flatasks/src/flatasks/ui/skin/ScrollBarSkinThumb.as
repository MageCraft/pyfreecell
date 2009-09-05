package flatasks.ui.skin
{
	import flash.display.GradientType;
	import flash.geom.Matrix;

	import mx.skins.Border;

	public class ScrollBarSkinThumb extends Border
	{
		
		override public function get measuredHeight():Number {
			return 1;
		}
		
		override public function get measuredWidth():Number {
			return 16;
		}
		
		override protected function updateDisplayList(w:Number, h:Number):void {
			trace('MyScrollThumb', 'updateDisplayList', w, h );
			super.updateDisplayList(w,h);
			
			if( w <= 0 || h <= 0 ) {
				return;
			}
			graphics.clear();
			graphics.beginFill(0xF9F9F9);
			graphics.drawRect(0,0,w,h);
			
			var matrix:Matrix = new Matrix();
			matrix.createGradientBox(w,h);			
			graphics.beginGradientFill(GradientType.LINEAR, [0xF9F9F9, 0xEDEDED],[1,1],[0,255],matrix);
			graphics.drawRect(1,1,w-2,h-2);
			
			graphics.beginFill(0x999999);
			graphics.drawRect(0,h-1,w,1);
			var w1:int = 4;
			var h1:int = 1;			
			graphics.drawRect((w-w1)/2,h/2-2*h1,w1,h1);
			graphics.drawRect((w-w1)/2,h/2+h1,w1,h1);
			
			graphics.beginFill(0xFFFFFF);
			graphics.drawRect((w-w1)/2,h/2-h1,w1,h1);
			graphics.drawRect((w-w1)/2,h/2+2*h1,w1,h1);			
			
			graphics.endFill();
		}
	}
}