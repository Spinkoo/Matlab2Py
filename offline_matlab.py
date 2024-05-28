import numpy as np
from .engine_wrapper_mat import Engine

#to add in the assertion params
#set_param(bdroot,'SimulationCommand','pause'), disp(sprintf('\nSimulation paused.'))
#Simulation path







#Matlab wrapper
class OfflineEngine(Engine):

    def __init__(self, model_path : str, sim_path : str, model_name = str) -> None:
        super().__init__(model_path, sim_path, model_name)


    def setup_workspace(self, inputs : dict):
        for attribute, v in inputs.items():
            self.write_ws_value(attribute = attribute, value=v)
    
    def setup_blocks(self, inputs : dict[str, tuple[any, str]]):
        for block_path, block_value in inputs.items():
            value, prop = block_value 
            self.set_param(block_path, value, prop)

    def filter_output(self, output, property ,attribute):
        return self.eng.find(self.eng.get(output, property), attribute)
    
    def retieve_from_logsout(self, output, attribute, prop = 'logsout'):
        temp = self.filter_output(output, prop, attribute)

        #create temporary variable in  matlab workspace to access it easily
        self.eng.workspace['temp'] = temp
        return self.eng.eval('temp.Values.Data')
    
    def get_simoutput(self, output, Toworkspace  : str = 'simout'):
        return self.eng.get(output, Toworkspace)
    
    def run_full_sim(self, wsinputs : dict = None, blocks_inputs : dict = None ):


        if wsinputs :
            self.setup_workspace(wsinputs)
        if blocks_inputs:
            self.setup_blocks(blocks_inputs)

        out = self.eng.sim(self.model_path)
        return out
    

        


# Start MATLAB engine

if __name__ == '__main__':

    #Debugging

    SIMULATION_PATH = 'simple_sim/'
    model_name = 'test'
    MODEL_PATH = f"{SIMULATION_PATH}{model_name}.slx"
    
    eng = OfflineEngine(model_path = MODEL_PATH, sim_path = SIMULATION_PATH, model_name = model_name,)
    eng.load_engine()

    #Run your .m initializing script
    eng.run_engine_script('init')
    eng.set_simulation_mode('Normal')
    seeds = np.random.randint(0, np.iinfo(np.int32).max, size = 3)

    o = eng.run_full_sim(blocks_inputs={'gau' : (seeds, 'seed'), 'theta' : ([.5, .3, -1.2], 'Value')})

    sig = eng.get_simoutput(o, 'simout')
    print(sig)

    # Close the MATLAB engine session
    
