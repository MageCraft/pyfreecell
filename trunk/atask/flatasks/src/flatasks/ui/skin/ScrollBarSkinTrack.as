package flatasks.ui.skin
{
	import flash.display.GradientType;
	import flash.geom.Matrix;

	import mx.skins.Border;

	public class ScrollBarSkinTrack extends Border
	{

		private static const TRACK_FILL_COLORS:Array = [0x323232,0x424242];
		private static const TRACK_FILL_ALPHAS:Array = [1,1];
		private static const TRACK_FILL_RATIOS:Array = [0,255];	

		override public function get measuredWidth():Number
		{
			return 14;
		}

		override public function get measuredHeight():Number
		{
			return 1;
		}	

		override protected function updateDisplayList(unscaledWidth:Number, unscaledHeight:Number):void  {
			super.updateDisplayList(unscaledWidth, unscaledHeight);
			graphics.clear();       
			var matrix:Matrix = new Matrix();
			matrix.createGradientBox(unscaledWidth,unscaledWidth,0,0,0);
			graphics.beginGradientFill(GradientType.LINEAR,TRACK_FILL_COLORS,TRACK_FILL_ALPHAS,TRACK_FILL_RATIOS,matrix);
			graphics.drawRect(0,0,unscaledWidth,unscaledHeight);
			graphics.endFill();
		}
	}
}