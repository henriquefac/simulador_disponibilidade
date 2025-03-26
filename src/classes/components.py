# recortes de uma tabela para selecionar os dados que precisa
import numpy as np

class Recorte():
    def __init__(self, matrix_stack: np.ndarray, k_range: np.ndarray, p_range: np.ndarray):
        self.list_stack = matrix_stack
        self.k_range = k_range 
        self.p_range = p_range
    
    def get_server_mean_disponibility(self):
        return np.mean(self.list_stack, axis=0)
    
    def get_server_mean_failure(self):
        return 1 - self.get_server_mean_disponibility()
    
    def get_server_std_disponibility(self):
        return np.std(self.list_stack, axis=0)
    
    