def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_forms(cldf_dataset):
    assert len(list(cldf_dataset["FormTable"])) == 8360
    assert any(f["Form"] == "tɯŋɯrak" for f in cldf_dataset["FormTable"])


def test_languages(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset["LanguageTable"])) == 32


# ...contains 254 different concepts
def test_parameters(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset["ParameterTable"])) == 254
