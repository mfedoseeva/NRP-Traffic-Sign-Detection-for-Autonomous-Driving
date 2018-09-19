import hbp_nrp_cle.tf_framework as nrp
from hbp_nrp_cle.robotsim.RobotInterface import Topic
import geometry_msgs.msg

@nrp.MapVariable("sign", initial_value=None, scope=nrp.GLOBAL)
@nrp.Neuron2Robot(Topic('/husky/cmd_vel', geometry_msgs.msg.Twist))
def velo_control(sign):
	if sign.value == '100':
		return geometry_msgs.msg.Twist(
        linear=geometry_msgs.msg.Vector3(x=1.0, y=0.0, z=0.0),
        angular=geometry_msgs.msg.Vector3(x=0.0, y=0.0, z=0.0))
	else if sign.value == '20':
		return geometry_msgs.msg.Twist(
        linear=geometry_msgs.msg.Vector3(x=0.2, y=0.0, z=0.0),
        angular=geometry_msgs.msg.Vector3(x=0.0, y=0.0, z=0.0))
	else if sign.value == 'stop':
		return geometry_msgs.msg.Twist(
        linear=geometry_msgs.msg.Vector3(x=0.0, y=0.0, z=0.0),
        angular=geometry_msgs.msg.Vector3(x=0.0, y=0.0, z=0.0))
	else:
		return geometry_msgs.msg.Twist(
        linear=geometry_msgs.msg.Vector3(x=0.6, y=0.0, z=0.0),
        angular=geometry_msgs.msg.Vector3(x=0.0, y=0.0, z=0.0))


