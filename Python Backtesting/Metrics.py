import matplotlib.pyplot as plt
import numpy as np


class Strategy:

    def __init__(self, name, returns):
        self.name = name
        self.returns = returns
        self.pnl = np.c_[np.array([100.]), 100.*np.cumprod(1.+returns.to_numpy()).reshape(1,-1)].flatten()
        
#Annual volatility/ 252 is the trading days in a year
    
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
                                                          (self.volatility(), self.sharpe_ratio(), self.max_drawdown()))
        ax.set_xlabel('Time')
        ax.set_ylabel('PnL')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        ax.set_title(f'PnL of the strategy {self.name}')
        ax.grid(axis='x', linestyle='--')
        fig.tight_layout()
        fig.savefig(f'{self.name}.pdf')
        plt.show()


if __name__ == "__main__":
    import pandas as pd
    test = Strategy("test", pd.Series(np.random.random(1000)))
    print(test.volatility())
    # test.illustrate()