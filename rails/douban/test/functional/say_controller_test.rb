require File.dirname(__FILE__) + '/../test_helper'
require 'say_controller'

# Re-raise errors caught by the controller.
class SayController; def rescue_action(e) raise e end; end

class SayControllerTest < Test::Unit::TestCase
  def setup
    @controller = SayController.new
    @request    = ActionController::TestRequest.new
    @response   = ActionController::TestResponse.new
  end

  # Replace this with your real tests.
  def test_truth
    assert true
  end
end
