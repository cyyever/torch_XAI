import importlib

from cyy_torch_xai.lean_hydra.lean_hydra_config import LeanHyDRAConfig

has_cyy_torch_vision: bool = importlib.util.find_spec("cyy_torch_vision") is not None


def test_lean_hydra() -> None:
    if not has_cyy_torch_vision:
        return
    import cyy_torch_vision  # noqa: F401

    config = LeanHyDRAConfig(dataset_name="MNIST", model_name="LeNet5")
    config.hyper_parameter_config.epoch = 2
    # config.hyper_parameter_config.learning_rate_scheduler_name = "CosineAnnealingLR"
    # config.hyper_parameter_config.optimizer_name = "Adam"
    config.hyper_parameter_config.optimizer_name = "SGD"
    config.hyper_parameter_config.learning_rate = 0.01
    trainer = config.create_deterministic_trainer()
    trainer.train()
    res = config.recreate_trainer_and_hook()
    trainer = res["trainer"]
    hydra_obj = res["hook"]

    hydra_obj.set_computed_indices([0, 1])
    trainer.train()
