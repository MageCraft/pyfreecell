package flatasks.ui
{
	import mx.controls.CheckBox;
	import mx.controls.List;
	import mx.controls.TextInput;

	public class FlatasksList extends List
	{
		private var checkBoxDone:CheckBox;
		private var input:TextInput;
		
		public function FlatasksList()
		{
			super();
		}
		
		private function createCheckBoxDone():void {
			checkBoxDone = new CheckBox();
			addChild(checkBoxDone);			
		}
		
		private function createInput():void {
			input = new Input();
			addChild(input);
		}
		
		override protected function commitProperties():void {
			super.commitProperties();
		}
		
		override protected function updateDisplayList(w:Number, h:Number):void {
			super.updateDisplayList(w,h);
		}
		
	}
}