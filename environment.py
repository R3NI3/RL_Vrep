import vrep

class vrep_env():
    def __init__(self, ip, port, time_step, actuator_names, robot_names, object_names):
         # Connect to the V-REP continuous server
        self.clientID = vrep.simxStart(ip, port, True, True, -500000, 5)
        if self.clientID != -1: # if we connected successfully
            print ('Connected to remote API server')
        else:
            raise Exception()
        # -------Setup the simulation
        vrep.simxSynchronous(self.clientID, True) #if we need to be syncronous
        # move simulation ahead one time step
        vrep.simxSynchronousTrigger(self.clientID)

        vrep.simxSetFloatingParameter(self.clientID,
                vrep.sim_floatparam_simulation_time_step,
                time_step, # specify a simulation time step
                vrep.simx_opmode_oneshot)

        self.time_step = time_step
        self.act_names = actuator_names
        # get the handles for each motor and set up streaming
        self.act_handles = {}
        for name in actuator_names:
            _, obj_handle = vrep.simxGetObjectHandle(self.clientID,
                    name, vrep.simx_opmode_blocking)
            if _ !=0 : raise Exception()
            self.act_handles.update({name:obj_handle})

        # get handle for target and set up streaming
        self.obj_handles = {}
        for name in object_names:
            _, obj_handle = vrep.simxGetObjectHandle(self.clientID,
                    name, vrep.simx_opmode_blocking)
            if _ !=0 : raise Exception()
            self.obj_handles.update({name:obj_handle})

        # get robot handle
        self.ddr_handles = {}
        for name in robot_names:
            _, obj_handle = vrep.simxGetObjectHandle(self.clientID,
                    name, vrep.simx_opmode_blocking)
            if _ !=0 : raise Exception()
            self.ddr_handles.update({name:obj_handle})

    def stop_robot(self, actuator_names):
        motor_handles = [self.act_handles[act_name] for act_name in actuator_names
                            if act_name in self.act_handles]
        for ii,motor_handle in enumerate(motor_handles):
            # if force has changed signs,
            # we need to change the target velocity sign
            vrep.simxSetJointTargetVelocity(self.clientID,
                        motor_handle,
                        0, # target velocity
                        vrep.simx_opmode_blocking)
        # move simulation ahead one time step
        vrep.simxSynchronousTrigger(self.clientID)

    def get_position(self, obj_name):
        if obj_name in self.ddr_handles:
            obj_handle = self.ddr_handles[obj_name]
        elif obj_name in self.obj_handles:
            obj_handle = self.obj_handles[obj_name]
        elif obj_name in self.act_handles:
            obj_handle = self.act_handles[obj_name]
        else:
            return -1

        _, obj_xyz = vrep.simxGetObjectPosition(self.clientID, obj_handle,
                -1, # retrieve absolute, not relative, position
                vrep.simx_opmode_blocking)
        if _ !=0 : raise Exception()
        else: return obj_xyz

    def get_orientation(self, obj_name):
        if obj_name in self.ddr_handles:
            obj_handle = self.ddr_handles[obj_name]
        elif obj_name in self.obj_handles:
            obj_handle = self.obj_handles[obj_name]
        elif obj_name in self.act_handles:
            obj_handle = self.act_handles[obj_name]
        else:
            return -1

        _, obj_ang = vrep.simxGetObjectOrientation(self.clientID, obj_handle,
                -1, # retrieve absolute, not relative, position
                vrep.simx_opmode_blocking)
        if _ !=0 : raise Exception()
        else: return obj_ang

    def setJointVelocity(self, motor_names, target_velocity):
        for idx,motor_name in enumerate(motor_names):
            if motor_name in self.act_handles:
                vrep.simxSetJointTargetVelocity(self.clientID, self.act_handles[motor_name],
                            target_velocity[idx], # target velocity
                            vrep.simx_opmode_blocking)
            else:
                return -1
        vrep.simxSynchronousTrigger(self.clientID)
        return 0

    def getSimulationState(self):
        state = {}
        for name, handle in self.ddr_handles.items():
            state[name] = [self.get_position(name),self.get_orientation(name)]
        for name, handle in self.obj_handles.items():
            state[name] = [self.get_position(name),self.get_orientation(name)]

        return state

    def startSimulation(self):
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_blocking)

    def stopSimulation(self):
        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_blocking)

    def finishSimulation(self):
        vrep.simxFinish(self.clientID)


