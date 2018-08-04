# Backtesting trading algos

The purpose of this repo is to invent and back test novel trading strategies/algorithms. It's recommended to use an UI-based OS (e.g. Windows) in combination with Canopy or a similar Python IDE (I use SublimeText 3 with anaconda plugin)

The module "algos/core.py" contains several core functions. It contains functions that allow you to record buy/sell signals, compute the ROI of a portfolio and even visualize all recorded signals on a Plotly chart.

Please preserve the naming convention "algo_NAME_vX" where NAME is an arbitrarily chosen name for your algo and X its version number. If you are going to develop an algorithm from scratch it is highly recommended to use an existing algorithm as a backbone/framework. If you are going to improve/alter an existing algorithm which was created by someone else then create a new file and increment the X's value.

## Dependencies

The file condalibs.txt contains a list of libraries which I've installed in my conda environment. These include Plotly, matplotlib and Tensforflow (which is not required for these backtesting scripts).

If you are going to use the visualization function ("portfolioToChart") then make sure you have Plotly installed. Or install it manually through:
```$ pip install plotly```
For more info: https://plot.ly/python/getting-started/

## Development
When editing imported modules (e.g. the "core.py"), make sure to restart your Python kernel, otherwise your system will remain using the outdated version. This was the case when using Canopy IDE, I did not have this issue with SublimeText IDE.

## Getting started
Once you have opened one of the available algorithms then try running it. When it's finished, the console will display your ROI, and if you have "portfolioToChart" enabled, then the system should automatically open up a new browser tab with the chart as shown on this image:

![first run](https://i.imgur.com/SDa8xps.png)

Plotly has many useful tools which you can use, such as zoom-in, pan, etc... when you scroll over the y-axis you will shrink it in the Y-direction (similar for X-axis). For more cool features visit Plotly's Python website.

Notice: on the image above there is a debug=1 variable. This is usually used for when you would like to debug/visualize your strategy and portfolio. When you disable debugging (debug=0) then you're usually about to simulate many (hundreds) of ROI calculations (if necessary that is).

## Using SublimeText(v3)
If you're Sublime fanatic like me, then follow along.
1. First install the Anaconda (conda) plugin for SublimeText which allows you to manage environments and more (Google the install instructions).
2. Once you've done that, make sure you already have an anaconda environment with the Plotly library installed (and its dependencies).
3. Open some algorithm in Sublime, then hit Ctrl+Shift+P to open the actions menu, and type in "conda: activate environment" and hit enter.
![](https://i.imgur.com/twCWFwZ.png)
4. Select your environment (it's called tensorflow in my case).
![](https://i.imgur.com/1DOgN4l.png)
5. Finally you are ready to run the script, doing so by pressing ctrl+b . Once it's finished (and depending on the script) it may open a chart with the Buy/Sell signals and more.
![](https://i.imgur.com/nGSaUl0.png)

