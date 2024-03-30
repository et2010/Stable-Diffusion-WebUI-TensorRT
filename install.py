import launch
import subprocess
import sys

python = sys.executable


def install():
    if not launch.is_installed("importlib_metadata"):
        launch.run_pip("install importlib_metadata", "importlib_metadata", live=True)
    from importlib_metadata import version

    if launch.is_installed("tensorrt"):
        if not version("tensorrt") == "9.2.0.post12.dev5":
            launch.run(
                ["python", "-m", "pip", "uninstall", "-y", "tensorrt"],
                "removing old version of tensorrt",
            )

    if not launch.is_installed("tensorrt"):
        print("TensorRT is not installed! Installing...")
        launch.run_pip(
            "install nvidia-cudnn-cu11==8.9.4.25 --no-cache-dir", "nvidia-cudnn-cu11"
        )
        launch.run_pip(
            "install --pre --extra-index-url https://pypi.nvidia.com tensorrt==9.2.0.post12.dev5 --no-cache-dir",
            "tensorrt",
            live=True,
        )
    uninstall_package(
        "nvidia-cudnn-cu11",
        "removing nvidia-cudnn-cu11",
    )
    # Polygraphy
    if not launch.is_installed("polygraphy"):
        print("Polygraphy is not installed! Installing...")
        launch.run_pip(
            "install polygraphy --extra-index-url https://pypi.ngc.nvidia.com",
            "polygraphy",
            live=True,
        )

    # ONNX GS
    if not launch.is_installed("onnx_graphsurgeon"):
        print("GS is not installed! Installing...")
        launch.run_pip("install protobuf==3.20.2", "protobuf", live=True)
        launch.run_pip(
            "install onnx-graphsurgeon --extra-index-url https://pypi.ngc.nvidia.com",
            "onnx-graphsurgeon",
            live=True,
        )

    # OPTIMUM
    if not launch.is_installed("optimum"):
        print("Optimum is not installed! Installing...")
        launch.run_pip(
            "install optimum",
            "optimum",
            live=True,
        )

    ###########################################################
    ############# ControlNet ##################################

    # Diffusers
    if not launch.is_installed("diffusers"):
        print("Diffusers is not installed! Installing...")
        launch.run_pip(
            "install diffusers",
            "diffusers",
            live=True,
        )
    if not launch.is_installed("transformers"):
        print("Transformers is not installed! Installing...")
        launch.run_pip(
            "install transformers",
            "transformers",
            live=True,
        )
    if not launch.is_installed("accelerate"):
        print("accelerate is not installed! Installing...")
        launch.run_pip(
            "install accelerate",
            "accelerate",
            live=True,
        )
    if not launch.is_installed("optimum"):
        print("Diffusers is not installed! Installing...")
        launch.run_pip(
            "install optimum",
            "optimum",
            live=True,
        )

    # OpenCV
    if not launch.is_installed("cv2"):
        print("OpenCV is not installed! Installing...")
        launch.run_pip(
            "install opencv-contrib-python",
            "opencv-contrib-python",
            live=True,
        )

    # ControlNet AUX
    if not launch.is_installed("controlnet_aux"):
        print("ControlNetAux is not installed! Installing...")
        launch.run_pip(
            "install controlnet-aux",
            "controlnet-aux",
            live=True,
        )

def uninstall_package(package, description):
    print(description)
    try:
        subprocess.run(["python", "-m", "pip", "uninstall", "-y", package], check=True)
        print(f"Successfully uninstalled {package}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to uninstall {package}: {e}")

install()
