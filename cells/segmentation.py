from collections import OrderedDict
from pathlib import Path
from typing import Optional
import csv

import matplotlib.pyplot as plt
import numpy as np
import pims
from cellpose import models
from cellpose import plot
from cellpose import utils
from cellpose.plot import mask_overlay
from loguru import logger
from pims import ImageSequence


def load_grey_folder(folder: Path, extension: str = "tif") -> OrderedDict[Path, np.ndarray]:
    """
    Loads micrsocopy images and converts them to gray
    :param folder:
    :param extension:
    :return:
    """
    experiment: ImageSequence = ImageSequence(str(folder)+f"/*.{extension}")
    results: OrderedDict[Path, np.array] = OrderedDict([ (Path(f), pims.as_grey(experiment.get_frame(i)).squeeze()) for i, f in enumerate(experiment._filepaths)])
    return results


def write_image_segmentation(img: np.ndarray, masks: np.ndarray, where: Optional[Path] = None) -> plt.Figure:
    img_out = img.copy()

    if img_out.shape[0] < 4:
        img_out = np.transpose(img_out, (1, 2, 0))
    if img_out.shape[-1] < 3 or img_out.ndim < 3:
        img_out = np.repeat(img_out[:, :, np.newaxis], 3, axis=2) #image_to_rgb(img_out, channels=channels)
    else:
        if img_out.max() <= 50.0:
            img_out = np.uint8(np.clip(img_out, 0, 1) * 255)

    # Create mask overlay
    overlay = mask_overlay(img_out.copy(), masks)
    outlines = utils.masks_to_outlines(masks)
    outX, outY = np.nonzero(outlines)
    overlay[outX, outY] = np.array([255, 0, 0])  # pure red

    # Create before-after figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    ax1.imshow(img, cmap='gray')
    ax1.set_title(f'Original ( {where.name} )')
    ax1.axis('off')

    ax2.imshow(overlay)
    count = int(masks.max())
    title = "Segmented" if count is None else f"Segmented (count = {count})"
    ax2.set_title(title)
    ax2.axis('off')

    plt.tight_layout()

    if where is not None:
        count = int(masks.max())
        if count != 0:
            stem = where.stem
            suffix = where.suffix
            new_filename = f"{stem}_count_{count}{suffix}"
            where = where.with_name(new_filename)
        fig.savefig(str(where), bbox_inches='tight', pad_inches=0)
        plt.close(fig)

    return fig

def write_folder_segmentation(folder: Path = Path("./data/test"),
                              output: Optional[Path] = Path("./data/output"),
                              extension: str = "tif",
                              diameter: int = 15,
                              model_name: str = "cyto3",
                              gpu: bool = False
                              ):
    image_dict = load_grey_folder(folder, extension=extension)
    channels = [0, 0]
    model = models.Cellpose(model_type=model_name, gpu=gpu)
    counts = []
    logger.info(f"Segmenting {folder.absolute().resolve()} and writing output to {output.absolute().resolve()}")
    for f, image in image_dict.items():
        masks, flows, styles, diameters = model.eval(image, diameter=diameter, channels=channels)
        where = (output / f.name)
        logger.info(f"writing segmentation to {where}")
        write_image_segmentation(image, masks, where)
        counts.append((where.name, int(masks.max())))
    if len(counts) > 0:
        # Define the output file path using Pathlib
        counts_path = output / 'counts.csv'
        with counts_path.open('w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Image', 'Counts'])  # Write header
            writer.writerows(counts)  # Write data rows
        logger.info(f"CSV file has been written to: {counts_path.resolve()}")
    return output