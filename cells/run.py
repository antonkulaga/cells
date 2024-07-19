from collections import OrderedDict
from typing import Optional, Any
from cellpose import models
from cellpose import plot
import numpy as np
import typer
from pathlib import Path
import matplotlib.pyplot as plt
from pims import ImageSequence
from pycomfort import files
from pathlib import Path
import pims
from cellpose import models
from loguru import logger
from segmentation import write_folder_segmentation

app = typer.Typer()

@app.command("segment")
def segment_folder(folder: Path = Path("./data/test"),
                              output: Optional[Path] = Path("./data/output"),
                              extension: str = "tif",
                              diameter: int = 15,
                              model_name: str = "cyto3",
                              gpu: bool = False
                              ):
    return write_folder_segmentation(folder, output, extension, diameter, model_name, gpu)

if __name__ == "__main__":
    app()