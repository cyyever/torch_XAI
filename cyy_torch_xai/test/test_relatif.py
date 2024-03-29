from cyy_torch_toolbox import Config

from ..inverse_hessian_vector_product import default_inverse_hvp_arguments
from ..relatif import compute_relatif

try:
    import cyy_torch_vision  # noqa: F401

    def test_IF() -> None:
        config = Config(dataset_name="MNIST", model_name="LeNet5")
        config.hyper_parameter_config.epoch = 10
        config.hyper_parameter_config.learning_rate = 0.01
        trainer = config.create_trainer()
        trainer.train()
        default_inverse_hvp_arguments["scale"] = 1000
        default_inverse_hvp_arguments["epsilon"] = 100
        default_inverse_hvp_arguments["repeated_num"] = 1
        compute_relatif(trainer, training_indices=[1, 2])

except BaseException:
    pass
