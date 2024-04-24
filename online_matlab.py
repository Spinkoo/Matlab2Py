import numpy as np
from .engine_wrapper_mat import Engine

#to add in the assertion params
#set_param(bdroot,'SimulationCommand','pause'), disp(sprintf('\nSimulation paused.'))
#Simulation path


#Matlab wrapper
class OnlineEngine(Engine):
    def __init__(self, model_path : str, sim_path : str, model_name : str, matlab_stepper:str = 'step_time', simulation_type ='sbs') -> None:

        super().__init__(model_path, sim_path, model_name)
        
        self.step_counter = 1
        self.matlab_stepper = matlab_stepper
        self.sim_type = simulation_type
        self.step_fn = self.init_steps_dict()
    
    # Initialize the dictionary of step functions
    def init_steps_dict(self) -> dict:
        return {'sbs' : self.step_by_step, 'sparsesbs' : self.sparsesbs, 'normal' : self.do_nothing}
    
    # Step by step simulation
    def step_by_step(self):
        self.set_param(f'{self.model_name}/{self.matlab_stepper}', str(9999))
        self.start_pause_simulation()

    # Sparse Step by step simulation, the idea is to skip certain number of steps if they are superfluous 

    def sparsesbs(self):
        self.timestep_forward()

    def do_nothing(self):
        pass
    
    def step_forward(self):
        self.step_fn[self.sim_type]()

    
    # Set maximum steps for the simulation, sort of timeout
    def set_max_steps(self, max_iter : int, max_iter_block = 'max_sim_time') -> None:
        self.set_param(f'{max_iter_block}', str(max_iter), )

    """An assertion block needs to be created in order to properly pause the simulation on Matlab each N steps (check simulink model)"""
    def set_step_size(self, step_sz):

        assert self.sim_type == 'sparsesbs', 'Simulation type has to be set to step by step (sbs), an assertion block should set inplace inside the simulation'
        self.step_size = step_sz
        self.set_param(f'{self.matlab_stepper}', str(step_sz), )
    
    def forward_sim(self) -> None:
        self.step_counter +=1
        current_time = self.step_counter * self.step_size
        t = f'{current_time:.1f}'
         
        self.set_param(f'{self.matlab_stepper}', t)



    def timestep_forward(self) -> None:
        self.forward_sim()
        self.eng.set_param(self.model_name, 'SimulationCommand', 'continue', nargout = 0)

    #This requires a Display / Calculation block on the Simuliation side, basically any block that has input and output ports
    def get_runtime_attribute(self, attribute : str, block_path : str, inport = True, port = 1, param_name = 'RuntimeObject'):
        assert self.sim_type != "normal", "Can't access Runtime attributes after the simulation is finished" 
        try:
            br = self.get_param(f'{block_path}/{attribute}', param_name)
            #time.sleep(.01)
            self.eng.workspace['br'] = br
            return self.eng.eval(f"br.{'InputPort' if inport else 'OutpotPort'}({port}).data") # Access displayed  data
        except Exception as e:
            print(e)
            self.stop_simulation()  
            return -1
 


