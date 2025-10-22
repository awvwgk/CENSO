"""Tests for PartsConfig"""

import pytest
from censo.config.parts_config import PartsConfig
from censo.config.parts import (
    GeneralConfig,
    PrescreeningConfig,
    ScreeningConfig,
    OptimizationConfig,
    RefinementConfig,
    NMRConfig,
    UVVisConfig,
)
from censo.params import OrcaSolvMod, TmSolvMod


def test_parts_config_default_initialization():
    """Test that PartsConfig initializes with default values"""
    config = PartsConfig()

    # Test that all parts are initialized with their default configurations
    assert isinstance(config.general, GeneralConfig)
    assert isinstance(config.prescreening, PrescreeningConfig)
    assert isinstance(config.screening, ScreeningConfig)
    assert isinstance(config.optimization, OptimizationConfig)
    assert isinstance(config.refinement, RefinementConfig)
    assert isinstance(config.nmr, NMRConfig)
    assert isinstance(config.uvvis, UVVisConfig)


def test_parts_config_str_representation():
    """Test the string representation of PartsConfig"""
    config = PartsConfig()
    str_repr = str(config)

    # Verify that the string representation contains all parts
    assert str_repr.count("\n") > 0  # Should have multiple lines
    for part_name in [
        "general",
        "prescreening",
        "screening",
        "optimization",
        "refinement",
        "nmr",
        "uvvis",
    ]:
        assert part_name in str_repr.lower()


@pytest.mark.parametrize(
    "solvent,sm_model,should_pass",
    [
        ("water", OrcaSolvMod.CPCM, True),  # Valid combination
        ("chloroform", OrcaSolvMod.SMD, True),  # Valid combination
        ("invalid_solvent", OrcaSolvMod.CPCM, False),  # Invalid solvent
    ],
)
def test_solvent_model_validation(solvent, sm_model, should_pass):
    """Test solvent model validation with different combinations"""
    config = PartsConfig()
    config.general.solvent = solvent

    # Set the same solvent model for all parts that use it
    config.screening.sm = sm_model
    config.optimization.sm = sm_model
    config.refinement.sm = sm_model
    config.nmr.sm = sm_model
    config.uvvis.sm = sm_model

    if should_pass:
        # Should not raise any validation errors
        config.model_validate(config, context={"check_all": True, "check_paths": False})
    else:
        # Should raise ValueError for invalid combinations
        with pytest.raises(ValueError, match="not available with"):
            config.model_validate(config, context={"check_all": True})


def test_custom_config_values():
    """Test PartsConfig with custom values"""
    custom_config = PartsConfig(
        general=GeneralConfig(solvent="water"),
        screening=ScreeningConfig(sm=OrcaSolvMod.CPCM),
        optimization=OptimizationConfig(sm=OrcaSolvMod.CPCM),
    )

    assert custom_config.general.solvent == "water"
    assert custom_config.screening.sm == OrcaSolvMod.CPCM
    assert custom_config.optimization.sm == OrcaSolvMod.CPCM


def test_invalid_solvent_combination():
    """Test that invalid solvent/model combinations raise appropriate errors"""
    config = PartsConfig()
    config.general.solvent = "dmf"
    config.screening.sm = OrcaSolvMod.CPCM
    config.optimization.sm = TmSolvMod.DCOSMORS  # Different solvent model

    # Should raise ValueError due to incompatible solvent/model combination
    with pytest.raises(ValueError):
        config.model_validate(config, context={"check_all": True})


def test_paths_model_validation():
    """Test that missing paths raise proper validation errors when check_paths=True"""
    config = PartsConfig()
    # Do not set required paths; assume default config is missing some required paths
    with pytest.raises(ValueError, match="path is not set in the configuration"):
        config.model_validate(config, context={"check_all": True, "check_paths": True})


def test_parts_validation():
    config = PartsConfig()
    config.screening.func = "invalid"
    with pytest.raises(ValueError):
        config.model_validate(config, context={"check": "screening"})

    config = PartsConfig()
    config.screening.gsolv_included = True
    config = config.model_validate(config, context={"check": "screening"})
    assert not config.screening.gsolv_included
