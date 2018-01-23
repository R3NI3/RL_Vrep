import numpy as np

class reinforcement:
    def __init__(self, robot_names, object_names):
    	self.reward = 0
    	self.robot_names = robot_names
    	self.object_names = object_names
	def updateEntities(self, state_info): 
		if(state_info.lenght > 0):
    		self.robot_pos = np.array(state_info[self.robot_names[0]][0])
    		self.target_pos = np.array(state_info[self.object_names[0]][0])
    		return 1
    	else
    		return 0
	def getReward(self):
		distance = np.linalg.norm(self.robot_pos - self.target_pos)
    	self.reward = (1/ distance if distance != 0 else 1000)
    	return self.reward