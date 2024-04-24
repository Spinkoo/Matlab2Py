import matlab.engine
import numpy as np


class Engine:
    def __init__(self, model_path : str, sim_path : str, model_name : str) -> None:

        self.model_path = model_path
        self.model_name = model_name
        self.step_counter = 1
        self.sim_path = sim_path

    


    # Run a .m file on matlab
    def run_engine_script(self, script_name : str):
        f = getattr(self.eng, script_name)
        f(nargout = 0)

    #Access a folder
    def cd_folder(self, path):
        self.eng.cd(f'{path}', nargout = 0)

    # Load the Python-Matlab engine
    def load_engine(self) -> None:

        self.eng = matlab.engine.start_matlab()
        self.cd_folder(self.sim_path)
        

        #Load initalization script, for example after accessing the simulation path that contains your Init_Calcul_Coef.m script you can run it this way
        #self.eng.Init_Calcul_Coef(nargout = 0)
        self.model = self.eng.load_system(self.model_path)

    def set_simulation_mode(self, s_mode : str = 'accelerator') -> None:
        self.eng.set_param(self.model, 'SimulationMode', s_mode, nargout = 0)
    
    # Set maximum steps for the simulation, sort of timeout
    def set_max_steps(self, max_iter : int, max_iter_block = 'max_sim_time') -> None:
        self.set_param(f'{max_iter_block}', str(max_iter), )
   

    def start_simulation(self) -> None:
        self.eng.set_param(self.model_name, 'SimulationCommand', 'start', nargout = 0)

    #One step forward -this moves according to the simulation timestep-
    def start_pause_simulation(self) -> None:
        self.step_counter = 1
        #self.eng.set_param(self.model_name, 'SimulationCommand', 'pause', nargout = 0)
        self.eng.set_param(self.model_name, 'SimulationCommand', 'start', 'SimulationCommand', 'pause', nargout = 0)


    def end_simulation(self) -> None:
        self.eng.quit()
    
    def stop_simulation(self) -> None:
        self.eng.set_param(self.model_name, 'SimulationCommand', 'stop', nargout = 0)

    def update_simulation(self) -> None:
        self.eng.set_param(self.model_name, 'SimulationCommand', 'update', nargout = 0)
    
    def pause_simulation(self) -> None:
        self.eng.set_param(self.model_name, 'SimulationCommand', 'pause', nargout = 0)

    def get_param(self, block_path, param_name):
        return self.eng.get_param(f'{self.model_name}/{block_path}', param_name)

    
    def get_simout(self, Toworkspace = 'simout', ws = 'base'):
        return self.get_simulation_last_readings(Toworkspace, ws)
    
    # Get simulation status
    def get_simulation_status(self) -> str:
        return self.get_param("", 'SimulationStatus')
    
    """# Get robot sensors readings
    def get_robots_readings(self,  robot_output = 'robot_readings', ws = 'base',):
        return np.array(self.get_simulation_last_readings(robot_output, ws)[0], dtype=np.float16)"""
    
    def get_simulation_last_readings(self, attribute, ws = 'base'):
        br = self.eng.evalin(ws, attribute)
        self.eng.workspace['br'] = br
        return self.eng.eval(f"br.data")
    
    # Get workspace parameter
    def get_ws_value(self, attribute = 'Vitesse', ws = 'base'):
        return self.eng.evalin(ws, attribute)
    
    # Write to workspace
    def write_ws_value(self, attribute = 'Vitesse', ws = 'base', value = 0) -> None:
        self.eng.assignin(ws, attribute, value, nargout = 0)
    
    def set_param(self, block_path, value, type = 'Value') -> None:
        self.eng.set_param(f'{self.model_name}/{block_path}', type, str(value), nargout = 0)


