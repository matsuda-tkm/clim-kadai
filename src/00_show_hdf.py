from pathlib import Path
from loguru import logger
import h5py
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


def setup_path(filename: str) -> Tuple[Path, Path]:
    # data
    h5_path = Path(Path(__file__).parent.parent / Path("data") / filename)
    if not h5_path.exists():
        logger.error(f"File does not exist: {h5_path}")
        exit(1)
    logger.debug(f"data: {h5_path}")

    # output
    output_dir = Path(Path(__file__).parent.parent / Path("output") / Path(__file__).stem)
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"output dir: {output_dir}")

    return h5_path, output_dir


if __name__ == "__main__":
    h5_path, output_dir = setup_path("GPMMRG_MAP_2401010500_H_L3S_MCH_05C.h5")
    logger.add(output_dir / f"{Path(__file__).stem}.txt", mode="w")

    with h5py.File(h5_path, "r") as data:
        logger.info("Keys:")
        for key in data.keys():
            logger.info("\t" + key)

        logger.info("Groups:")
        for subkey in data["Grid"].keys():
            logger.info("\t" + subkey)

        arr = np.asarray(data["Grid"]["hourlyPrecipRate"])
        plt.imshow(arr, cmap="jet")
        plt.colorbar()
        plt.tight_layout()
        plt.savefig(output_dir / "00_show_hdf.png")
