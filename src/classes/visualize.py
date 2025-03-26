import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.classes.simulator import Simulator, Recorte

class SimulatorVisualizer():
    def __init__(self, object_data: Simulator | Recorte, simulacoes = 10000):
        self.data: Simulator | Recorte = object_data

    def plot_fixed_availability_curve(self, value_fix: int, flag: bool = False):
        """Plota a variação da disponibilidade fixando K ou P.
        
        - Se `flag=False`: Fixa `k=value_fix` e varia `p` no range completo.
        - Se `flag=True`: Fixa `p=value_fix` e varia `k` no range completo.

        Args:
            value_fix (int): O valor fixo de `k` ou `p` (dependendo da flag).
            flag (bool, optional): Define se `p` ou `k` será fixo. Default é `False` (fixa `k`).
        """
        plt.figure(figsize=(8, 6))
        mean_disponibility = self.data.get_server_mean_disponibility()

        if flag:
            if value_fix not in self.data.p_range:
                raise ValueError(f"O valor de p={value_fix} não está no range disponível.")
            idx_p = np.where(self.data.p_range == value_fix)[0][0]

            plt.plot(self.data.k_range, mean_disponibility[idx_p, :], marker='o', linestyle='-', color='b')
            plt.xlabel("Número mínimo de servidores ativos (k)")
            plt.ylabel("Probabilidade de Sucesso")
            plt.title(f"Probabilidade Fixando p={value_fix}")
        else:
            if value_fix not in self.data.k_range:
                raise ValueError(f"O valor de k={value_fix} não está no range disponível.")
            idx_k = np.where(self.data.k_range == value_fix)[0][0]

            plt.plot(self.data.p_range, mean_disponibility[:, idx_k], marker='o', linestyle='-', color='r')
            plt.xlabel("Disponibilidade Individual (p)")
            plt.ylabel("Probabilidade de Sucesso")
            plt.title(f"Probabilidade Fixando k={value_fix}")

        plt.grid()
        plt.show()
    
    
    def plot_availability_curves(self):
        """
        Plota a probabilidade de sucesso (ter pelo menos k servidores funcionando)
        em função da disponibilidade p.
        """
        plt.figure(figsize=(8, 6))
        mean_disponibility = self.data.get_server_mean_disponibility()

        for i, k in enumerate(self.data.k_range):
            plt.plot(self.data.p_range, mean_disponibility[:, i], label=f'k = {k}')

        plt.xlabel("Disponibilidade Individual (p)")
        plt.ylabel("Probabilidade de Sucesso")
        plt.title("Curvas de Disponibilidade")
        plt.legend()
        plt.grid()
        plt.show()
        
    def plot_heatmap(self):
        """
        Plota um heatmap para visualizar a probabilidade de sucesso dependendo de k e p.
        """
        plt.figure(figsize=(8, 6))
        mean_disponibility = self.data.get_server_mean_disponibility()

        sns.heatmap(mean_disponibility, annot=True, cmap="coolwarm",
                    xticklabels=self.data.k_range, yticklabels=np.round(self.data.p_range, 2), cbar=True)

        plt.xlabel("Número mínimo de servidores ativos (k)")
        plt.ylabel("Disponibilidade individual dos servidores (p)")
        plt.title("Heatmap da Probabilidade de Servidores Ativos")
        plt.show()