import unittest.mock as mock
from pathlib import Path

import numpy as np
import pytest

from geojson import FeatureCollection, Feature

from blockutils.common import ensure_data_directories_exist, TestDirectoryContext
from blockutils.syntheticimage import SyntheticImage
from blockutils.exceptions import UP42Error

from context import KMeansClustering, raise_if_too_large


@pytest.fixture(scope="session", autouse=True)
def fixture():
    ensure_data_directories_exist()


def test_kmeans_clustering():
    lcc = KMeansClustering(n_clusters=5, n_iterations=5, n_sieve_pixels=1)
    input_ar = np.random.uniform(0, 255, 30000).reshape(100, 100, 3)
    clusters_ar = lcc.run_kmeans(input_ar)
    assert len(clusters_ar.flatten()) == 10000
    assert len(np.unique(clusters_ar)) == 5
    assert np.min(clusters_ar) == 0
    assert np.max(clusters_ar) == 4

    lcc = KMeansClustering(n_clusters=3, n_iterations=8, n_sieve_pixels=16)
    input_ar = np.random.uniform(0, 10, 400000).reshape(200, 200, 10)
    clusters_ar = lcc.run_kmeans(input_ar)
    assert len(clusters_ar.flatten()) == 40000
    assert len(np.unique(clusters_ar)) == 3
    assert np.min(clusters_ar) == 0
    assert np.max(clusters_ar) == 2


def test_process():
    lcc = KMeansClustering(n_clusters=5, n_iterations=5, n_sieve_pixels=1)
    with TestDirectoryContext(Path("/tmp")) as temp:
        image_path, _ = SyntheticImage(
            100, 100, 4, "uint16", out_dir=temp / "input"
        ).create(seed=100)
        input_fc = FeatureCollection(
            [
                Feature(
                    geometry={
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [-8.89411926269531, 38.61687046392973],
                                [-8.8604736328125, 38.61687046392973],
                                [-8.8604736328125, 38.63939998171362],
                                [-8.89411926269531, 38.63939998171362],
                                [-8.89411926269531, 38.61687046392973],
                            ]
                        ],
                    },
                    properties={"up42.data_path": str(image_path.name)},
                )
            ]
        )
        output_fc = lcc.process(input_fc)
        assert output_fc.features


def test_raise_if_too_large():
    with mock.patch("rasterio.DatasetReader") as src:
        instance = src.return_value
        instance.meta["dtype"] = "uint8"
        instance.count = 4
        instance.shape = (10, 10)
        raise_if_too_large(instance)

        with pytest.raises(UP42Error, match=r".*[WRONG_INPUT_ERROR].*"):
            instance.meta["dtype"] = "float"
            instance.count = 4
            instance.shape = (500000, 500000)
            raise_if_too_large(instance)

        with pytest.raises(UP42Error, match=r".*[WRONG_INPUT_ERROR].*"):
            instance.meta["dtype"] = "uint8"
            instance.count = 4
            instance.shape = (500000, 500000)
            raise_if_too_large(instance)

        with pytest.raises(UP42Error, match=r".*[WRONG_INPUT_ERROR].*"):
            instance.meta["dtype"] = "uint16"
            instance.count = 4
            instance.shape = (500000, 500000)
            raise_if_too_large(instance)

        with pytest.raises(UP42Error, match=r".*[WRONG_INPUT_ERROR].*"):
            instance.meta["dtype"] = "uint8"
            instance.count = 4
            instance.shape = (10, 10)
            raise_if_too_large(instance, 1)
