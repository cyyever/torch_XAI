import torch
from cyy_torch_toolbox.hook import HookCollection
from cyy_torch_toolbox.ml_type import ModelExecutorHookPoint
from cyy_torch_toolbox.model_with_loss import ModelWithLoss

from .lean_hydra_sgd_hook import LeanHyDRASGDHook


class LeanHyDRA:
    def __init__(
        self,
        model,
        loss_function,
        optimizer,
        test_gradient,
        training_set_size,
    ):
        self.__hooks = HookCollection()
        if isinstance(optimizer, torch.optim.SGD):
            self._hydra_hook = LeanHyDRASGDHook(test_gradient=test_gradient)
            self.__hooks.append_hook(LeanHyDRASGDHook(test_gradient=test_gradient))
        else:
            raise RuntimeError(f"unsupported optimizer type {type(optimizer)}")

        self.optimizer = optimizer
        self.model_with_loss = ModelWithLoss(model, loss_function)
        self.__hooks.exec_hooks(
            ModelExecutorHookPoint.BEFORE_EXECUTE, training_set_size=training_set_size
        )
        self.__end_exe: bool = False

    def set_computed_indices(self, computed_indices):
        self._hydra_hook.set_computed_indices(computed_indices=computed_indices)

    def iterate(self, batch_indices, batch_input, batch_targets):
        self.__hooks.exec_hooks(
            ModelExecutorHookPoint.AFTER_FORWARD,
            model_with_loss=self.model_with_loss,
            sample_indices=batch_indices.tolist(),
            inputs=batch_input,
            targets=batch_targets,
        )
        self.__hooks.exec_hooks(
            ModelExecutorHookPoint.AFTER_OPTIMIZER_STEP,
            batch_size=len(batch_indices),
            step_skipped=False,
            optimizer=self.optimizer,
        )

    def get_contribution(self, **kwargs):
        if not self.__end_exe:
            self.__hooks.exec_hooks(ModelExecutorHookPoint.AFTER_EXECUTE)
            self.__end_exe = True
        return self._hydra_hook.contributions