

import numpy as np
from src.classes.components import Recorte
# entradas: n, k, p
# n -> número de servidores
# k -> número mínimo de servidores funcionando
# p -> disponibilidade de cada servidor

# simulador deve ser capaz de:

# atravêz de várias rodadas, se aproximar da disponibilidade média
# dado os parâmetros n, k e p


# gerar array de verdadeiro ou falso para entrada n e p

class Operations:
    def __init__(self, n: int, k_range: str, p_range: str, step_k=1, step_p=50, division: str = "-"):
        self.n = n
        
        k_min, k_max = map(int, k_range.split(division))
        p_min, p_max = map(int, p_range.split(division))
        
        if not (0 < k_min <= k_max <= n):
            raise ValueError(f"Erro: k_range deve estar entre 1 e {n}. Recebido: {k_min}_{k_max}")
        
        if not (0 < p_min < p_max <= 1000):
            raise ValueError(f"Erro: p_range deve estar entre 1 e 1000. Recebido: {p_min}_{p_max}")
        
        self.k_range = np.arange(k_min, k_max + 1, step=step_k, dtype=int)
        self.p_range = np.arange(p_min, p_max + 1, step=step_p, dtype=int)/1000        
        self.p_range[-1] = p_max/1000
    
    # gera um vetor de 0 e 1 para n servidores e disponibilidade p
    # 1 -> disponível
    # 0 -> inidisponível
    @staticmethod
    def get_server_vector(n: int, p: float)->np.ndarray:
        return (np.random.rand(n) < p).astype(int)
    
    def get_server_matrix_p(self) -> np.ndarray:
        array = np.random.rand(self.n)
        return (array <= self.p_range.reshape(-1, 1)).astype(int)
    
    def get_server_matrix_p_k(self) -> np.ndarray:
        """
        Retorna uma matriz onde cada linha representa um valor de p e cada coluna representa um valor de k.
        O valor 1 indica que a condição (número de servidores disponíveis >= k) foi atendida.
        """
        server_matrix_p = self.get_server_matrix_p()
                
        available_servers = np.sum(server_matrix_p, axis=1, keepdims=True)

        return (available_servers >= self.k_range).astype(int)
    
class Simulator(Operations):
    def __init__(self, n, k_range, p_range, step_k=1, step_p=50, division = "-"):
        super().__init__(n, k_range, p_range, step_k, step_p, division)
        """
        Classe que recebe um número total de servidores (n) e os intervalos de valores para k e p,
        para gerar ranges de valores utilizando np.arange.

        Args:
            n (int): Quantidade total de servidores.
            k_range (str): String no formato "inicio_fim", representando o range de k.
            p_range (str): Range da disponibilidade de cada servidor (entre 0 e 1).
            step_k (int): Passo para os valores de k (padrão = 1).
            step_p (float): Passo para os valores de p (padrão: 1.0).
        """
        self.list_stack = None
    
    def get_server_matrix_disponibility(self, reset=False, rounds=10000):
        if self.list_stack is not None and not reset:
            return self.list_stack
        self.list_stack = np.stack([self.get_server_matrix_p_k() for _ in range(rounds)])
        return self.list_stack
    
    def get_server_mean_disponibility(self):
        return np.mean(self.get_server_matrix_disponibility(), axis=0)
    
    def get_server_mean_failure(self):
        return 1 - self.get_server_mean_disponibility()
    
    def get_server_std_disponibility(self):
        return np.std(self.get_server_matrix_disponibility(), axis=0)
    

    def get_slice(self, k_range: str = None, p_range: str = None, division="-"):
        if k_range:
            k_min, k_max = map(int, k_range.split(division))
            if not (0 < k_min <= k_max <= self.n):
                raise ValueError(f"Erro: k_range deve estar entre 1 e {self.n}. Recebido: {k_min}_{k_max}")
            k_range = np.where((self.k_range >= k_min) & (self.k_range <= k_max))[0]
        else:
            k_range = np.arange(len(self.k_range))

        if p_range:
            p_min, p_max = map(int, p_range.split(division))       
            if not (0 < p_min <= p_max <= 1000):
                raise ValueError(f"Erro: p_range deve estar entre 1 e 1000. Recebido: {p_min}_{p_max}")
            p_min, p_max = p_min / 1000, p_max / 1000
            p_range = np.where((self.p_range >= p_min) & (self.p_range <= p_max))[0]
        else:
            p_range = np.arange(len(self.p_range))

        print(k_range)
        print(p_range)
        return Recorte(self.list_stack[:, p_range, :][:, :, k_range], self.k_range[k_range], self.p_range[p_range])

        
        

if __name__ == "__main__":
    op = Simulator(14, "7-10", "001-900", step_p=50)
    matrix = op.get_server_matrix_disponibility(rounds=1000000)
    matrix_mean = op.get_server_mean_disponibility()
    print(matrix_mean)
    sliced = op.get_slice()
    print(sliced.get_server_mean_disponibility( ))
    