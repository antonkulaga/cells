# cells

The command-line tool that runs segmentation using cellpose model on your 

# Setting up

Install pixi (see https://pixi.sh/latest/ for more details).
Install dependencies:
```bash
pixi install
```
Activate the environment (note you can configure it in IDEs as if it is conda using ./pixi/envs/default/bin/python)
```bash
pixi shell
```

# running
```bash
pixi run python cells/run.py data/test --dimeter 15
```
You have to give expected cell diameter in pixels as parameter, otherwise it tries to guess it.
By default, it assumes grayscale images and creates segmented folder for segmentations.
It also tries to estimate cell count and creates counts.csv file