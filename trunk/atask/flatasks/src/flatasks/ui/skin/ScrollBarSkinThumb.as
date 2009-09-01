package flatasks.ui.skin
{
	import flash.display.GradientType;
	import flash.geom.Matrix;

	import mx.skins.Border;

	public class ScrollBarSkinThumb extends Border
	{

		private static const THUMB_FILL_COLORS:Array = [0x626262,0x8D8D8D,0x8D8D8D,0x626262];
		private static const THUMB_FILL_ALPHAS:Array = [1,1,1,1];
		private static const THUMB_FILL_RATIOS:Array = [0,80,175,255];		

		override public function get measuredWidth():Number
		{
			return 14;
		}

		override public function get measuredHeight():Number
		{
			return 1;
		}	
		
		
		override protected function updateDisplayList(w:Number, h:Number):void  {
			super.updateDisplayList(w, h);
			graphics.clear();       
			var matrix:Matrix = new Matrix();
			matrix.createGradientBox(w,h,0,0,0);
			graphics.beginGradientFill(GradientType.LINEAR,THUMB_FILL_COLORS,THUMB_FILL_ALPHAS,THUMB_FILL_RATIOS,matrix);
			graphics.moveTo(0,4);
			graphics.lineTo(0,h-4);
			graphics.curveTo(w/2,h+1,w,h-4);
			graphics.lineTo(w,4);
			graphics.curveTo(w/2,-1,0,4);
			graphics.endFill();
		}
	}
}