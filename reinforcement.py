import numpy as np

class reinforcement():
	def __init__(self, robot_names, object_names, goal_pos, goal_limits):
		self.reward = 0
		self.goal_pos = np.zeros((1,3))
		self.robot_names = robot_names
		self.object_names = object_names
		self.goal_pos = goal_pos
		self.goal_limits = goal_limits
	def updateInfo(self, state_info):
		if(len(state_info) > 0):
			self.robot_pos = np.array(state_info[self.robot_names[0]][0])
			self.ball_pos = np.array(state_info[self.object_names[0]][0])
			return 1
		else:
			return 0
	def getReward(self):
		distance = np.linalg.norm(self.goal_pos - self.ball_pos)
		self.reward = (1/ distance if distance != 0 else 0.0001)
		if(self.isInsideGoal(self.ball_pos)):
			self.reward = 50
		return self.reward

	def isInsideGoal(self, obj_pos):
		if (obj_pos[0] > self.goal_pos[0]):
			if(obj_pos[1] < (self.goal_pos[1]+self.goal_limits[0])):
				if(obj_pos[1] > (self.goal_pos[1]+self.goal_limits[1])):
					return True
		return False