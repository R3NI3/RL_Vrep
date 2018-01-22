import vrep
import numpy as np
import random
import time
from enviroment import vrep_env

ip = '127.0.0.1'
port = 19997
time_step = 0.01
motor_names = ['LeftMotor', 'RightMotor']
object_names = ['Bola']
robot_names = ['DifferentialDriveRobot']

NUM_ACT = 10 #discretization of actions per motor

#def select_action(epsilon, state):
#    sample = random.random()

#    if sample > epsilon:
        #greedy
        #return model(Variable(state, volatile=True).type(FloatTensor)).data.max(1)[1].view(1, 2)
#    else:
#        return LongTensor([[random.randrange(NUM_ACT), random.randrange(NUM_ACT)]])


def get_reward(state_info):
    reward = 0
    robot_pos = state_info[0]
    target_pos = state_info[2]
    distance = np.linalg.norm(robot_pos - target_pos)
    reward = 1/ distance if distance != 0 else 1000
    return reward


def main():
    env = vrep_env(ip, port, time_step, motor_names, robot_names, object_names)

    model = None
    # --------- Stop Sim ----
    env.startSimulation()
    env.stop_robot(motor_names)
    env.stopSimulation()
    print('done')
    time.sleep(.05)

    # --------- Dummy Sim ---
    num_simulations = 0
    while(num_simulations < 2):
        env.startSimulation()
        dt = 0
        while (dt < 1):
            env.setJointVelocity(motor_names, [10,10])
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
    #vrep.simxFinish(-1)
    env.finishSimulation()


if __name__ == "__main__":
    main()

