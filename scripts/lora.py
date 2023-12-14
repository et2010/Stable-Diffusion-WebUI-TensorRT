import os
from typing import List
import numpy as np
from safetensors.torch import load_file
import onnx_graphsurgeon as gs
import onnx
import torch
from onnx import numpy_helper


def merge_loras(loras: List[str], scales: List[str], model_name: str):
    refit_dict = {}
    for lora, scale in zip(loras, scales):
        lora_dict = load_file(os.path.join(lora, model_name + ".refit"))
        for k, v in lora_dict.items():
            if k in refit_dict:
                refit_dict[k] += scale * v
            else:
                refit_dict[k] = scale * v
    return refit_dict


def apply_loras(
    base_path: str, loras: List[str], scales: List[str], model_name: str
) -> dict:
    refit_dict = merge_loras(loras, scales, model_name)
    base = onnx.load(os.path.join(base_path, model_name + ".onnx"))
    onnx_opt_dir = os.path.dirname(base_path)

    def convert_int64(arr):
        if len(arr.shape) == 0:
            return np.array([np.int32(arr)])
        return arr

    for initializer in base.graph.initializer:
        if initializer.name not in refit_dict:
            continue

        wt = refit_dict[initializer.name]
        initializer_data = numpy_helper.to_array(
            initializer, base_dir=onnx_opt_dir
        ).astype(np.float16)
        delta = torch.tensor(initializer_data).to(wt.device) + wt

        refit_dict[initializer.name] = delta.contiguous()

    return refit_dict