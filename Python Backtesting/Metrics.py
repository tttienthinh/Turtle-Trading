import matplotlib.pyplot as plt
import numpy as np


class Strategy:

    def __init__(self, name, returns):
        self.name = name
        self.returns = returns
        self.pnl = np.c_[np.array([100.]), 100.*np.cumprod(1.+returns.to_numpy()).reshape(1,-1)].flatten()

    def volatility(self):
        return np.std(self.returns)*np.sqrt(252)

    def sharpe_ratio(self):
        return np.mean(self.returns)*np.sqrt(252)/np.std(self.returns)

    def max_drawdown(self):
        return 1. - np.min(np.flip(np.minimum.accumulate(np.flip(self.pnl)))/self.pnl)

    def max_drawdown_2(self):
        return np.max(1. - self.pnl/np.maximum.accumulate(self.pnl))

    def illustrate(self):
        fig, ax = plt.subplots(1, 1)
        ax.plot(self.returns.index, self.pnl[1:], 'b', label=self.name + ' (vol: %.2f, Sharpe: %.2f, MDD: %.2f)'%
                                                          (self.volatility(), self.sharpe_ratio(), self.max_dd()))
        ax.set_xlabel('Time')
        ax.set_ylabel('PnL')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        ax.set_title(f'PnL of the strategy {self.name}')
        ax.grid(axis='x', linestyle='--')
        fig.tight_layout()
        fig.savefig(f'{self.name}.pdf')
        plt.show()


class CapiWeighted(Strategy):

    def __init__(self, name, returns, capitalizations):
        weights_CW = capitalizations.copy()
        weights_CW['sum'] = weights_CW.sum(axis=1)
        weights_CW = weights_CW.div(weights_CW['sum'], axis=0)
        weights_CW.drop(columns='sum', inplace=True)
        weights_CW = weights_CW.shift(1).dropna()
        returns_CW = (returns * weights_CW).sum(axis=1)
        super().__init__(name, returns_CW)