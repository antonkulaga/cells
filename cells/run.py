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
                   output_name: str = "segmented",
                   extension: str = "tif",
                   diameter: Optional[int] = None,
                   model_name: str = "cyto3",
                   show_outline: bool = False,
                   gpu: bool = False,
                   subfolders: bool = True  # Flag to control recursive processing
                   ) -> list[Path]:
    """Apply segmentation to the folder and its subfolders if subfolders=True, returning a list of processed paths."""
    processed_paths = []

    def process_directory(directory: Path):
        # Process the current folder
        # Apply segmentation
        write_folder_segmentation(directory, extension, diameter, model_name, gpu, show_outline, output_name)
        processed_paths.append(directory)

        if subfolders:
            logger.info(f"processing subfolders...")
            # Process subdirectories recursively
            for subfolder in directory.iterdir():
                if subfolder.is_dir() and not output_name in subfolder.name:
                    process_directory(subfolder)

    # Start processing from the top-level folder
    process_directory(folder)
    logger.info(f"processing finished...")
    return processed_paths

if __name__ == "__main__":
    app()