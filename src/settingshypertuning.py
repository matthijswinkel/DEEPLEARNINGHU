from pathlib import Path
from typing import Dict, Optional, Union

from pydantic import BaseModel, HttpUrl, root_validator
from ray import tune

SAMPLE_INT = tune.search.sample.Integer
SAMPLE_FLOAT = tune.search.sample.Float


class BaseSearchSpace(BaseModel):
    input_size: int
    output_size: int
    tune_dir: Optional[Path]
    data_dir: Path

    class Config:
        arbitrary_types_allowed = True

    @root_validator
    def check_path(cls, values: Dict) -> Dict:  # noqa: N805
        datadir = values.get("data_dir")
        if not datadir.exists():
            raise FileNotFoundError(
                f"Make sure the datadir exists.\n Found {datadir} to be non-existing."
            )
        return values


# this is what ray will use to create configs
class SearchSpace(BaseSearchSpace):
    hidden_size: Union[int, SAMPLE_INT] = tune.randint(16, 128)
    dropout: Union[float, SAMPLE_FLOAT] = tune.uniform(0.0, 0.3)
    num_layers: Union[int, SAMPLE_INT] = tune.randint(2, 5)


class BaseSettings(BaseModel):
    data_dir: Path


cwd = Path(__file__).parent
cwd = (cwd / "../").resolve()


class GeneralSettings(BaseSettings):
    data_dir = cwd / "data/raw"


class VAESettings(GeneralSettings):
    h1: int = 250
    h2: int = 100
    insize: int = 784
    latent: int = 10
    batchsize: int = 32
    epochs: int = 100
    modelname: Path = Path("vaemodel.pt")
    imgpath: Path = Path("img")
    samplesize: int = 512


class SiameseSettings(GeneralSettings):
    url: HttpUrl = "https://github.com/maticvl/dataHacker/raw/master/DATA/at%26t.zip"
    filename: Path = Path("faces.zip")
    training: Path = Path("data/faces/training/")


class EurosatSettings(BaseSettings):
    data_dir = Path("../data/raw")
    valid_paths = Path("ds")


class StyleSettings(BaseSettings):
    data_dir = Path("../../data/external")
    trainpath = Path("../../data/external/sentences/train.feather")
    testpath = Path("../../data/external/sentences/test.feather")


class ImageExplainerSettings(GeneralSettings):
    datadir: Path = Path("../../../data/raw/")
    epochs: int = 10
    modelname: Path = Path("trained_model.pt")
    imgpath: Path = Path("img")
    num_classes: int = 10
