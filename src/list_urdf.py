from pathlib import Path
import os

class listURDF:
    def __init__(self):
        pass

    def list_URDF(self):
    # Path to the current script
        script_path = Path(__file__)

        # Directory the script is located in
        script_dir = script_path.parent
        script_dir_dir = script_dir.parent

        print("Script path:", script_path)
        print("Script directory:", script_dir)
        print("Script dir directory:", script_dir_dir)

        folder = os.path.join(script_dir_dir, "data", "object2urdf", "examples", "ycb_assets")
        print("FOLDER: ", folder)

        urdf_list = []

        for file in Path(folder).glob("*.urdf"):
            if file.is_file():
                # print(file.name)
                urdf_list.append(file.name)

        urdf_list.remove("_prototype.urdf")
        sorted_files = sorted(urdf_list, key=lambda x: int(x[:3]))


        return sorted_files

