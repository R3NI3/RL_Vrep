import vrep
import numpy as np
import random
import time
from environment import vrep_env
from reinforcement import reinforcement

ip = '127.0.0.1'
port = 19997
time_step = 0.01
motor_names = ['LeftMotor', 'RightMotor']
object_names = ['Bola']
robot_names = ['DifferentialDriveRobot']
goal_pos = [0.73, 0, 0.0725]
goal_limits = [0.174, -0.174]
epsilon = 0.8

NUM_ACT = 10 #discretization of actions per motor

#def select_action(state):
#    sample = random.random()

#    if sample > epsilon:
        #greedy
        #return model(Variable(state, volatile=True).type(FloatTensor)).data.max(1)[1].view(1, 2)
#    else:
#        return LongTensor([[random.randrange(NUM_ACT), random.randrange(NUM_ACT)]])


def get_reward(state_info):
    reward = 0
    robot_pos = np.array(state_info[robot_names[0]][0])
    target_pos = np.array(state_info[object_names[0]][0])
    distance = np.linalg.norm(robot_pos - target_pos)
    reward = 1/ distance if distance != 0 else 1000
    return reward

def train(env, model):
    actions = select_action()


def main():
    env = vrep_env(ip, port, time_step, motor_names, robot_names, object_names)
    reinforce = reinforcement(robot_names, object_names, goal_pos, goal_limits)
    model = None
    # --------- Stop Sim ----
    env.startSimulation()
    env.stop_robot(motor_names)
    env.stopSimulation()
    time.sleep(.05)

    # --------- Dummy Sim ---
    num_simulations = 0
    while(num_simulations < 2):
        env.startSimulation()
        dt = 0
        while (dt < 1):
            env.setJointVelocity(motor_names, [0,0])
            state_info = env.getSimulationState()
            reinforce.updateInfo(state_info)
            print(reinforce.getReward())
            dt += time_step
        env.stop_robot(motor_names)
        env.stopSimulation()
        time.sleep(.05)
        num_simulations += 1

    # --------- Train -------
    #print("train")
    #train(env, model)

    # --------- Test --------
    #print("test")
    #test(clientID, motor_handles, target_handle, ddr_handle, dt, model)

    # close any open connections
    env.finishSimulation()


if __name__ == "__main__":
    main()

